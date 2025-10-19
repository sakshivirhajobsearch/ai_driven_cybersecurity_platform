package com.ai.driven.cybersecurity.platform;

import java.time.LocalDateTime;

import com.ai.driven.cybersecurity.platform.api.InferenceClient;
import com.ai.driven.cybersecurity.platform.config.ConfigLoader;
import com.ai.driven.cybersecurity.platform.db.CentralDBSync;
import com.ai.driven.cybersecurity.platform.db.DatabaseManager;
import com.ai.driven.cybersecurity.platform.gui.ChartRefresher;
import com.ai.driven.cybersecurity.platform.gui.Dashboard;
import com.ai.driven.cybersecurity.platform.notify.EmailNotifier;
import com.ai.driven.cybersecurity.platform.notify.SMSNotifier;

public class AIDrivenCybersecurityPlatform {

	public static void main(String[] args) {
		try {
			ConfigLoader config = ConfigLoader.getInstance();

			DatabaseManager localDb = new DatabaseManager(config.getDbUrl(), config.getDbUsername(),
					config.getDbPassword());

			DatabaseManager centralDb = new DatabaseManager(config.getCentralDbUrl(), config.getCentralDbUsername(),
					config.getCentralDbPassword());

			InferenceClient aiClient = new InferenceClient();
			EmailNotifier emailNotifier = new EmailNotifier();
			SMSNotifier smsNotifier = new SMSNotifier();

			// Start database sync
			CentralDBSync sync = new CentralDBSync(localDb, centralDb) {
				@Override
				public void onSyncComplete(int recordsSynced) {
					String message = "Cybersecurity Platform Sync Completed.\n" + "Total records synced: "
							+ recordsSynced + "\n" + "Time: " + LocalDateTime.now();

					smsNotifier.sendSMS(message, config.getTwilioToNumber());
					emailNotifier.sendEmail("Sync Summary", message, config.getSecurityEmail());

					System.out.println(message);
				}
			};
			sync.startSync(60_000);

			// Launch dashboard
			Dashboard dashboard = Dashboard.launchDashboard(localDb);

			// Refresh charts hourly
			ChartRefresher refresher = new ChartRefresher(dashboard, localDb);
			refresher.startHourly();

			System.out.println("AI-Driven Cybersecurity Platform started successfully.");

			// Example: send dummy event to AI
			String sampleJson = "{\"event_type\":\"phishing\",\"description\":\"Suspicious email detected\"}";
			String aiResponse = aiClient.sendThreatData(sampleJson);
			System.out.println("AI Prediction Response: " + aiResponse);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
