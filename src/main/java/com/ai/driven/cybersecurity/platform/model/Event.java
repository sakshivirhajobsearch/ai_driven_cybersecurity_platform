package com.ai.driven.cybersecurity.platform.model;

import java.time.LocalDateTime;

public class Event {

	private long id;
	private LocalDateTime eventTime;
	private String source;
	private String category;
	private double riskScore;
	private String rawJson;

	public Event() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Event(long id, LocalDateTime eventTime, String source, String category, double riskScore, String rawJson) {
		super();
		this.id = id;
		this.eventTime = eventTime;
		this.source = source;
		this.category = category;
		this.riskScore = riskScore;
		this.rawJson = rawJson;
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public LocalDateTime getEventTime() {
		return eventTime;
	}

	public void setEventTime(LocalDateTime eventTime) {
		this.eventTime = eventTime;
	}

	public String getSource() {
		return source;
	}

	public void setSource(String source) {
		this.source = source;
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public double getRiskScore() {
		return riskScore;
	}

	public void setRiskScore(double riskScore) {
		this.riskScore = riskScore;
	}

	public String getRawJson() {
		return rawJson;
	}

	public void setRawJson(String rawJson) {
		this.rawJson = rawJson;
	}

}
