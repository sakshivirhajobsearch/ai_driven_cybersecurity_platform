package com.ai.driven.cybersecurity.platform.gui;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;

public class Dashboard {

	private DatabaseManager db;

	private Dashboard(DatabaseManager db) {
		this.db = db;
	}

	// Launch GUI and return the instance
	public static Dashboard launchDashboard(DatabaseManager db) {
		Dashboard dashboard = new Dashboard(db);
		// TODO: Initialize GUI components
		System.out.println("Dashboard launched");
		return dashboard;
	}

	public void refreshCharts() {
		// TODO: Refresh charts using db data
		System.out.println("Charts refreshed at " + java.time.LocalDateTime.now());
	}
}
