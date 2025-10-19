package com.ai.driven.cybersecurity.platform.notify;

import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;

public class SMSNotifier {

	// --- CONFIGURATION ---
	public static final String ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID";
	public static final String AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN";
	public static final String FROM_NUMBER = "+1234567890"; // Your Twilio number

	static {
		Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
	}

	// Static method to send SMS
	public static void sendSMS(String messageBody, String toNumber) {
		try {
			Message message = Message.creator(new com.twilio.type.PhoneNumber(toNumber),
					new com.twilio.type.PhoneNumber(FROM_NUMBER), messageBody).create();
			System.out.println("SMS sent successfully to " + toNumber + ", SID: " + message.getSid());
		} catch (Exception e) {
			System.err.println("Error sending SMS: " + e.getMessage());
		}
	}
}
