-- select.sql
-- Common queries for monitoring & dashboard

-- Users
SELECT * FROM users;
SELECT COUNT(*) AS total_users FROM users;

-- Threat events
SELECT * FROM threat_events ORDER BY detected_at DESC;
SELECT severity_level, COUNT(*) AS total FROM threat_events GROUP BY severity_level;

-- High-confidence threats
SELECT * FROM threat_events WHERE ai_confidence > 0.80 ORDER BY ai_confidence DESC;

-- Unhandled critical threats
SELECT * FROM threat_events WHERE severity_level='Critical' AND handled=FALSE;

-- Remediation actions
SELECT ra.id, lt.threat_type, ra.action, ra.executed_at
FROM remediation_actions ra
JOIN local_threats lt ON ra.threat_id=lt.threat_id
ORDER BY ra.executed_at DESC;

-- Pending remediation actions
SELECT * FROM remediation_actions WHERE executed_at < NOW() - INTERVAL 2 HOUR AND synced=FALSE;

-- Alerts
SELECT * FROM alerts ORDER BY created_at DESC;
SELECT alert_type, COUNT(*) AS total_alerts FROM alerts GROUP BY alert_type;

-- System health
SELECT * FROM system_health ORDER BY checked_at DESC;
SELECT * FROM system_health WHERE status IN ('WARNING','ERROR');

-- AI model logs
SELECT * FROM ai_model_logs ORDER BY log_time DESC;
SELECT model_name, COUNT(*) AS total_actions FROM ai_model_logs GROUP BY model_name;

-- Sync status
SELECT * FROM sync_status ORDER BY last_synced DESC;
SELECT COUNT(*) AS unsynced_events FROM threat_events WHERE synced=FALSE;
SELECT COUNT(*) AS unsynced_actions FROM remediation_actions WHERE synced=FALSE;
SELECT COUNT(*) AS unsynced_alerts FROM alerts WHERE synced=FALSE;

USE soc_ai_platform;

-- Get recent threats
SELECT * FROM threat_events ORDER BY detected_at DESC LIMIT 10;

-- Get latest alerts
SELECT * FROM alerts ORDER BY created_at DESC LIMIT 10;

-- Get recent remediation actions
SELECT * FROM remediation_actions ORDER BY performed_at DESC LIMIT 10;

-- Get system health snapshot
SELECT * FROM system_health ORDER BY checked_at DESC LIMIT 5;


USE ai_driven_cybersecurity_platform_local;

SELECT * FROM ai_model_logs;                                
SELECT * FROM alerts;
SELECT * FROM local_threats;
SELECT * FROM remediation_actions;
SELECT * FROM sync_status;
SELECT * FROM system_health;
SELECT * FROM threat_events;
SELECT * FROM users;

USE ai_driven_cybersecurity_platform_central;

SELECT * FROM ai_model_logs;                                
SELECT * FROM alerts;
SELECT * FROM local_threats;
SELECT * FROM remediation_actions;
SELECT * FROM sync_status;
SELECT * FROM system_health;
SELECT * FROM threat_events;
SELECT * FROM users;

USE soc_ai_platform;

SELECT * FROM threats;
SELECT * FROM alerts;
