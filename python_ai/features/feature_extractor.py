"""
Feature Extractor for AI-Driven Cybersecurity Platform
------------------------------------------------------
Normalizes incoming raw events and prepares feature vectors for AI inference.
Extracted features are designed for use with the trained model and scaler.
"""

import re
import hashlib
import numpy as np
from datetime import datetime


# ==========================================================
# Utility Functions
# ==========================================================
def ip_to_int(ip_address: str) -> int:
    """Convert IP string to an integer (simple numeric encoding)."""
    try:
        parts = [int(p) for p in ip_address.split('.')]
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
    except Exception:
        return 0


def normalize_text(text: str) -> str:
    """Normalize text safely."""
    if not text:
        return ""
    text = str(text).strip().lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


def hash_to_number(value: str) -> float:
    """Stable hash-based numeric encoding."""
    if not value:
        return 0.0
    h = int(hashlib.sha256(value.encode()).hexdigest(), 16)
    return float(h % 1_000_000) / 1_000_000.0


# ==========================================================
# Main Feature Extraction Logic
# ==========================================================
def extract_features(raw_event: dict):
    """
    Extracts structured and numerical features for AI inference.
    Input:
        raw_event (dict): Raw event data (from sensor/log/alert)
    Output:
        dict with keys:
            - feature_vector: list of numerical values
            - event_name, threat_type, severity, source_ip, destination_ip, ai_confidence, category
    """

    try:
        # -------------------------------
        # Basic normalization
        # -------------------------------
        event_name = normalize_text(raw_event.get("event_name", "unknown_event"))
        threat_type = normalize_text(raw_event.get("threat_type", "external"))
        severity = normalize_text(raw_event.get("severity", "medium"))
        source_ip = raw_event.get("source_ip", "0.0.0.0")
        destination_ip = raw_event.get("destination_ip", "0.0.0.0")

        # -------------------------------
        # Severity encoding
        # -------------------------------
        severity_map = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        severity_score = severity_map.get(severity, 1)

        # -------------------------------
        # Threat type encoding
        # -------------------------------
        threat_map = {
            "insider": 1,
            "external": 2,
            "network": 3,
            "application": 4,
            "phishing": 5,
            "malware": 6,
            "data": 7,
            "access": 8,
        }
        threat_code = threat_map.get(threat_type, 0)

        # -------------------------------
        # Source & Destination Encoding
        # -------------------------------
        src_int = ip_to_int(source_ip)
        dst_int = ip_to_int(destination_ip)

        # -------------------------------
        # Time-based Features
        # -------------------------------
        now = datetime.utcnow()
        hour_of_day = now.hour
        day_of_week = now.weekday()

        # -------------------------------
        # Text-based Hash Features
        # -------------------------------
        event_hash = hash_to_number(event_name)
        threat_hash = hash_to_number(threat_type)

        # -------------------------------
        # Feature Vector Assembly
        # -------------------------------
        feature_vector = [
            severity_score,
            threat_code,
            src_int % 255,  # normalize IPs into compact range
            dst_int % 255,
            hour_of_day / 24.0,
            day_of_week / 7.0,
            event_hash,
            threat_hash,
        ]

        # -------------------------------
        # Simulated AI Confidence (pre-model)
        # -------------------------------
        ai_confidence = float(
            (severity_score + threat_code) / (len(feature_vector) + 0.1)
        )

        # -------------------------------
        # Category Prediction (initial guess)
        # -------------------------------
        if threat_code in [1, 7, 8]:
            category = "insider"
        else:
            category = "external"

        # -------------------------------
        # Final normalized structure
        # -------------------------------
        normalized = {
            "event_name": event_name.title(),
            "threat_type": threat_type,
            "severity": severity,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "ai_confidence": ai_confidence,
            "category": category,
            "feature_vector": feature_vector,
        }

        return normalized

    except Exception as e:
        print("❌ Feature extraction error:", e)
        # Return a minimal safe fallback
        return {
            "event_name": "Unknown",
            "threat_type": "external",
            "severity": "medium",
            "source_ip": "0.0.0.0",
            "destination_ip": "0.0.0.0",
            "ai_confidence": 0.0,
            "category": "external",
            "feature_vector": [0, 0, 0, 0, 0, 0, 0, 0],
        }
