# Database scripts
python -m database.ai_driven_cybersecurity_platform_central
python -m database.ai_driven_cybersecurity_platform_local
python -m database.central
python -m database.local

# Feature extraction
python -m features.feature_extractor

# Ingest
python -m ingest.connectors
python -m ingest.parser

# Model training
python -m models.train_model
python -m models.train

# Notifiers
python -m notifiers.email_notifier
python -m notifiers.sms_notifier

# API service
python -m api.ai_driven_cybersecurity_platform

# Dashboard
python -m dashboard.dashboard
