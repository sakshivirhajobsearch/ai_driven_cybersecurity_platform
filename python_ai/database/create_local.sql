CREATE DATABASE IF NOT EXISTS cyber_central;
USE cyber_central;

CREATE TABLE IF NOT EXISTS security_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(255),
    source_ip VARCHAR(50),
    severity VARCHAR(50),
    confidence FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
