@echo off
echo Starting Multi-Agent AI System...
echo.

echo Starting FastAPI server...
start "FastAPI Server" cmd /k "uvicorn src.api.main:app --reload --host localhost --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Streamlit frontend...
start "Streamlit Frontend" cmd /k "streamlit run app.py --server.port 8501"

echo.
echo ✅ Multi-Agent AI System is starting...
echo 📡 API Server: http://localhost:8000
echo 🌐 Frontend: http://localhost:8501
echo.
pause