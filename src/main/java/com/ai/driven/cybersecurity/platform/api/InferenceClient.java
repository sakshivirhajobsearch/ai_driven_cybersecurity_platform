package com.ai.driven.cybersecurity.platform.api;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import com.ai.driven.cybersecurity.platform.config.ConfigLoader;

public class InferenceClient {

    private final String endpoint;

    public InferenceClient() {
        try {
            // Use singleton ConfigLoader instance
            ConfigLoader config = ConfigLoader.getInstance();
            this.endpoint = config.getAiApiUrl();
        } catch (Exception e) {
            throw new RuntimeException("Failed to load AI endpoint from config", e);
        }
    }

    public String sendThreatData(String jsonPayload) {
        try {
            URL url = new URL(endpoint);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            try (OutputStream os = conn.getOutputStream()) {
                os.write(jsonPayload.getBytes());
                os.flush();
            }

            try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
                return response.toString();
            }

        } catch (Exception e) {
            return "Error contacting AI: " + e.getMessage();
        }
    }
}
