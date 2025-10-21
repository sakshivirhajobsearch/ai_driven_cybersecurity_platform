# =====================================================
# File: auto_sync.py
# Purpose: Periodic sync between local and central MySQL
# =====================================================

import time
import mysql.connector
from datetime import datetime
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, SYNC_INTERVAL_SECONDS, LOG_FILE

def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def sync_table(cursor, table_name):
    cursor.execute(f"UPDATE {table_name} SET synced=TRUE WHERE synced=FALSE;")
    log(f"✅ Synced new entries for table: {table_name}")

def run_sync_cycle():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        sync_table(cursor, "threat_events")
        sync_table(cursor, "remediation_actions")
        sync_table(cursor, "alerts")

        conn.commit()
        log("🔄 Sync completed successfully.")
    except Exception as e:
        log(f"❌ Sync error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    log("=== Starting Auto Sync Service ===")
    while True:
        run_sync_cycle()
        time.sleep(SYNC_INTERVAL_SECONDS)
