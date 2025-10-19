package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.junit.jupiter.api.Test;

import com.ai.driven.cybersecurity.platform.db.CentralDBSync;
import com.ai.driven.cybersecurity.platform.db.DatabaseManager;

public class CentralDBSyncIntegrationTest {

	private final String localUrl = "jdbc:mysql://localhost:3306/ai_driven_cybersecurity_platform_local?useSSL=false&allowPublicKeyRetrieval=true";
	private final String centralUrl = "jdbc:mysql://localhost:3306/ai_driven_cybersecurity_platform_central?useSSL=false&allowPublicKeyRetrieval=true";
	private final String user = "root";
	private final String password = "admin";

	@Test
	public void testSyncOnce() throws SQLException {
		DatabaseManager localDb = new DatabaseManager(localUrl, user, password);
		DatabaseManager centralDb = new DatabaseManager(centralUrl, user, password);

		CentralDBSync sync = new CentralDBSync(localDb, centralDb) {
			@Override
			public void onSyncComplete(int recordsSynced) {
				// Optional: log for test
				System.out.println("Records synced: " + recordsSynced);
			}
		};

		// Run one-time sync
		int syncedRecords = sync.syncOnce();
		System.out.println("Synced records: " + syncedRecords);

		int localCount = getRowCount(localUrl, "local_threats");
		int centralCount = getRowCount(centralUrl, "central_threats");

		assertEquals(localCount, centralCount, "local_threats and central_threats row count should match after sync");
	}

	private int getRowCount(String url, String tableName) throws SQLException {
		try (Connection conn = DriverManager.getConnection(url, user, password);
				Statement stmt = conn.createStatement();
				ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM " + tableName)) {
			if (rs.next())
				return rs.getInt(1);
		}
		return 0;
	}
}
