import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_features(data):
    """
    Convert incoming JSON event data into numeric ML feature vector.
    Example input: {"cpu_usage": 70, "network_packets": 1500, "failed_logins": 3}
    """
    cpu = float(data.get('cpu_usage', 0))
    packets = float(data.get('network_packets', 0))
    logins = float(data.get('failed_logins', 0))
    return [cpu, packets, logins]
