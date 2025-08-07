# HackRx Competition System Startup Script
Write-Host "🚀 HackRx Competition System Startup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Set your OpenRouter API key here
$env:OPENAI_API_KEY = "sk-or-v1-YOUR_KEY_HERE"

if ($env:OPENAI_API_KEY -eq "sk-or-v1-YOUR_KEY_HERE") {
    Write-Host "❌ Please edit start_server.ps1 and add your real OpenRouter API key" -ForegroundColor Red
    Write-Host "   Replace 'sk-or-v1-YOUR_KEY_HERE' with your actual key" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ API Key configured" -ForegroundColor Green
Write-Host "🔧 Starting FastAPI server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 Server will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "🎯 HackRx endpoint: http://localhost:8000/hackrx/run" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Magenta
Write-Host ""

# Start the FastAPI server
try {
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host "Make sure you have installed all dependencies with: pip install -r requirements.txt" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"
