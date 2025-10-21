import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root")
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS soc_ai_platform;")
print("✅ Database 'soc_ai_platform' created or already exists.")
conn.close()
