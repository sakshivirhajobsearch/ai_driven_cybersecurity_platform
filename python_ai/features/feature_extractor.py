# python/features/feature_extractor.py
"""
Simple, defensive feature extractor.
Returns normalized dict and a numeric feature_vector (list) for ML.
Customize per your logs and fields.
"""

def extract_features(raw_event: dict):
    # Ensure raw_event is a dict
    if raw_event is None:
        raw_event = {}

    # Normalize common fields (defensive)
    src_ip = raw_event.get("src_ip") or raw_event.get("source_ip") or ""
    dst_ip = raw_event.get("dst_ip") or raw_event.get("target_ip") or raw_event.get("target_system") or ""
    username = raw_event.get("user") or raw_event.get("username") or ""

    # Basic numeric features (examples)
    num_failed_logins = int(raw_event.get("num_failed_logins", 0) or 0)
    data_exfil_kb = int(raw_event.get("data_exfil_kb", 0) or 0)
    suspicious_score = float(raw_event.get("suspicious_score", 0.0) or 0.0)

    # Build feature_vector (expand with domain specific features)
    feature_vector = [num_failed_logins, data_exfil_kb, int(suspicious_score * 100)]

    normalized = {
        "source": raw_event.get("source", "unknown"),
        "threat_type": raw_event.get("threat_type") or raw_event.get("type"),
        "description": raw_event.get("description") or raw_event.get("message"),
        "severity_level": raw_event.get("severity") or raw_event.get("severity_level"),
        "ai_confidence": raw_event.get("ai_confidence") or raw_event.get("confidence"),
        "src_ip": src_ip,
        "target_system": dst_ip,
        "user": username,
        "feature_vector": feature_vector,
        "category": raw_event.get("category")
    }
    return normalized
