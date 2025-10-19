# ingest/parser.py
def parse_raw_event(event: dict) -> dict:
    parsed = {
        "source": event.get("source", "unknown"),
        "src_ip": event.get("src_ip", ""),
        "dst_ip": event.get("dst_ip", ""),
        "user": event.get("user", "unknown"),
        "timestamp": event.get("timestamp", None)
    }
    return parsed
