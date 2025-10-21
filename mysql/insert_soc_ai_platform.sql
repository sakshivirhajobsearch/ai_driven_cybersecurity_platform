USE soc_ai_platform;

INSERT INTO threat_events (event_name, threat_type, severity, source_ip, destination_ip, ai_confidence, risk_score, status)
VALUES
('Phishing Attempt', 'External', 'High', '192.168.1.10', '10.0.0.5', 0.91, 87.5, 'Detected'),
('Malware Infection', 'Internal', 'Medium', '192.168.1.22', '10.0.0.9', 0.76, 62.3, 'Under Review'),
('Unauthorized Access', 'Internal', 'High', '192.168.1.55', '10.0.0.11', 0.88, 79.4, 'Detected'),
('DDoS Attack', 'External', 'Critical', '203.0.113.5', '10.0.0.2', 0.95, 91.0, 'Blocked');

INSERT INTO alerts (alert_message, alert_type, threat_id)
VALUES
('Detected high-risk phishing attempt.', 'Network', 1),
('Detected medium-level malware infection.', 'Endpoint', 2),
('Unauthorized login attempt detected.', 'Access', 3),
('High volume of incoming traffic blocked.', 'Network', 4);

INSERT INTO system_health (cpu_usage, memory_usage, disk_usage, network_latency_ms)
VALUES
(23.5, 45.2, 62.7, 10.3),
(30.1, 50.8, 65.9, 12.1),
(28.3, 47.6, 63.4, 9.8);

INSERT INTO remediation_actions (threat_id, action_taken, performed_by, result)
VALUES
(1, 'Phishing email quarantined and sender blocked.', 'SOC Analyst', 'Success'),
(2, 'Malware process terminated and files quarantined.', 'EDR Agent', 'Success'),
(3, 'User account locked for review.', 'IAM System', 'Pending'),
(4, 'DDoS source IPs blackholed via firewall.', 'Network Team', 'Success');
