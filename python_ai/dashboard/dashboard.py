# dashboard/dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ===============================
# CONFIGURATION
# ===============================
REFRESH_INTERVAL_MS = 60000  # 1 minute
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',         # Replace with your MySQL user
    'password': 'admin', # Replace with your MySQL password
    'database': 'ai_driven_cybersecurity_platform_local'
}

# ===============================
# DATABASE FUNCTIONS
# ===============================
def fetch_data(query, columns):
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame(columns=columns)

def get_event_data():
    query = """
        SELECT event_type, threat_category, COUNT(*) AS count
        FROM events
        GROUP BY event_type, threat_category
    """
    return fetch_data(query, ['event_type', 'threat_category', 'count'])

def get_risk_score_data():
    query = "SELECT AVG(risk_score) AS avg_risk FROM events"
    return fetch_data(query, ['avg_risk'])

def get_latest_alerts(limit=10):
    query = f"""
        SELECT timestamp, event_type, threat_category, risk_score, alert_sent
        FROM events
        ORDER BY timestamp DESC
        LIMIT {limit}
    """
    return fetch_data(query, ['timestamp','event_type','threat_category','risk_score','alert_sent'])

# ===============================
# DASHBOARD CLASS
# ===============================
class CyberDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOC Cybersecurity Dashboard")
        self.geometry("1000x700")

        # --- Risk Score ---
        self.risk_label = tk.Label(self, text="Avg Risk: N/A", font=("Helvetica", 36, "bold"), fg="red")
        self.risk_label.pack(pady=10)

        # --- Threat Chart ---
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(10,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- Latest Alerts Table ---
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill=tk.X, pady=10)
        self.tree = ttk.Treeview(self.table_frame)
        self.tree.pack(fill=tk.X)
        self.columns = ['timestamp','event_type','threat_category','risk_score','alert_sent']
        self.tree["columns"] = self.columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor='center')
        self.tree["show"] = "headings"

        # Define tag styles for risk severity
        self.tree.tag_configure('high', background='#ff4d4d')    # red
        self.tree.tag_configure('medium', background='#fff066')  # yellow
        self.tree.tag_configure('low', background='#66ff66')     # green

        # Start updating dashboard
        self.update_dashboard()

    def update_dashboard(self):
        # --- Update Risk Score ---
        risk_df = get_risk_score_data()
        if not risk_df.empty and pd.notna(risk_df['avg_risk'][0]):
            avg_risk = round(risk_df['avg_risk'][0], 2)
            self.risk_label.config(text=f"Avg Risk: {avg_risk}")
        else:
            self.risk_label.config(text="Avg Risk: N/A")

        # --- Update Threat Chart ---
        event_df = get_event_data()
        self.ax.clear()
        if not event_df.empty:
            categories = event_df['threat_category'].unique()
            bar_width = 0.3
            event_types = sorted(event_df['event_type'].unique())
            x_positions = range(len(event_types))
            offsets = [-bar_width/2, bar_width/2] if len(categories)==2 else [0]*len(categories)
            event_type_to_pos = {etype: i for i, etype in enumerate(event_types)}

            for i, cat in enumerate(categories):
                subset = event_df[event_df['threat_category'] == cat]
                positions = [event_type_to_pos[etype] + offsets[i] for etype in subset['event_type']]
                self.ax.bar(positions, subset['count'], width=bar_width, label=cat)

            self.ax.set_xticks(list(event_type_to_pos.values()))
            self.ax.set_xticklabels(list(event_type_to_pos.keys()), fontsize=14)
            self.ax.set_title("Internal vs External Threats", fontsize=20, fontweight='bold')
            self.ax.set_ylabel("Count", fontsize=16)
            self.ax.tick_params(axis='y', labelsize=14)
            self.ax.legend(fontsize=14)
        else:
            self.ax.text(0.5, 0.5, 'No event data', ha='center', va='center', fontsize=16)
        self.canvas.draw()

        # --- Update Latest Alerts Table ---
        for row in self.tree.get_children():
            self.tree.delete(row)
        alerts_df = get_latest_alerts(limit=10)
        if not alerts_df.empty:
            for _, row in alerts_df.iterrows():
                # Determine severity tag
                try:
                    risk = float(row['risk_score'])
                except:
                    risk = 0
                if risk >= 7:
                    tag = 'high'
                elif risk >= 4:
                    tag = 'medium'
                else:
                    tag = 'low'
                self.tree.insert("", tk.END, values=(
                    row['timestamp'], row['event_type'], row['threat_category'], row['risk_score'], row['alert_sent']
                ), tags=(tag,))

        # Schedule next update
        self.after(REFRESH_INTERVAL_MS, self.update_dashboard)

# ===============================
# RUN DASHBOARD
# ===============================
if __name__ == "__main__":
    # Test DB connection first
    try:
        conn_test = mysql.connector.connect(**LOCAL_DB_CONFIG)
        conn_test.close()
    except Error as e:
        messagebox.showerror("Database Connection Error",
                             f"Cannot connect to MySQL:\n{e}")
        exit(1)

    app = CyberDashboard()
    app.mainloop()
