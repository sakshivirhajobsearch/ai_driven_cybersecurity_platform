package com.ai.driven.cybersecurity.platform.config;

import java.io.FileInputStream;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/**
 * Centralized configuration loader for all app components. Reads from
 * src/main/resources/application.properties and provides DB connections, AI
 * settings, Twilio configs, and dashboard metadata.
 */
public class ConfigLoader {

	private static ConfigLoader instance;
	private Properties props;

	private ConfigLoader() {
		props = new Properties();
		try (FileInputStream fis = new FileInputStream("src/main/resources/application.properties")) {
			props.load(fis);
		} catch (IOException e) {
			System.err.println("❌ Failed to load configuration file: " + e.getMessage());
		}

		try {
			// Load MySQL driver
			Class.forName("com.mysql.cj.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			System.err.println("❌ MySQL Driver not found! Make sure mysql-connector-j is in classpath.");
		}
	}

	public static synchronized ConfigLoader getInstance() {
		if (instance == null) {
			instance = new ConfigLoader();
		}
		return instance;
	}

	// ---------------------- Database ----------------------

	public String getDbUrl() {
		return props.getProperty("db.url");
	}

	public String getDbUsername() {
		return props.getProperty("db.username");
	}

	public String getDbPassword() {
		return props.getProperty("db.password");
	}

	public String getCentralDbUrl() {
		return props.getProperty("db.central.url");
	}

	public String getCentralDbUsername() {
		return props.getProperty("db.central.username");
	}

	public String getCentralDbPassword() {
		return props.getProperty("db.central.password");
	}

	public Connection getLocalDbConnection() throws SQLException {
		return DriverManager.getConnection(getDbUrl(), getDbUsername(), getDbPassword());
	}

	public Connection getCentralDbConnection() throws SQLException {
		return DriverManager.getConnection(getCentralDbUrl(), getCentralDbUsername(), getCentralDbPassword());
	}

	// ---------------------- AI ----------------------

	public String getAiApiUrl() {
		return props.getProperty("ai.api.url");
	}

	public double getAiConfidenceThreshold() {
		return Double.parseDouble(props.getProperty("ai.confidence.threshold", "0.85"));
	}

	// ---------------------- Twilio ----------------------

	public String getTwilioAccountSid() {
		return props.getProperty("twilio.account.sid");
	}

	public String getTwilioAuthToken() {
		return props.getProperty("twilio.auth.token");
	}

	public String getTwilioFromNumber() {
		return props.getProperty("twilio.from.number");
	}

	public String getTwilioToNumber() {
		return props.getProperty("twilio.to.number");
	}

	// ---------------------- Dashboard ----------------------

	public String getDashboardTitle() {
		return props.getProperty("dashboard.title", "AI-Driven Cybersecurity Dashboard");
	}

	public int getDashboardRefreshInterval() {
		return Integer.parseInt(props.getProperty("dashboard.refresh.interval.seconds", "60"));
	}

	// ---------------------- Generic Getter ----------------------

	public String get(String key) {
		return props.getProperty(key);
	}

	// ---------------------- Security Contact ----------------------

	public String getSecurityEmail() {
		return props.getProperty("security.email", "security@company.com");
	}

	public String getSecuritySms() {
		return props.getProperty("security.sms", "+911234567890");
	}

}
