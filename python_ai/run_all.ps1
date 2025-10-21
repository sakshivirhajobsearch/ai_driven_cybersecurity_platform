# =====================================================
# File: run_all.ps1
# Purpose: Unified PowerShell launcher for all components
# =====================================================

Write-Host "=== Running Unified AI-Driven SOC Platform ===" -ForegroundColor Cyan

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

$pythonPath = Join-Path $root "python_ai"
$dashboardPath = Join-Path $pythonPath "dashboard"
$backendPath = Join-Path $pythonPath "backend"
$mysqlPath = Join-Path $root "mysql"

# Initialize MySQL database
Write-Host "Initializing MySQL..." -ForegroundColor Yellow
& mysql -u root -p -e "source $mysqlPath\create.sql"
& mysql -u root -p -e "source $mysqlPath\insert_central.sql"
& mysql -u root -p -e "source $mysqlPath\insert_local.sql"

# Start all services in background
Write-Host "`nStarting backend, AI, and dashboard..." -ForegroundColor Yellow
Start-Job { cd $using:backendPath; python app.py }
Start-Job { cd $using:pythonPath; python ai_engine.py }
Start-Job { cd $using:dashboardPath; python dashboard.py }

Write-Host "`n✅ Platform running successfully!"
Write-Host "Dashboard URL: http://127.0.0.1:8051" -ForegroundColor Green
