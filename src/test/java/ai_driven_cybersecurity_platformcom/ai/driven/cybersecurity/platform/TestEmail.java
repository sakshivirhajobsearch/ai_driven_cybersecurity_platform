package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import com.ai.driven.cybersecurity.platform.notify.EmailNotifier;

public class TestEmail {
	
	public static void main(String[] args) {
		
		String toEmail = "sunayanasamanjobsearch@yahoo.com"; // Replace with a real email
		String subject = "Test Email - AI Cybersecurity Alert";
		String body = "This is a test email from AI-Driven Cybersecurity Platform.";

		EmailNotifier.sendEmail(subject, body, toEmail);
	}
}
