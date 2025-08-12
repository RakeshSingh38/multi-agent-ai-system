#!/usr/bin/env python3
"""
Render.com startup script for Multi-Agent AI System
Runs both FastAPI and Streamlit in a single web service
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def start_fastapi():
    """Start FastAPI server - Simplified for performance"""
    print("🚀 Starting FastAPI server...")
    cmd = ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.Popen(cmd)

def start_streamlit():
    """Start Streamlit frontend - Simplified for performance"""
    print("🌐 Starting Streamlit frontend...")
    port = os.environ.get("PORT", "8501")
    cmd = ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", port]
    return subprocess.Popen(cmd)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\n⚠️  Received signal {signum}, shutting down...")
    sys.exit(0)

def main():
    """Main startup function"""
    print("🔥 Multi-Agent AI System - Starting on Render...")
    
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start FastAPI in background
        fastapi_process = start_fastapi()
        time.sleep(3)  # Give FastAPI time to start
        
        # Start Streamlit (main process)
        streamlit_process = start_streamlit()
        
        print("✅ Both services started successfully!")
        print(f"📡 FastAPI: Running on port 8000")
        print(f"🌐 Streamlit: Running on port {os.environ.get('PORT', '8501')}")
        
        # Wait for Streamlit (main process)
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n⚠️  Shutting down...")
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)
    finally:
        # Clean up processes
        try:
            fastapi_process.terminate()
            streamlit_process.terminate()
        except:
            pass

if __name__ == "__main__":
    main()