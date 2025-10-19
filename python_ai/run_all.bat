@echo off
REM ===============================
REM Run All Script for Cybersecurity Platform
REM ===============================
echo ===============================
echo 1️⃣ Initializing Databases
echo ===============================

python database\ai_driven_cybersecurity_platform_central.py
if errorlevel 1 pause

python database\ai_driven_cybersecurity_platform_local.py
if errorlevel 1 pause

python database\central.py
if errorlevel 1 pause

python database\local.py
if errorlevel 1 pause

echo ===============================
echo 2️⃣ Feature Extraction & Ingestion
echo ===============================

python features\feature_extractor.py
if errorlevel 1 pause

python ingest\parser.py
if errorlevel 1 pause

echo ===============================
echo 3️⃣ Notification Modules
echo ===============================

python notifiers\email_notifier.py
if errorlevel 1 pause

python notifiers\sms_notifier.py
if errorlevel 1 pause

echo ===============================
echo 4️⃣ Install Dash (if not installed)
echo ===============================
python -m pip install dash dash-bootstrap-components
if errorlevel 1 pause

echo ===============================
echo 5️⃣ Start Dashboard
echo ===============================
start cmd /k "python dashboard\dashboard.py"

echo ===============================
echo 6️⃣ Train ML Model
echo ===============================
python models\train_model.py
if errorlevel 1 pause

echo ===============================
echo 7️⃣ Start Flask API
echo ===============================
start cmd /k "python api\ai_driven_cybersecurity_platform.py"

echo ===============================
echo ✅ All components started.
echo ===============================
pause
