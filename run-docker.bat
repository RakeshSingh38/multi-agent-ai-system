@echo off
echo ========================================
echo  Multi-Agent AI System - Docker Setup
echo ========================================

echo.
echo Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please make sure .env file exists in the project root.
    pause
    exit /b 1
)

echo .env file found ✓
echo.

echo Building and starting Docker containers...
echo This may take a few minutes on first run...
echo.

docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo.
echo ========================================
echo  Deployment Status
echo ========================================

timeout /t 5 >nul
docker-compose ps

echo.
echo ========================================
echo  Access Your Application
echo ========================================
echo.
echo FastAPI (Backend):     http://localhost:8000
echo Streamlit (Frontend):  http://localhost:8501
echo Ollama API:           http://localhost:11434
echo.
echo To view logs:         docker-compose logs -f
echo To stop:             docker-compose down
echo.

pause