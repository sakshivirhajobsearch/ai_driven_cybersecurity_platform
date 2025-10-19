# dashboard/dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
import threading
import time

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

CENTRAL_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootpass',
    'database': 'cybersec_central'
}

# ===============================
# FUNCTION TO QUERY DATABASE
# ===============================
def get_event_data():
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        query = """
            SELECT event_type, COUNT(*) AS count
            FROM events
            GROUP BY event_type
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame(columns=['event_type', 'count'])

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

# ===============================
# DASH APP INITIALIZATION
# ===============================
app = dash.Dash(__name__)
app.title = "AI Cybersecurity Dashboard"

# ===============================
# DASH LAYOUT
# ===============================
app.layout = html.Div([
    html.H1("AI-driven Cybersecurity Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            dcc.Graph(id='event-chart')
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='action-chart')
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS,  # in milliseconds
        n_intervals=0
    )
])

# ===============================
# CALLBACKS FOR LIVE UPDATES
# ===============================
@app.callback(
    Output('event-chart', 'figure'),
    Output('action-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_charts(n):
    # Fetch latest data
    event_df = get_event_data()
    action_df = get_action_data()

    # Event chart
    if not event_df.empty:
        event_fig = px.bar(event_df, x='event_type', y='count',
                           title='Detected Cybersecurity Events',
                           labels={'count': 'Number of Events', 'event_type': 'Event Type'},
                           color='event_type')
    else:
        event_fig = px.bar(title='No event data available')

    # Action chart
    if not action_df.empty:
        action_fig = px.pie(action_df, names='action_taken', values='count',
                            title='Actions Taken')
    else:
        action_fig = px.pie(title='No action data available')

    return event_fig, action_fig

# ===============================
# RUN DASHBOARD
# ===============================
if __name__ == '__main__':
    print(f"Dashboard running locally at http://127.0.0.1:{DASHBOARD_PORT}")
    print(f"Dashboard running on LAN at http://192.168.29.206:{DASHBOARD_PORT}")
    app.run(host="0.0.0.0", port=DASHBOARD_PORT, debug=True)
