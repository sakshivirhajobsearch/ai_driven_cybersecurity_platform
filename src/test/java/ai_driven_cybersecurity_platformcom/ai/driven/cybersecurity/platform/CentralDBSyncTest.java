package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Timer;
import java.util.TimerTask;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;

public class CentralDBSyncTest {

	private final DatabaseManager localDb;
	private final DatabaseManager centralDb;

	public CentralDBSyncTest(DatabaseManager localDb, DatabaseManager centralDb) {
		this.localDb = localDb;
		this.centralDb = centralDb;
	}

	/**
	 * Start periodic sync
	 *
	 * @param intervalMillis interval in milliseconds
	 */
	public void startSync(long intervalMillis) {
		Timer timer = new Timer(true); // daemon
		timer.scheduleAtFixedRate(new TimerTask() {
			@Override
			public void run() {
				try {
					syncOnce();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
		}, 0, intervalMillis);
	}

	/**
	 * Single sync operation: sync local_threats → central_threats
	 */
	public void syncOnce() throws SQLException {
		try (Connection localConn = localDb.getConnection(); Connection centralConn = centralDb.getConnection()) {

			// Idempotent sync for local_threats
			try (PreparedStatement selectStmt = localConn.prepareStatement(
					"SELECT threat_id, threat_type, severity_level, source_ip, target_system, detected_at, handled "
							+ "FROM local_threats WHERE synced = FALSE");
					ResultSet rs = selectStmt.executeQuery()) {

				while (rs.next()) {
					int threatId = rs.getInt("threat_id");
					String threatType = rs.getString("threat_type");
					String severity = rs.getString("severity_level");
					String sourceIp = rs.getString("source_ip");
					String targetSystem = rs.getString("target_system");
					java.sql.Timestamp detectedAt = rs.getTimestamp("detected_at");
					boolean handled = rs.getBoolean("handled");

					// Upsert into central_threats
					try (PreparedStatement insertStmt = centralConn.prepareStatement(
							"INSERT INTO central_threats (threat_id, threat_type, severity_level, source_ip, target_system, detected_at, handled) "
									+ "VALUES (?, ?, ?, ?, ?, ?, ?) "
									+ "ON DUPLICATE KEY UPDATE threat_type = VALUES(threat_type), "
									+ "severity_level = VALUES(severity_level), " + "source_ip = VALUES(source_ip), "
									+ "target_system = VALUES(target_system), " + "detected_at = VALUES(detected_at), "
									+ "handled = VALUES(handled)")) {

						insertStmt.setInt(1, threatId);
						insertStmt.setString(2, threatType);
						insertStmt.setString(3, severity);
						insertStmt.setString(4, sourceIp);
						insertStmt.setString(5, targetSystem);
						insertStmt.setTimestamp(6, detectedAt);
						insertStmt.setBoolean(7, handled);
						insertStmt.executeUpdate();
					}

					// Mark local row as synced
					try (PreparedStatement updateStmt = localConn
							.prepareStatement("UPDATE local_threats SET synced = TRUE WHERE threat_id = ?")) {
						updateStmt.setInt(1, threatId);
						updateStmt.executeUpdate();
					}
				}
			}
		}
	}
}
