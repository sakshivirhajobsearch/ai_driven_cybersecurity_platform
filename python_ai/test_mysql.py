# =====================================================
# File: test_mysql.py
# Purpose: Verify connectivity and schema integrity
# =====================================================

import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def test_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"✅ Connected to MySQL Server version {db_Info}")
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("📋 Tables available:", [t[0] for t in tables])
            cursor.close()
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    test_mysql_connection()
