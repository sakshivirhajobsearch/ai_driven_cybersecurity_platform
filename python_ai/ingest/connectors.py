# ingest/connectors.py
from ingest.parser import parse_raw_event  # use absolute import
import json

def process_event(raw_event_json):
    raw_event = json.loads(raw_event_json)
    parsed_event = parse_raw_event(raw_event)
    print(f"Parsed event: {parsed_event}")
    return parsed_event

if __name__ == "__main__":
    sample = '{"source": "firewall", "src_ip": "192.168.1.10", "dst_ip": "10.0.0.5"}'
    process_event(sample)
