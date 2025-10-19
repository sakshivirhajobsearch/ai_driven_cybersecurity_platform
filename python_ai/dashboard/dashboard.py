# dashboard/dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
import datetime

# ===============================
# DASHBOARD CONFIG
# ===============================
DASHBOARD_PORT = 8051
REFRESH_INTERVAL_MS = 60000  # 60 seconds

# ===============================
# DATABASE CONNECTION SETTINGS
# ===============================
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootpass',
    'database': 'cybersec_local'
}

# ===============================
# DATABASE QUERY FUNCTIONS
# ===============================
def get_event_data():
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        query = """
            SELECT event_type, threat_category, COUNT(*) AS count
            FROM events
            GROUP BY event_type, threat_category
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching event data: {e}")
        return pd.DataFrame(columns=['event_type', 'threat_category', 'count'])

def get_action_data():
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        query = """
            SELECT action_taken, COUNT(*) AS count
            FROM actions
            GROUP BY action_taken
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching action data: {e}")
        return pd.DataFrame(columns=['action_taken', 'count'])

def get_risk_score_data():
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        query = """
            SELECT DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') AS hour, AVG(risk_score) AS avg_risk
            FROM events
            GROUP BY hour
            ORDER BY hour ASC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching risk score data: {e}")
        return pd.DataFrame(columns=['hour', 'avg_risk'])

def get_latest_alerts(limit=10):
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        query = f"""
            SELECT timestamp, event_type, threat_category, risk_score, alert_sent
            FROM events
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return pd.DataFrame(columns=['timestamp','event_type','threat_category','risk_score','alert_sent'])

# ===============================
# DASH APP INITIALIZATION
# ===============================
app = dash.Dash(__name__)
app.title = "SOC Cybersecurity Dashboard"

# ===============================
# DASH LAYOUT
# ===============================
app.layout = html.Div([
    html.H1("SOC Cybersecurity Dashboard", style={'textAlign': 'center'}),
    
    # Charts
    html.Div([
        html.Div([
            dcc.Graph(id='event-chart')
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='action-chart')
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        dcc.Graph(id='risk-chart')
    ]),
    
    # Latest alerts table
    html.Div([
        html.H2("Latest Alerts", style={'textAlign': 'center'}),
        html.Div(id='alerts-table')
    ]),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS,  # milliseconds
        n_intervals=0
    )
])

# ===============================
# CALLBACKS FOR LIVE UPDATES
# ===============================
@app.callback(
    Output('event-chart', 'figure'),
    Output('action-chart', 'figure'),
    Output('risk-chart', 'figure'),
    Output('alerts-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    # --- Events chart ---
    event_df = get_event_data()
    if not event_df.empty:
        event_fig = px.bar(
            event_df, x='event_type', y='count', color='threat_category',
            title='Detected Cybersecurity Events (Internal vs External)',
            labels={'count': 'Number of Events', 'event_type': 'Event Type', 'threat_category':'Threat Category'}
        )
    else:
        event_fig = px.bar(title='No event data available')

    # --- Actions chart ---
    action_df = get_action_data()
    if not action_df.empty:
        action_fig = px.pie(
            action_df, names='action_taken', values='count',
            title='Actions Taken'
        )
    else:
        action_fig = px.pie(title='No action data available')

    # --- Risk score chart ---
    risk_df = get_risk_score_data()
    if not risk_df.empty:
        risk_fig = px.line(
            risk_df, x='hour', y='avg_risk',
            title='Average Risk Score Over Time',
            labels={'hour':'Hour', 'avg_risk':'Average Risk Score'}
        )
    else:
        risk_fig = px.line(title='No risk score data available')

    # --- Latest alerts table ---
    alerts_df = get_latest_alerts(limit=10)
    if not alerts_df.empty:
        table_header = [
            html.Thead(html.Tr([html.Th(col) for col in alerts_df.columns]))
        ]
        table_body = [html.Tr([html.Td(alerts_df.iloc[i][col]) for col in alerts_df.columns]) for i in range(len(alerts_df))]
        table = html.Table(table_header + [html.Tbody(table_body)], style={'width':'100%', 'border':'1px solid black','borderCollapse':'collapse'})
    else:
        table = html.Div("No alerts available.")

    return event_fig, action_fig, risk_fig, table

# ===============================
# RUN DASHBOARD
# ===============================
if __name__ == '__main__':
    print(f"Dashboard running locally at http://127.0.0.1:{DASHBOARD_PORT}")
    print(f"Dashboard running on LAN at http://192.168.29.206:{DASHBOARD_PORT}")
    app.run(host="0.0.0.0", port=DASHBOARD_PORT, debug=True)
