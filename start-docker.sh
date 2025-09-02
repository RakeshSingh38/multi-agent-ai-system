#!/bin/bash

echo "🚀 Starting Multi-Agent AI System..."

# Start FastAPI server in background
echo "📡 Starting API server..."
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait for API server to start
sleep 5

# Start Streamlit frontend
echo "🌐 Starting Streamlit frontend..."
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

# Keep container running
wait