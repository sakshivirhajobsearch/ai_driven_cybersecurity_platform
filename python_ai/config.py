# =====================================================
# File: config.py
# Purpose: Centralized configuration for SOC AI platform
# =====================================================

import os

# -----------------------------
# MySQL Connection Configuration
# -----------------------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "admin")  # <-- Update this
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "soc_ai_platform")

# -----------------------------
# Sync Configuration
# -----------------------------
SYNC_INTERVAL_SECONDS = int(os.getenv("SYNC_INTERVAL_SECONDS", 60))  # Every 60 seconds
LOG_FILE = os.getenv("LOG_FILE", "auto_sync.log")

# -----------------------------
# Notification Configuration
# -----------------------------
EMAIL_ALERTS_ENABLED = True
SMS_ALERTS_ENABLED = True
