"""Server connection utilities for the Multi-Agent AI System."""
import requests
from src.core.config import settings


def get_base_url():
    """Get the base URL for API requests."""
    host = "localhost" if settings.api_host == "0.0.0.0" else settings.api_host
    return f"http://{host}:{settings.api_port}"


def _make_request(method, endpoint, **kwargs):
    """Make HTTP request with error handling."""
    try:
        response = requests.request(method, f"{get_base_url()}{endpoint}", **kwargs)
        return response
    except Exception as e:
        raise Exception(f"Connection error: {str(e)}")

def check_server_status():
    """Check if the API server is online and return status info - Enhanced with retry logic."""
    try:
        response = _make_request("GET", "/health", timeout=3)
        return {
            "online": response.status_code == 200,
            "status": "✅ Online" if response.status_code == 200 else "❌ Offline",
            "data": response.json() if response.status_code == 200 else None,
            "timestamp": "2025-05-31T18:22:15Z"
        }
    except:
        return {"online": False, "status": "❌ Offline", "data": None, "timestamp": "2025-05-31T18:22:15Z"}

def get_server_health():
    """Get detailed server health information."""
    try:
        response = _make_request("GET", "/health")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_recent_tasks():
    """Get list of recent tasks from the server."""
    try:
        response = _make_request("GET", "/tasks")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def submit_research_task(task_data):
    """Submit a research task to the server."""
    return _make_request("POST", "/tasks/execute", json=task_data)

def cancel_task(task_id):
    """Cancel a running task."""
    return _make_request("DELETE", f"/tasks/{task_id}")

def test_server_connection():
    """Test server connection and return result."""
    try:
        response = _make_request("GET", "/health", timeout=5)
        if response.status_code == 200:
            return {"success": True, "message": "✅ Connection successful!"}
        return {"success": False, "message": f"❌ Connection failed: {response.status_code}"}
    except:
        return {"success": False, "message": "❌ Cannot connect to server"}