$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"
$ollama = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"

function Test-Url($url) {
    try {
        Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

if (-not (Test-Path $ollama)) {
    throw "Ollama was not found at $ollama"
}

if (-not (Test-Url "http://127.0.0.1:11434/api/tags")) {
    Start-Process -WindowStyle Hidden -FilePath $ollama -ArgumentList "serve"
    Start-Sleep -Seconds 5
}

if (-not (Test-Url "http://127.0.0.1:11434/api/tags")) {
    throw "Ollama did not start correctly. Start it manually with: ollama serve"
}

try {
    & $ollama stop "llama3:latest" 2>$null | Out-Null
}
catch {
}

if (-not (Test-Url "http://127.0.0.1:8000/api/v1/health")) {
    Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList "-m","uvicorn","main:app","--host","127.0.0.1","--port","8000" -WorkingDirectory $backend
    Start-Sleep -Seconds 4
}

if (-not (Test-Url "http://127.0.0.1:8000/api/v1/health")) {
    throw "Backend did not start correctly. Run: cd backend; uvicorn main:app --reload --port 8000"
}

Write-Host "Demo is ready: http://127.0.0.1:8000"
