package com.ai.driven.cybersecurity.platform.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DatabaseManager {

	private final String url;
	private final String username;
	private final String password;

	public DatabaseManager(String url, String username, String password) {
		this.url = url;
		this.username = username;
		this.password = password;
	}

	public Connection getConnection() throws SQLException {
		return DriverManager.getConnection(url, username, password);
	}

	public boolean testConnection() {
		try (Connection conn = getConnection()) {
			return conn.isValid(2);
		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
	}

	public int executeUpdate(String sql) throws SQLException {
		try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
			return stmt.executeUpdate(sql);
		}
	}

	public List<Map<String, Object>> executeQuery(String sql) throws SQLException {
		List<Map<String, Object>> results = new ArrayList<>();
		try (Connection conn = getConnection();
				Statement stmt = conn.createStatement();
				ResultSet rs = stmt.executeQuery(sql)) {

			ResultSetMetaData meta = rs.getMetaData();
			int columnCount = meta.getColumnCount();

			while (rs.next()) {
				Map<String, Object> row = new HashMap<>();
				for (int i = 1; i <= columnCount; i++) {
					row.put(meta.getColumnLabel(i), rs.getObject(i));
				}
				results.add(row);
			}
		}
		return results;
	}
}
