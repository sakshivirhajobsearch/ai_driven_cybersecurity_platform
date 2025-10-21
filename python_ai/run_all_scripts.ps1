# =====================================================
# File: run_all_scripts.ps1
# Purpose: Launch all major SOC platform components
# =====================================================

Write-Host "=== Starting AI + Cybersecurity Platform (PowerShell) ===" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

# Define paths
$pythonDir = Join-Path $projectRoot "python_ai"
$dashboardDir = Join-Path $pythonDir "dashboard"
$backendDir = Join-Path $pythonDir "backend"
$mysqlDir = Join-Path $projectRoot "mysql"

# Start MySQL schema initialization
Write-Host "`n[1/4] Initializing MySQL schema..." -ForegroundColor Yellow
if (Test-Path "$mysqlDir\create.sql") {
    Write-Host "Running create.sql..."
    & mysql -u root -p -e "source $mysqlDir\create.sql"
}

# Insert central data
Write-Host "`n[2/4] Inserting central data..." -ForegroundColor Yellow
if (Test-Path "$mysqlDir\insert_central.sql") {
    & mysql -u root -p -e "source $mysqlDir\insert_central.sql"
}

# Insert local data
Write-Host "`n[3/4] Inserting local data..." -ForegroundColor Yellow
if (Test-Path "$mysqlDir\insert_local.sql") {
    & mysql -u root -p -e "source $mysqlDir\insert_local.sql"
}

# Start Flask backend
Write-Host "`n[4/4] Starting Flask backend service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "cd '$backendDir'; python app.py"

# Start AI engine
Write-Host "Launching AI engine service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "cd '$pythonDir'; python ai_engine.py"

# Start dashboard
Write-Host "Starting SOC dashboard on http://127.0.0.1:8051 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "cd '$dashboardDir'; python dashboard.py"

Write-Host "`n✅ All services launched successfully!" -ForegroundColor Green
