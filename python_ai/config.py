import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "cyber_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
TABLE_EVENTS = "threat_events"

THREAT_CLASSES = ["benign", "phishing", "malware", "ddos", "insider"]

MYSQL_LOCAL = {
    "host": "localhost",
    "user": "ai_user",
    "password": "StrongPassword123",
    "database": "ai_driven_cybersecurity_local",
    "auth_plugin": "mysql_native_password"
}

MYSQL_CENTRAL = {
    "host": "localhost",
    "user": "ai_user",
    "password": "StrongPassword123",
    "database": "ai_driven_cybersecurity_central",
    "auth_plugin": "mysql_native_password"
}
