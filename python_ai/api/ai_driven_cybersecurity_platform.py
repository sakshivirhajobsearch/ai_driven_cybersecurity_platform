from flask import Flask, jsonify
import socket, os

app = Flask(__name__)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Read Dashboard port from environment
DASHBOARD_PORT = int(os.environ.get("DASHBOARD_PORT", "8051"))

@app.route("/")
def home():
    local_ip = get_local_ip()
    return jsonify({
        "message": "AI-Driven Cybersecurity Platform API running",
        "api_urls": {
            "local": "http://127.0.0.1:5000",
            "lan": f"http://{local_ip}:5000"
        },
        "dashboard_urls": {
            "local": f"http://127.0.0.1:{DASHBOARD_PORT}",
            "lan": f"http://{local_ip}:{DASHBOARD_PORT}"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
