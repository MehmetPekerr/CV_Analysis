$ErrorActionPreference = "Stop"

try {
    $gpu = nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    Write-Host "GPU: $gpu"
}
catch {
    Write-Host "nvidia-smi is not available."
}

$body = @{
    model = "llama3:latest"
    prompt = 'Return only this JSON: {"ok": true}'
    stream = $false
    options = @{
        temperature = 0.1
        num_predict = 20
    }
} | ConvertTo-Json -Depth 5

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/generate" -Method Post -ContentType "application/json" -Body $body -UseBasicParsing -TimeoutSec 90
    Write-Host "GPU/default Ollama generation succeeded."
    Write-Host $response.Content
}
catch {
    Write-Host "GPU/default Ollama generation failed."
    Write-Host $_.Exception.Message
    if ($_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message
    }
}
