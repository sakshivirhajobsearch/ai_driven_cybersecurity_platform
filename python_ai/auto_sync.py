# auto_sync.py
import time
from datetime import datetime
from database.ai_driven_cybersecurity_platform_local import insert_local, fetch_unsynced_local
from database.ai_driven_cybersecurity_platform_central import insert_central, fetch_central
from notifiers.sms_notifier import send_sms
from notifiers.email_notifier import send_email
import pymysql

# --- CONFIGURATION ---
SYNC_INTERVAL_SECONDS = 3600  # hourly
SECURITY_EMAIL = "security@company.com"
SECURITY_PHONE = "+911234567890"

# Database credentials
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "ai_driven_cybersecurity_platform_local"
}

CENTRAL_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "ai_driven_cybersecurity_platform_central"
}

def connect_db(config):
    return pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

def sync_table(table_name, local_conn, central_conn):
    """
    Sync one table from Local -> Central
    """
    with local_conn.cursor() as lcur, central_conn.cursor() as ccur:
        lcur.execute(f"SELECT * FROM {table_name} WHERE synced = FALSE")
        rows = lcur.fetchall()
        synced_count = 0
        for row in rows:
            columns = ", ".join(row.keys())
            placeholders = ", ".join(["%s"] * len(row))
            update_keys = ", ".join([f"{k}=VALUES({k})" for k in row.keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) " \
                  f"ON DUPLICATE KEY UPDATE {update_keys}"
            try:
                ccur.execute(sql, list(row.values()))
                synced_count += 1
            except Exception as e:
                print(f"[{table_name}] Error inserting row: {e}")
            # Mark local as synced
            update_sql = f"UPDATE {table_name} SET synced = TRUE WHERE {list(row.keys())[0]} = %s"
            lcur.execute(update_sql, (row[list(row.keys())[0]],))
        return synced_count

def log_sync_status(local_conn, table_name, count):
    with local_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sync_status (table_name, last_synced, status) VALUES (%s, %s, %s)",
            (table_name, datetime.now(), f"Synced {count} records")
        )
    local_conn.commit()

def main():
    print("Starting Python auto-sync service...")
    while True:
        local_conn = connect_db(LOCAL_DB_CONFIG)
        central_conn = connect_db(CENTRAL_DB_CONFIG)
        tables = ["local_threats", "ai_model_logs", "alerts", "remediation_actions",
                  "system_health", "threat_events", "users"]
        total_synced = 0
        for table in tables:
            count = sync_table(table, local_conn, central_conn)
            log_sync_status(local_conn, table, count)
            total_synced += count
        # Commit all
        central_conn.commit()
        local_conn.commit()

        # Send notification
        message = f"[{datetime.now()}] Auto-sync completed. Total records synced: {total_synced}"
        send_sms(message, SECURITY_PHONE)
        send_email("AI Cybersecurity Sync Summary", message, SECURITY_EMAIL)

        print(message)
        local_conn.close()
        central_conn.close()
        time.sleep(SYNC_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
