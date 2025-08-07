@echo off
echo 🚀 HackRx Competition System Startup
echo =====================================

REM Set your OpenRouter API key here
set OPENAI_API_KEY=sk-or-v1-YOUR_KEY_HERE

if "%OPENAI_API_KEY%"=="sk-or-v1-YOUR_KEY_HERE" (
    echo ❌ Please edit start_server.bat and add your real OpenRouter API key
    echo    Replace 'sk-or-v1-YOUR_KEY_HERE' with your actual key
    pause
    exit /b 1
)

echo ✅ API Key configured
echo 🔧 Starting FastAPI server...
echo.
echo 📡 Server will be available at: http://localhost:8000
echo 🎯 HackRx endpoint: http://localhost:8000/hackrx/run
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
