package com.ai.driven.cybersecurity.platform.gui;

import java.util.Timer;
import java.util.TimerTask;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;

public class ChartRefresher {
	private Timer timer;
	private Dashboard dashboard;
	private DatabaseManager db;

	public ChartRefresher(Dashboard dashboard, DatabaseManager db) {
		this.dashboard = dashboard;
		this.db = db;
		timer = new Timer(true);
	}

	public void startHourly() {
		timer.scheduleAtFixedRate(new TimerTask() {
			public void run() {
				try {
					dashboard.refreshCharts();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}, 0, 60 * 60 * 1000); // every 1 hour
	}

	public void stop() {
		timer.cancel();
	}
}
