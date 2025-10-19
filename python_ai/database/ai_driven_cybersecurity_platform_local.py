import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from config import MYSQL_LOCAL, TABLE_EVENTS

def insert_event(source, threat, raw_data):
    conn = mysql.connector.connect(**MYSQL_LOCAL)
    cursor = conn.cursor()
    query = f"INSERT INTO {TABLE_EVENTS} (source, threat_type, raw_data) VALUES (%s, %s, %s)"
    cursor.execute(query, (source, threat, raw_data))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_last_events(limit=10):
    conn = mysql.connector.connect(**MYSQL_LOCAL)
    cursor = conn.cursor()
    query = f"SELECT id, source, threat_type, timestamp FROM {TABLE_EVENTS} ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
