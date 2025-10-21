package com.ai.driven.cybersecurity.platform.notify;

import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;

public class SMSNotifier {

	public static final String ACCOUNT_SID = "YOUR_REAL_TWILIO_SID";
	public static final String AUTH_TOKEN = "YOUR_REAL_TWILIO_AUTH_TOKEN";
	public static final String FROM_NUMBER = "+YOUR_TWILIO_NUMBER";

	static {
		try {
			Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
			System.out.println("✅ Twilio initialized successfully.");
		} catch (Exception e) {
			e.printStackTrace();
			System.err.println("❌ Twilio initialization failed: " + e.getMessage());
		}
	}

	public static void sendSMS(String messageBody, String toNumber) {
		try {
			Message message = Message.creator(new PhoneNumber(toNumber), new PhoneNumber(FROM_NUMBER), messageBody)
					.create();
			System.out.println("✅ SMS sent successfully to " + toNumber + ", SID: " + message.getSid());
		} catch (Exception e) {
			e.printStackTrace();
			System.err.println("❌ Error sending SMS: " + e.getMessage());
		}
	}
}
