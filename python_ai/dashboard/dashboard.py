# python/dashboard/dashboard.py
"""
Dash dashboard for SOC platform.
Requirements:
 - Place alert.mp3 in python/dashboard/assets/alert.mp3 (optional)
 - Uses Dash >= 3, dash_bootstrap_components
"""

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.express as px
import socket
import os

# -------------------------
# CONFIG
# -------------------------
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "admin"),
    "database": os.environ.get("DB_NAME", "ai_driven_cybersecurity_platform_local")
}

REFRESH_INTERVAL_SECONDS = int(os.environ.get("REFRESH_INTERVAL", 60))

# -------------------------
# Helper: Fetch SQL -> DataFrame (defensive)
# -------------------------
def fetch_query(query, params=None):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print("Database error:", e)
        return pd.DataFrame()

# -------------------------
# App init
# -------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "SOC AI Dashboard"

# Layout includes a dcc.Store to keep last_seen_alert_id
app.layout = dbc.Container(fluid=True, children=[
    dcc.Interval(id="auto-refresh", interval=REFRESH_INTERVAL_SECONDS*1000, n_intervals=0),
    dcc.Store(id="last-seen-alert-id", data=0),
    html.Audio(id="alert-sound", src="/assets/alert.mp3", autoPlay=False),
    html.H1("🛡️ SOC AI Dashboard", className="text-center mt-3 mb-2 text-info"),

    html.Div(id="system-stats", className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="severity-chart"), md=6),
        dbc.Col(dcc.Graph(id="threat-type-chart"), md=6)
    ]),

    html.H4("Latest Alerts", className="text-warning mt-4"),
    html.Div(id="alerts-table"),

    html.H4("System Health", className="text-success mt-4"),
    html.Div(id="health-table"),

    # Live toast area (we only show one toast at a time; new critical alerts update this)
    dbc.Toast(id="live-toast",
              header="",
              is_open=False,
              dismissable=True,
              duration=10000,
              style={"position": "fixed", "top": 20, "right": 20, "width": 420, "zIndex": 9999})
])

# -------------------------
# Callback: Refresh everything and manage toast + sound
# -------------------------
@app.callback(
    Output("system-stats", "children"),
    Output("severity-chart", "figure"),
    Output("threat-type-chart", "figure"),
    Output("alerts-table", "children"),
    Output("health-table", "children"),
    Output("live-toast", "is_open"),
    Output("live-toast", "header"),
    Output("live-toast", "children"),
    Output("alert-sound", "autoPlay"),
    Output("last-seen-alert-id", "data"),
    Input("auto-refresh", "n_intervals"),
    State("last-seen-alert-id", "data")
)
def refresh_dashboard(n, last_seen_id):
    # Fetch latest data
    threats_df = fetch_query("SELECT id, threat_type, description, severity_level, ai_confidence, source_ip, target_system, detected_at FROM threat_events ORDER BY detected_at DESC LIMIT 200;")
    alerts_df = fetch_query("SELECT id, alert_type, message, IFNULL(severity, 'Low') AS severity, created_at FROM alerts ORDER BY created_at DESC LIMIT 50;")
    system_df = fetch_query("SELECT id, component, status, checked_at FROM system_health ORDER BY checked_at DESC LIMIT 20;")

    # Normalize column names (ensure lower)
    threats_df.columns = [c if c is None else c for c in threats_df.columns]

    # Defensive counters
    total_threats = len(threats_df)
    high_conf = 0
    critical = 0
    insider_threats = 0
    external_threats = 0

    if not threats_df.empty:
        if "ai_confidence" in threats_df.columns:
            try:
                high_conf = threats_df[threats_df["ai_confidence"].astype(float) > 0.8].shape[0]
            except Exception:
                high_conf = 0
        if "severity_level" in threats_df.columns:
            critical = threats_df[threats_df["severity_level"].astype(str).str.lower() == "critical"].shape[0]
        # If there is a source_type or differentiate by threat_type for internal vs external:
        if "source_ip" in threats_df.columns:
            # crude heuristic: private IPs -> internal, else external (customize as needed)
            def ip_is_private(ip):
                if not ip: return False
                try:
                    parts = ip.split(".")
                    if len(parts) != 4: return False
                    a,b = int(parts[0]), int(parts[1])
                    # 10.x.x.x, 172.16-31.x.x, 192.168.x.x
                    if a == 10: return True
                    if a == 192 and b == 168: return True
                    if a == 172 and 16 <= b <= 31: return True
                except Exception:
                    return False
                return False
            insider_threats = threats_df[threats_df["source_ip"].apply(lambda x: ip_is_private(str(x)))].shape[0]
            external_threats = total_threats - insider_threats

    # Build stats summary
    stats = html.Div([
        html.H5(f"Total Threats: {total_threats}  |  Critical: {critical}  |  High Confidence: {high_conf}  |  Internal: {insider_threats}  |  External: {external_threats}",
                className="text-light text-center")
    ])

    # Severity chart
    if not threats_df.empty and "severity_level" in threats_df.columns:
        severity_counts = threats_df.groupby("severity_level").size().reset_index(name="count")
        fig_severity = px.bar(severity_counts, x="severity_level", y="count", title="Threats by Severity", text_auto=True)
    else:
        fig_severity = px.bar(title="Threats by Severity (no data)")

    # Internal vs External pie
    if total_threats > 0:
        pie_df = pd.DataFrame({
            "type": ["Internal", "External"],
            "count": [insider_threats, external_threats]
        })
        fig_threat_type = px.pie(pie_df, names="type", values="count", title="Internal vs External Threats")
    else:
        fig_threat_type = px.pie(title="Internal vs External Threats")

    # Alerts table
    if not alerts_df.empty:
        alerts_df["created_at"] = alerts_df["created_at"].astype(str)
        table_alerts = dash_table.DataTable(
            data=alerts_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in alerts_df.columns],
            style_cell={"textAlign": "center", "fontSize": 16},
            style_data_conditional=[
                {"if": {"filter_query": '{severity} = "High"'}, "backgroundColor": "#FF7F7F"},
                {"if": {"filter_query": '{severity} = "Medium"'}, "backgroundColor": "#FFF68F"},
                {"if": {"filter_query": '{severity} = "Low"'}, "backgroundColor": "#90EE90"}
            ],
            page_size=10
        )
    else:
        table_alerts = html.P("No alerts found.", className="text-muted")

    # System health table
    if not system_df.empty:
        system_df["checked_at"] = system_df["checked_at"].astype(str)
        table_health = dash_table.DataTable(
            data=system_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in system_df.columns],
            style_cell={"textAlign": "center", "fontSize": 16},
            style_data_conditional=[
                {"if": {"filter_query": '{status} = "ERROR"'}, "backgroundColor": "#FF6347"},
                {"if": {"filter_query": '{status} = "WARNING"'}, "backgroundColor": "#FFD700"},
                {"if": {"filter_query": '{status} = "OK"'}, "backgroundColor": "#90EE90"}
            ],
            page_size=10
        )
    else:
        table_health = html.P("No system health data.", className="text-muted")

    # Toast / Sound detection: look for newest high-severity alert id
    toast_open = False
    toast_header = ""
    toast_body = ""
    play_sound = False
    if not alerts_df.empty and "severity" in alerts_df.columns:
        # Find the newest high severity alert
        high_alerts = alerts_df[alerts_df["severity"].astype(str).str.lower().isin(["high", "critical"])]
        if not high_alerts.empty:
            latest_high = high_alerts.iloc[0]  # newest due to ORDER BY
            try:
                latest_id = int(latest_high["id"])
            except Exception:
                latest_id = last_seen_id or 0
            if latest_id > (last_seen_id or 0):
                # New critical alert found
                toast_open = True
                toast_header = f"{latest_high.get('alert_type','Alert')} — {latest_high.get('severity','')}"
                toast_body = html.Div([
                    html.P(latest_high.get("message", ""), className="text-light"),
                    html.Small(f"Time: {latest_high.get('created_at','')}", className="text-secondary")
                ])
                play_sound = True
                last_seen_id = latest_id

    # Return all outputs
    return stats, fig_severity, fig_threat_type, table_alerts, table_health, toast_open, toast_header, toast_body, play_sound, last_seen_id

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"
    print(f"Dashboard running locally at http://127.0.0.1:8051")
    print(f"Dashboard running on LAN at http://{local_ip}:8051")
    app.run(host="0.0.0.0", port=8051, debug=False)
