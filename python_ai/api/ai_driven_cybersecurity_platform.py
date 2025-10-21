"""
AI-Driven Cybersecurity Platform - Inference API (Patched)
----------------------------------------------------------
Handles AI-based threat inference with robust error handling.
Always returns JSON to the client, avoiding 500 errors.
"""

from flask import Flask, request, jsonify
from joblib import load
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import os
import numpy as np
import sys
import traceback

# ==========================================================
# Fix imports dynamically for features module
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    from features.feature_extractor import extract_features
except ImportError as e:
    print(f"❌ Failed to import feature_extractor: {e}")
    sys.exit(1)

# ==========================================================
# Flask App Initialization
# ==========================================================
app = Flask(__name__)

# ==========================================================
# Model and Scaler Loading
# ==========================================================
MODEL = None
SCALER = None

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "features", "scaler.pkl")

try:
    if os.path.exists(MODEL_PATH):
        MODEL = load(MODEL_PATH)
        print("✅ Model loaded successfully.")
    else:
        print("⚠️ Model file not found:", MODEL_PATH)

    if os.path.exists(SCALER_PATH):
        SCALER = load(SCALER_PATH)
        print("✅ Scaler loaded successfully.")
    else:
        print("⚠️ Scaler file not found:", SCALER_PATH)

except Exception as e:
    print("⚠️ Warning: Failed to load model/scaler:", e)
    traceback.print_exc()

# ==========================================================
# Database Configuration
# ==========================================================
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "admin"),
    "database": os.environ.get("DB_NAME", "soc_ai_platform"),
}

# ==========================================================
# Database Helper Function
# ==========================================================
def insert_event_db(raw_event, normalized, category, risk_score):
    """Insert a new AI-detected threat event into MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = (
            "INSERT INTO threat_events "
            "(event_name, threat_type, severity, source_ip, destination_ip, "
            "detected_at, ai_confidence, risk_score, status, synced) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )

        event_name = normalized.get("event_name", "Unknown Event")
        threat_type = normalized.get("threat_type", "External")
        severity = normalized.get("severity", "Medium")
        src_ip = normalized.get("source_ip", "0.0.0.0")
        dst_ip = normalized.get("destination_ip", "0.0.0.0")
        detected_at = datetime.utcnow()
        ai_conf = float(normalized.get("ai_confidence", risk_score))
        risk_score = float(risk_score)
        status = "Detected"
        synced = 0

        cursor.execute(
            sql,
            (
                event_name,
                threat_type,
                severity,
                src_ip,
                dst_ip,
                detected_at,
                ai_conf,
                risk_score,
                status,
                synced,
            ),
        )

        conn.commit()
        event_id = cursor.lastrowid
        cursor.close()
        conn.close()

        print(f"✅ Threat event inserted with ID: {event_id}")
        return event_id

    except Error as e:
        print("❌ DB Error:", e)
        traceback.print_exc()
        return None
    except Exception as e:
        print("❌ Unknown DB Error:", e)
        traceback.print_exc()
        return None

# ==========================================================
# Inference Logic
# ==========================================================
@app.route("/infer", methods=["POST"])
def infer():
    """Main AI inference endpoint with robust error handling."""
    try:
        payload = request.get_json(force=True)
        print("📥 Payload received:", payload)

        raw_event = payload.get("raw", payload)

        # ------------------------
        # Feature extraction
        # ------------------------
        try:
            normalized = extract_features(raw_event)
            print("🔹 Normalized features:", normalized)
            feat_vector = normalized.get("feature_vector")
            print("🔹 Feature vector:", feat_vector)
        except Exception as e:
            print("❌ Feature extraction error:", e)
            traceback.print_exc()
            normalized = {}
            feat_vector = None

        risk_score = 0.0
        category = "unknown"

        # ------------------------
        # Model inference
        # ------------------------
        try:
            if MODEL is not None and feat_vector is not None:
                x = np.array(feat_vector).reshape(1, -1)
                if SCALER is not None:
                    x = SCALER.transform(x)
                if hasattr(MODEL, "predict_proba"):
                    proba = MODEL.predict_proba(x)[0]
                    best_idx = int(proba.argmax())
                    risk_score = float(proba.max() * 100)
                    category = normalized.get("category") or str(best_idx)
                else:
                    pred = MODEL.predict(x)[0]
                    risk_score = float(pred)
                    category = normalized.get("category") or "Unknown"
            else:
                print("⚠️ Model or feature vector missing, skipping inference.")
        except Exception as e:
            print("❌ Model inference error:", e)
            traceback.print_exc()

        # ------------------------
        # Insert into DB (optional)
        # ------------------------
        try:
            event_id = insert_event_db(raw_event, normalized, category, risk_score)
        except Exception as e:
            print("❌ DB insertion skipped due to error:", e)
            event_id = None

        # ------------------------
        # Return JSON response
        # ------------------------
        return jsonify(
            {
                "success": True,
                "event_id": event_id,
                "category": category,
                "risk_score": risk_score,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    except Exception as e:
        print("❌ Inference endpoint failed:", e)
        traceback.print_exc()
        return jsonify(
            {
                "success": False,
                "error": str(e),
                "category": "unknown",
                "risk_score": 0.0,
                "event_id": None,
            }
        )

# ==========================================================
# API Predict Alias
# ==========================================================
@app.route("/api/predict", methods=["POST"])
def predict_alias():
    """Alias route for dashboard compatibility."""
    return infer()

# ==========================================================
# Root Health Check
# ==========================================================
@app.route("/", methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "AI-Driven Cybersecurity API is running",
            "routes": ["/infer", "/api/predict"],
        }
    )

# ==========================================================
# Main Entry
# ==========================================================
if __name__ == "__main__":
    print("\n🚀 AI-Driven Cybersecurity Platform started successfully.")
    print("✅ Available routes:")
    print("   → /infer")
    print("   → /api/predict")
    print("   → / (health check)\n")

    app.run(host="0.0.0.0", port=5000, debug=False)
