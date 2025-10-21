# python/api/app.py
"""
Lightweight Flask inference API for threat scoring.
Safe DB writes and defensive handling for missing fields.
"""
from flask import Flask, request, jsonify
from joblib import load
import json
import mysql.connector
from datetime import datetime
from features.feature_extractor import extract_features
from mysql.connector import Error
import os

app = Flask(__name__)

# Load model & scaler if present (safe)
MODEL = None
SCALER = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "../features/scaler.pkl")
try:
    if os.path.exists(MODEL_PATH):
        MODEL = load(MODEL_PATH)
    if os.path.exists(SCALER_PATH):
        SCALER = load(SCALER_PATH)
except Exception as e:
    print("Warning: could not load model/scaler:", e)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "rootpass"),
    "database": os.environ.get("DB_NAME", "ai_driven_cybersecurity_platform_local")
}

def insert_event_db(raw_event, normalized, category, risk_score):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = ("INSERT INTO threat_events "
               "(threat_type, description, severity_level, ai_confidence, source_ip, target_system, detected_at, handled, synced) "
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        threat_type = normalized.get("threat_type") if isinstance(normalized, dict) else None
        description = normalized.get("description") if isinstance(normalized, dict) else json.dumps(raw_event)[:250]
        severity = normalized.get("severity_level", None) if isinstance(normalized, dict) else None
        src_ip = normalized.get("src_ip", "") if isinstance(normalized, dict) else ""
        tgt = normalized.get("target_system", "") if isinstance(normalized, dict) else ""
        detected_at = datetime.utcnow()
        handled = False
        synced = False
        cursor.execute(sql, (threat_type, description, severity, float(risk_score), src_ip, tgt, detected_at, handled, synced))
        conn.commit()
        event_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return event_id
    except Error as e:
        print("DB error:", e)
        return None

@app.route("/infer", methods=["POST"])
def infer():
    payload = request.json or {}
    raw_event = payload.get("raw", payload)

    # Feature extraction
    normalized = extract_features(raw_event)  # should return a dict with "feature_vector" key and helpful meta
    feat_vector = normalized.get("feature_vector", None)

    risk_score = 0.0
    category = "unknown"
    # If model exists, try to predict safely
    try:
        if MODEL is not None and feat_vector is not None:
            import numpy as np
            x = np.array(feat_vector).reshape(1, -1)
            if SCALER is not None:
                x = SCALER.transform(x)
            if hasattr(MODEL, "predict_proba"):
                proba = MODEL.predict_proba(x)[0]
                best_idx = int(proba.argmax())
                risk_score = float(proba.max())
                # category map fallback
                category = normalized.get("category") or str(best_idx)
            else:
                pred = MODEL.predict(x)[0]
                risk_score = 1.0 if pred else 0.0
                category = normalized.get("category") or str(pred)
    except Exception as e:
        print("Model inference error:", e)
        risk_score = normalized.get("ai_confidence", 0.0) or 0.0
        category = normalized.get("category", "unknown")

    # Insert into DB
    event_id = insert_event_db(raw_event, normalized, category, risk_score)
    response = {"event_id": event_id, "category": category, "risk_score": risk_score}
    return jsonify(response), 200

if __name__ == "__main__":
    # Run for local dev
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
