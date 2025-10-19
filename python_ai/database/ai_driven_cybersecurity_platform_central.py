import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from config import MYSQL_CENTRAL, TABLE_EVENTS

def insert_central_event(source, threat, raw_data):
    conn = mysql.connector.connect(**MYSQL_CENTRAL)
    cursor = conn.cursor()
    query = f"INSERT INTO {TABLE_EVENTS} (source, threat_type, raw_data) VALUES (%s, %s, %s)"
    cursor.execute(query, (source, threat, raw_data))
    conn.commit()
    cursor.close()
    conn.close()
