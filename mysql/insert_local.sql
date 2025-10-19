-- =====================================================
-- File: insert.sql
-- Purpose: Insert dummy/test data
-- =====================================================

USE ai_driven_cybersecurity_platform_local;

-- -----------------------
-- Local threats
-- -----------------------
INSERT INTO local_threats (threat_type, severity_level, source_ip, target_system, handled)
VALUES
('Phishing', 'High', '192.168.1.10', 'Server1', FALSE),
('Malware', 'Medium', '192.168.1.20', 'Server2', FALSE),
('Ransomware', 'Critical', '192.168.1.30', 'Server3', FALSE),
('Insider Threat', 'Medium', '192.168.1.40', 'Server4', FALSE),
('DDoS', 'High', '192.168.1.50', 'Server5', FALSE),
('SQL Injection', 'High', '192.168.1.60', 'Server6', FALSE),
('Phishing', 'Medium', '192.168.1.70', 'Server7', FALSE),
('Malware', 'Low', '192.168.1.80', 'Server8', FALSE),
('Ransomware', 'Critical', '192.168.1.90', 'Server9', FALSE),
('Zero-Day', 'Critical', '192.168.1.100', 'Server10', FALSE);

-- -----------------------
-- Users
-- -----------------------
INSERT INTO users (username, email, role)
VALUES
('alice','alice@example.com','Admin'),
('bob','bob@example.com','Analyst'),
('charlie','charlie@example.com','Operator'),
('david','david@example.com','Analyst'),
('eve','eve@example.com','Admin'),
('frank','frank@example.com','Operator'),
('grace','grace@example.com','Analyst'),
('heidi','heidi@example.com','Operator'),
('ivan','ivan@example.com','Admin'),
('judy','judy@example.com','Analyst');

-- -----------------------
-- AI model logs
-- -----------------------
INSERT INTO ai_model_logs (model_name, action_taken)
VALUES
('ThreatClassifierV1','Analyzed sample event'),
('ThreatClassifierV1','Predicted Malware risk'),
('ThreatClassifierV2','Detected Phishing pattern'),
('ThreatClassifierV1','Ransomware score calculated'),
('ThreatClassifierV2','Insider threat risk assessed'),
('ThreatClassifierV1','DDoS threat probability computed'),
('ThreatClassifierV2','SQL Injection detected'),
('ThreatClassifierV1','Phishing alert logged'),
('ThreatClassifierV2','Zero-Day vulnerability flagged'),
('ThreatClassifierV1','System anomaly detected');

-- -----------------------
-- Alerts
-- -----------------------
INSERT INTO alerts (alert_type, message)
VALUES
('Email','Phishing detected for user alice'),
('SMS','Critical threat detected on Server3'),
('Email','Malware detected on Server2'),
('SMS','Ransomware detected on Server9'),
('Email','SQL Injection attack on Server6'),
('SMS','DDoS attack on Server5'),
('Email','Insider threat on Server4'),
('SMS','Zero-Day vulnerability detected on Server10'),
('Email','Firewall anomaly detected'),
('SMS','SIEM system warning');

-- -----------------------
-- Remediation actions
-- -----------------------
INSERT INTO remediation_actions (threat_id, action)
VALUES
(1,'Quarantine user account'),
(2,'Block malicious IP'),
(3,'Isolate infected server'),
(4,'Revoke user privileges'),
(5,'Activate DDoS mitigation'),
(6,'Patch vulnerable application'),
(7,'Reset user password'),
(8,'Run malware scan'),
(9,'Apply ransomware recovery plan'),
(10,'Deploy zero-day mitigation');

-- -----------------------
-- System health
-- -----------------------
INSERT INTO system_health (component, status)
VALUES
('Firewall','OK'),
('SIEM','WARNING'),
('Endpoint Protection','OK'),
('Email Gateway','OK'),
('Network Switch','OK'),
('Database Server','OK'),
('Web Server','WARNING'),
('VPN Gateway','OK'),
('Intrusion Detection','ERROR'),
('Backup System','OK');

-- -----------------------
-- Threat events
-- -----------------------
INSERT INTO threat_events (threat_type, description, severity_level, ai_confidence, source_ip, target_system)
VALUES
('Phishing','Email phishing attempt','High',0.85,'192.168.1.10','Server1'),
('Malware','Malware detected on endpoint','Medium',0.78,'192.168.1.20','Server2'),
('Ransomware','Encrypted critical files','Critical',0.95,'192.168.1.30','Server3'),
('Insider Threat','Unauthorized access detected','Medium',0.65,'192.168.1.40','Server4'),
('DDoS','High traffic from multiple IPs','High',0.90,'192.168.1.50','Server5'),
('SQL Injection','SQL injection attempt blocked','High',0.88,'192.168.1.60','Server6'),
('Phishing','Suspicious login email','Medium',0.72,'192.168.1.70','Server7'),
('Malware','Trojan detected in system','Low',0.60,'192.168.1.80','Server8'),
('Ransomware','Ransom note found','Critical',0.93,'192.168.1.90','Server9'),
('Zero-Day','Unknown exploit attempted','Critical',0.99,'192.168.1.100','Server10');
