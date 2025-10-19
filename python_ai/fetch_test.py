import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'ai_driven_cybersecurity_platform_local'
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT * FROM events;")
events = cursor.fetchall()
print("Events:", events)

cursor.execute("SELECT * FROM actions;")
actions = cursor.fetchall()
print("Actions:", actions)

conn.close()
