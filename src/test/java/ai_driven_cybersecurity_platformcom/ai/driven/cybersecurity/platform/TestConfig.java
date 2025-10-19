package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import java.sql.Connection;

import com.ai.driven.cybersecurity.platform.config.ConfigLoader;

public class TestConfig {

	public static void main(String[] args) throws Exception {
		ConfigLoader config = ConfigLoader.getInstance();

		// Database connections
		Connection localConn = config.getLocalDbConnection();
		Connection centralConn = config.getCentralDbConnection();

		System.out.println("Local DB: " + localConn.getMetaData().getURL());
		System.out.println("Central DB: " + centralConn.getMetaData().getURL());

		// AI
		System.out.println("AI API URL: " + config.getAiApiUrl());
		System.out.println("Confidence Threshold: " + config.getAiConfidenceThreshold());

		// Twilio
		System.out.println("Twilio From: " + config.getTwilioFromNumber());
		System.out.println("Twilio To: " + config.getTwilioToNumber());

		// Dashboard
		System.out.println("Dashboard Title: " + config.getDashboardTitle());
		System.out.println("Refresh Interval: " + config.getDashboardRefreshInterval() + " seconds");
	}
}
