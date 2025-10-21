# =====================================================
# File: fetch_test.py
# Purpose: Test retrieval of data from SOC AI MySQL database
# =====================================================

import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def fetch_and_display():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor(dictionary=True)

    print("\n=== Threat Events ===")
    cursor.execute("SELECT * FROM threat_events ORDER BY detected_at DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(row)

    print("\n=== Alerts ===")
    cursor.execute("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(row)

    print("\n=== System Health ===")
    cursor.execute("SELECT * FROM system_health ORDER BY checked_at DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Running fetch_test.py to validate database data...")
    fetch_and_display()
