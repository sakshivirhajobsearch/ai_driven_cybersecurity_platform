# python/ingest/connectors.py
"""
Example connectors: adapt these functions to pull logs from files, syslog, or APIs.
Two examples:
 - push_to_api(raw_event): calls the Flask inference service
 - write_to_local_db(raw_event): direct DB insert (optional)
"""
import requests
import os
from mysql.connector import connect, Error
import json

INFER_URL = os.environ.get("INFER_URL", "http://localhost:5000/infer")

def push_to_api(raw_event: dict):
    try:
        resp = requests.post(INFER_URL, json={"raw": raw_event}, timeout=10)
        return resp.json()
    except Exception as e:
        print("Error pushing to inference API:", e)
        return None

def write_to_local_db(raw_event: dict, db_config: dict):
    try:
        conn = connect(**db_config)
        cursor = conn.cursor()
        sql = ("INSERT INTO threat_events (threat_type, description, severity_level, ai_confidence, source_ip, target_system, detected_at, handled, synced) "
               "VALUES (%s,%s,%s,%s,%s,%s,NOW(),%s,%s)")
        cursor.execute(sql, (
            raw_event.get("threat_type"),
            raw_event.get("description") or raw_event.get("message"),
            raw_event.get("severity"),
            raw_event.get("ai_confidence") or raw_event.get("confidence", 0.0),
            raw_event.get("src_ip") or raw_event.get("source_ip"),
            raw_event.get("target_system") or raw_event.get("target"),
            False,
            False
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("DB write error:", e)
