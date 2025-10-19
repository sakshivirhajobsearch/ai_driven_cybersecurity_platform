package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;

class DatabaseManagerTest {

	private DatabaseManager dbManager;
	private Connection mockConn;
	private Statement mockStmt;
	private ResultSet mockRs;

	@BeforeEach
	void setup() throws Exception {
		dbManager = Mockito.spy(new DatabaseManager("jdbc:test", "user", "pass"));
		mockConn = mock(Connection.class);
		mockStmt = mock(Statement.class);
		mockRs = mock(ResultSet.class);

		doReturn(mockConn).when(dbManager).getConnection();
		when(mockConn.createStatement()).thenReturn(mockStmt);
	}

	@Test
	void testExecuteUpdate() throws Exception {
		when(mockStmt.executeUpdate("UPDATE test")).thenReturn(1);
		int result = dbManager.executeUpdate("UPDATE test");
		assertEquals(1, result);
		verify(mockStmt, times(1)).executeUpdate("UPDATE test");
	}

	@Test
	void testExecuteQuery() throws Exception {
		when(mockStmt.executeQuery("SELECT * FROM test")).thenReturn(mockRs);
		when(mockRs.getMetaData()).thenReturn(mock(java.sql.ResultSetMetaData.class));
		when(mockRs.getMetaData().getColumnCount()).thenReturn(1);
		when(mockRs.getMetaData().getColumnLabel(1)).thenReturn("col");
		when(mockRs.next()).thenReturn(true, false);
		when(mockRs.getObject(1)).thenReturn("value");

		List<Map<String, Object>> results = dbManager.executeQuery("SELECT * FROM test");
		assertEquals(1, results.size());
		assertEquals("value", results.get(0).get("col"));
	}
}
