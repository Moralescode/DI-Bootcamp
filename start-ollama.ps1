#!/usr/bin/env pwsh
# Ollama Startup Script for Windows
# Run this to start the Ollama server

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

if (-not (Test-Path $ollamaPath)) {
    Write-Error "Ollama executable not found at $ollamaPath"
    exit 1
}

$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue

if ($ollamaProcess) {
    Write-Host "Ollama is already running (PID: $($ollamaProcess.Id))" -ForegroundColor Green
    & $ollamaPath list
    exit 0
}

Write-Host "Starting Ollama server..." -ForegroundColor Cyan
Start-Process $ollamaPath -ArgumentList "serve" -WindowStyle Hidden

$maxRetries = 10
$retryDelay = 2

for ($i = 1; $i -le $maxRetries; $i++) {
    Start-Sleep -Seconds $retryDelay
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/version" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        Write-Host "Ollama is running!" -ForegroundColor Green
        Write-Host "Version: $($response.Content)" -ForegroundColor Green
        & $ollamaPath list
        exit 0
    } catch {
        Write-Host "Waiting for Ollama to start... ($i/$maxRetries)" -ForegroundColor Yellow
    }
}

Write-Error "Failed to start Ollama"
exit 1
