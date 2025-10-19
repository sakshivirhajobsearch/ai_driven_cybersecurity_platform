# Cybersec Solution (AI + Python + Java + MySQL)

## Overview
This project collects internal and external security events, runs ML inference to score/prioritize threats, records events and remediation actions into local and centralized MySQL, provides a JavaFX GUI with hourly charts, and sends notifications via email/SMS.

## Components
- python/ : ingestion, feature extraction, model training & Flask inference service
- java/ : JavaFX GUI, DB manager, notification clients, inference client
- mysql/ : schema + sample data
- docs/ : architecture, deployment

## Quickstart (Local)
1. Setup MySQL:
   - `mysql -u root -p < mysql/schema.sql`
2. Python:
   - `cd python`
   - `pip install -r requirements.txt`
   - Train (if you have training data): `python models/train.py`
   - Run API: `python api/app.py` (listens on port 5000)
3. Java:
   - Edit `src/main/resources/application.properties` with DB & notifier creds and inference endpoint `http://localhost:5000`
   - `mvn clean package`
   - Run `java -jar target/cybersec-solution-1.0.0.jar`
4. Configure connectors to forward logs to `python/ingest` or call Java `InferenceClient` with raw events.

## Alerts
- Configure email credentials (SMTP) and Twilio in `application.properties` for production alerts.

## Security & Hardening Notes
- Use TLS for inference and DB connections.
- Use least-privilege DB users.
- Rotate API keys and secrets (do NOT store in repo; use env or vault).
- Use rate limiting and authentication on the Flask API (JWT or mTLS).

