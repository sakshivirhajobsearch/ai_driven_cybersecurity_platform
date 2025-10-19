# ========================================
# AI-Driven Cybersecurity Platform - RUN ALL
# ========================================

$logFile = "run_all_log.txt"
if (Test-Path $logFile) { Remove-Item $logFile }
Write-Host "Logging output to $logFile"

# MySQL password prompt
$mysqlPassword = Read-Host -AsSecureString "Enter MySQL password for root@localhost"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($mysqlPassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
$env:MYSQL_PASS = $plainPassword

function Run-WithRetry {
    param([string]$description, [string]$command, [int]$maxRetries = 3)
    $attempt = 1
    while ($attempt -le $maxRetries) {
        Write-Host "==== STEP: $description (Attempt $attempt) ===="
        try {
            & cmd /c "$command" *>> $logFile 2>>&1
            if ($LASTEXITCODE -eq 0) { Write-Host "✅ $description"; return $true }
            else { Write-Host "❌ $description failed. Retrying..."; $attempt++; Start-Sleep 3 }
        } catch { Write-Host "❌ EXCEPTION: $_"; $attempt++; Start-Sleep 3 }
    }
    Write-Host "❌ FAILED: $description after $maxRetries attempts."
    return $false
}

# STEP 1: Train ML Model
Run-WithRetry -description "Train ML Model" -command "python -m models.train"

# STEP 2: Find free dashboard port
function Get-FreePort { param([int]$start=8051,[int]$max=8100)
    for ($p=$start;$p -le $max;$p++) { if (-not (netstat -ano | findstr ":$p")) { return $p } }
    throw "No free ports between $start and $max"
}
$dashboardPort = Get-FreePort
$env:DASHBOARD_PORT = $dashboardPort
Write-Host "Dashboard port: $dashboardPort"

# STEP 3: Start Dashboard
$dashboardProcess = Start-Process -PassThru -NoNewWindow -FilePath "python" -ArgumentList "-m dashboard.dashboard" -RedirectStandardOutput "$logFile" -RedirectStandardError "$logFile" -WindowStyle Hidden
do { Start-Sleep 2; $listening = (netstat -ano | findstr ":$dashboardPort") } while (-not $listening)
Write-Host "✅ Dashboard running."

# STEP 4: Start API
$apiProcess = Start-Process -PassThru -NoNewWindow -FilePath "python" -ArgumentList "-m api.ai_driven_cybersecurity_platform" -RedirectStandardOutput "$logFile" -RedirectStandardError "$logFile" -WindowStyle Hidden
do { Start-Sleep 2; $listening = (netstat -ano | findstr ":5000") } while (-not $listening)
Write-Host "✅ API running."

# STEP 5: Show URLs
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp" -and $_.IPAddress -ne "127.0.0.1"} | Select-Object -First 1).IPAddress
Write-Host "`n==== ACCESS LINKS ===="
Write-Host "API (Localhost): http://127.0.0.1:5000"
Write-Host "API (LAN):       http://$localIP:5000"
Write-Host "Dashboard (Localhost): http://127.0.0.1:$dashboardPort"
Write-Host "Dashboard (LAN):       http://$localIP:$dashboardPort"

# Open in browser
Start-Process "http://127.0.0.1:5000"
Start-Process "http://127.0.0.1:$dashboardPort"

# STEP 6: Graceful termination
$onExit = {
    Write-Host "`nCtrl+C detected! Terminating API & Dashboard..."
    if ($apiProcess -ne $null) { Stop-Process -Id $apiProcess.Id -Force }
    if ($dashboardProcess -ne $null) { Stop-Process -Id $dashboardProcess.Id -Force }
    Write-Host "✅ All processes terminated."
    exit
}
$null = Register-EngineEvent PowerShell.Exiting -Action $onExit
$null = Register-EngineEvent Console_CancelKeyPress -Action $onExit

Write-Host "`nPress Ctrl+C to stop API & Dashboard gracefully."
while ($true) { Start-Sleep 5 }
