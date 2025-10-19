package com.ai.driven.cybersecurity.platform.db;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class CentralDBSync {

	private final DatabaseManager localDb;
	private final DatabaseManager centralDb;

	public CentralDBSync(DatabaseManager localDb, DatabaseManager centralDb) {
		this.localDb = localDb;
		this.centralDb = centralDb;
	}

	/**
	 * Override this method for callback after sync
	 */
	public void onSyncComplete(int recordsSynced) {
		// Default empty
	}

	/**
	 * One-time sync
	 */
	public int syncOnce() throws SQLException {
		return syncInternal();
	}

	/**
	 * Periodic sync
	 */
	public void startSync(long intervalMs) {
		Thread syncThread = new Thread(() -> {
			while (true) {
				try {
					int count = syncInternal();
					onSyncComplete(count);
					Thread.sleep(intervalMs);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		syncThread.setDaemon(true);
		syncThread.start();
	}

	/**
	 * Core sync logic: copy unsynced local threats to central
	 */
	private int syncInternal() throws SQLException {
		int recordsSynced = 0;

		try (Connection localConn = localDb.getConnection(); Connection centralConn = centralDb.getConnection()) {

			String selectSql = "SELECT threat_id, threat_type, severity_level, source_ip, target_system, detected_at, handled "
					+ "FROM local_threats WHERE synced = FALSE";

			try (PreparedStatement selectStmt = localConn.prepareStatement(selectSql);
					ResultSet rs = selectStmt.executeQuery()) {

				String insertSql = "INSERT INTO central_threats (threat_id, threat_type, severity_level, source_ip, target_system, detected_at, handled) "
						+ "VALUES (?, ?, ?, ?, ?, ?, ?) "
						+ "ON DUPLICATE KEY UPDATE threat_type=VALUES(threat_type), severity_level=VALUES(severity_level), "
						+ "source_ip=VALUES(source_ip), target_system=VALUES(target_system), detected_at=VALUES(detected_at), handled=VALUES(handled)";

				try (PreparedStatement insertStmt = centralConn.prepareStatement(insertSql)) {
					while (rs.next()) {
						insertStmt.setInt(1, rs.getInt("threat_id"));
						insertStmt.setString(2, rs.getString("threat_type"));
						insertStmt.setString(3, rs.getString("severity_level"));
						insertStmt.setString(4, rs.getString("source_ip"));
						insertStmt.setString(5, rs.getString("target_system"));
						insertStmt.setTimestamp(6, rs.getTimestamp("detected_at"));
						insertStmt.setBoolean(7, rs.getBoolean("handled"));

						recordsSynced += insertStmt.executeUpdate();
					}
				}
			}

			// mark synced in local DB
			try (PreparedStatement updateStmt = localConn
					.prepareStatement("UPDATE local_threats SET synced = TRUE WHERE synced = FALSE")) {
				updateStmt.executeUpdate();
			}
		}

		return recordsSynced;
	}
}
