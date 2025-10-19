import mysql.connector

LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'ai_driven_cybersecurity_platform_local'
}

conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
cursor = conn.cursor()
cursor.execute("SELECT * FROM events;")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
