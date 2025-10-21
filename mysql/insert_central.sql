-- insert_central.sql
USE ai_driven_cybersecurity_platform_central;

INSERT INTO central_threats (threat_id, threat_type, severity_level, source_ip, target_system, detected_at, handled)
VALUES
(1,'Phishing', 'High', '192.168.1.10', 'Server1', NOW(), FALSE),
(2,'Malware', 'Medium', '192.168.1.20', 'Server2', NOW(), FALSE),
(3,'Ransomware', 'Critical', '192.168.1.30', 'Server3', NOW(), FALSE),
(4,'Insider Threat', 'Medium', '192.168.1.40', 'Server4', NOW(), FALSE),
(5,'DDoS', 'High', '192.168.1.50', 'Server5', NOW(), FALSE),
(6,'SQL Injection', 'High', '192.168.1.60', 'Server6', NOW(), FALSE),
(7,'Phishing', 'Medium', '192.168.1.70', 'Server7', NOW(), FALSE),
(8,'Malware', 'Low', '192.168.1.80', 'Server8', NOW(), FALSE),
(9,'Ransomware', 'Critical', '192.168.1.90', 'Server9', NOW(), FALSE),
(10,'Zero-Day', 'Critical', '192.168.1.100', 'Server10', NOW(), FALSE);

INSERT INTO users (id, username, email, role, created_at)
VALUES
(1,'alice','alice@example.com','Admin', NOW()),
(2,'bob','bob@example.com','Analyst', NOW()),
(3,'charlie','charlie@example.com','Operator', NOW()),
(4,'david','david@example.com','Analyst', NOW()),
(5,'eve','eve@example.com','Admin', NOW()),
(6,'frank','frank@example.com','Operator', NOW()),
(7,'grace','grace@example.com','Analyst', NOW()),
(8,'heidi','heidi@example.com','Operator', NOW()),
(9,'ivan','ivan@example.com','Admin', NOW()),
(10,'judy','judy@example.com','Analyst', NOW());

INSERT INTO ai_model_logs (id, model_name, action_taken, log_time)
VALUES
(1,'ThreatClassifierV1','Analyzed sample event', NOW()),
(2,'ThreatClassifierV1','Predicted Malware risk', NOW()),
(3,'ThreatClassifierV2','Detected Phishing pattern', NOW()),
(4,'ThreatClassifierV1','Ransomware score calculated', NOW()),
(5,'ThreatClassifierV2','Insider threat risk assessed', NOW()),
(6,'ThreatClassifierV1','DDoS threat probability computed', NOW()),
(7,'ThreatClassifierV2','SQL Injection detected', NOW()),
(8,'ThreatClassifierV1','Phishing alert logged', NOW()),
(9,'ThreatClassifierV2','Zero-Day vulnerability flagged', NOW()),
(10,'ThreatClassifierV1','System anomaly detected', NOW());

INSERT INTO alerts (id, alert_type, message, created_at, severity)
VALUES
(1,'Email','Phishing detected for user alice', NOW(),'High'),
(2,'SMS','Critical threat detected on Server3', NOW(),'High'),
(3,'Email','Malware detected on Server2', NOW(),'Medium'),
(4,'SMS','Ransomware detected on Server9', NOW(),'High'),
(5,'Email','SQL Injection attack on Server6', NOW(),'High'),
(6,'SMS','DDoS attack on Server5', NOW(),'High'),
(7,'Email','Insider threat on Server4', NOW(),'Medium'),
(8,'SMS','Zero-Day vulnerability detected on Server10', NOW(),'High'),
(9,'Email','Firewall anomaly detected', NOW(),'Medium'),
(10,'SMS','SIEM system warning', NOW(),'Low');

INSERT INTO remediation_actions (id, threat_id, action, executed_at)
VALUES
(1,1,'Quarantine user account', NOW()),
(2,2,'Block malicious IP', NOW()),
(3,3,'Isolate infected server', NOW()),
(4,4,'Revoke user privileges', NOW()),
(5,5,'Activate DDoS mitigation', NOW()),
(6,6,'Patch vulnerable application', NOW()),
(7,7,'Reset user password', NOW()),
(8,8,'Run malware scan', NOW()),
(9,9,'Apply ransomware recovery plan', NOW()),
(10,10,'Deploy zero-day mitigation', NOW());

INSERT INTO system_health (id, component, status, checked_at)
VALUES
(1,'Firewall','OK', NOW()),
(2,'SIEM','WARNING', NOW()),
(3,'Endpoint Protection','OK', NOW()),
(4,'Email Gateway','OK', NOW()),
(5,'Network Switch','OK', NOW()),
(6,'Database Server','OK', NOW()),
(7,'Web Server','WARNING', NOW()),
(8,'VPN Gateway','OK', NOW()),
(9,'Intrusion Detection','ERROR', NOW()),
(10,'Backup System','OK', NOW());

INSERT INTO threat_events (id, threat_type, description, detected_at, severity_level, ai_confidence, source_ip, target_system)
VALUES
(1,'Phishing','Email phishing attempt', NOW(),'High',0.85,'192.168.1.10','Server1'),
(2,'Malware','Malware detected on endpoint', NOW(),'Medium',0.78,'192.168.1.20','Server2'),
(3,'Ransomware','Encrypted critical files', NOW(),'Critical',0.95,'192.168.1.30','Server3'),
(4,'Insider Threat','Unauthorized access detected', NOW(),'Medium',0.65,'192.168.1.40','Server4'),
(5,'DDoS','High traffic from multiple IPs', NOW(),'High',0.90,'192.168.1.50','Server5'),
(6,'SQL Injection','SQL injection attempt blocked', NOW(),'High',0.88,'192.168.1.60','Server6'),
(7,'Phishing','Suspicious login email', NOW(),'Medium',0.72,'192.168.1.70','Server7'),
(8,'Malware','Trojan detected in system', NOW(),'Low',0.60,'192.168.1.80','Server8'),
(9,'Ransomware','Ransom note found', NOW(),'Critical',0.93,'192.168.1.90','Server9'),
(10,'Zero-Day','Unknown exploit attempted', NOW(),'Critical',0.99,'192.168.1.100','Server10');
