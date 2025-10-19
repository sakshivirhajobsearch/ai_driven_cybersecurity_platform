package com.ai.driven.cybersecurity.platform.notify;

import java.util.Properties;

import jakarta.mail.Authenticator;
import jakarta.mail.Message;
import jakarta.mail.PasswordAuthentication;
import jakarta.mail.Session;
import jakarta.mail.Transport;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;

public class EmailNotifier {

	// --- CONFIGURATION ---
	private static final String SMTP_HOST = "smtp.yourmail.com";
	private static final String SMTP_PORT = "587"; // TLS
	private static final String SMTP_USER = "your_email@domain.com";
	private static final String SMTP_PASSWORD = "your_email_password";
	private static final String FROM_EMAIL = "your_email@domain.com";

	// Static method to send email
	public static void sendEmail(String subject, String body, String toEmail) {
		try {
			Properties props = new Properties();
			props.put("mail.smtp.auth", "true");
			props.put("mail.smtp.starttls.enable", "true");
			props.put("mail.smtp.host", SMTP_HOST);
			props.put("mail.smtp.port", SMTP_PORT);

			Session session = Session.getInstance(props, new Authenticator() {
				protected PasswordAuthentication getPasswordAuthentication() {
					return new PasswordAuthentication(SMTP_USER, SMTP_PASSWORD);
				}
			});

			Message message = new MimeMessage(session);
			message.setFrom(new InternetAddress(FROM_EMAIL));
			message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(toEmail));
			message.setSubject(subject);
			message.setText(body);

			Transport.send(message);
			System.out.println("Email sent successfully to " + toEmail);
		} catch (Exception e) {
			System.err.println("Error sending email: " + e.getMessage());
		}
	}
}
