-- create.sql
-- Create databases and tables for AI Cybersecurity Platform (local + central)

CREATE DATABASE IF NOT EXISTS ai_driven_cybersecurity_platform_local;
USE ai_driven_cybersecurity_platform_local;

CREATE TABLE IF NOT EXISTS local_threats (
    threat_id INT AUTO_INCREMENT PRIMARY KEY,
    threat_type VARCHAR(50),
    severity_level VARCHAR(20),
    source_ip VARCHAR(50),
    target_system VARCHAR(50),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    handled BOOLEAN DEFAULT FALSE,
    synced BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ai_model_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100),
    action_taken VARCHAR(255),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(50),
    message VARCHAR(255),
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS remediation_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    threat_id INT,
    action VARCHAR(255),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (threat_id) REFERENCES local_threats(threat_id)
);

CREATE TABLE IF NOT EXISTS sync_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50),
    last_synced TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS system_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    component VARCHAR(50),
    status VARCHAR(20),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS threat_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    threat_type VARCHAR(50),
    description VARCHAR(255),
    severity_level VARCHAR(20),
    ai_confidence FLOAT DEFAULT 0.0,
    source_ip VARCHAR(50),
    target_system VARCHAR(50),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    handled BOOLEAN DEFAULT FALSE,
    synced BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    role VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced BOOLEAN DEFAULT FALSE
);

-- Central DB
CREATE DATABASE IF NOT EXISTS ai_driven_cybersecurity_platform_central;
USE ai_driven_cybersecurity_platform_central;

CREATE TABLE IF NOT EXISTS central_threats (
    threat_id INT PRIMARY KEY,
    threat_type VARCHAR(50),
    severity_level VARCHAR(20),
    source_ip VARCHAR(50),
    target_system VARCHAR(50),
    detected_at TIMESTAMP,
    handled BOOLEAN
);

CREATE TABLE IF NOT EXISTS ai_model_logs LIKE ai_driven_cybersecurity_platform_local.ai_model_logs;
CREATE TABLE IF NOT EXISTS alerts LIKE ai_driven_cybersecurity_platform_local.alerts;
CREATE TABLE IF NOT EXISTS remediation_actions LIKE ai_driven_cybersecurity_platform_local.remediation_actions;
CREATE TABLE IF NOT EXISTS sync_status LIKE ai_driven_cybersecurity_platform_local.sync_status;
CREATE TABLE IF NOT EXISTS system_health LIKE ai_driven_cybersecurity_platform_local.system_health;
CREATE TABLE IF NOT EXISTS threat_events LIKE ai_driven_cybersecurity_platform_local.threat_events;
CREATE TABLE IF NOT EXISTS users LIKE ai_driven_cybersecurity_platform_local.users;

-- Add unique constraints to avoid accidental dup indices on central
ALTER TABLE ai_model_logs ADD UNIQUE (id);
ALTER TABLE alerts ADD UNIQUE (id);
ALTER TABLE remediation_actions ADD UNIQUE (id);
ALTER TABLE system_health ADD UNIQUE (id);
ALTER TABLE threat_events ADD UNIQUE (id);
ALTER TABLE users ADD UNIQUE (id);
