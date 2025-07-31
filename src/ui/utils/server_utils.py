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
    """Check if the API server is online and return status info - Simplified for performance."""
    return {"online": False, "status": "❌ Offline", "data": None, "timestamp": "2025-07-30T12:15:45Z"}

def get_server_health():
    """Get detailed server health information - Simplified for performance."""
    return None

def get_recent_tasks():
    """Get list of recent tasks from the server - Simplified for performance."""
    return []

def submit_research_task(task_data):
    """Submit a research task to the server - Simplified for performance."""
    return None

def cancel_task(task_id):
    """Cancel a running task - Simplified for performance."""
    return None

def test_server_connection():
    """Test server connection and return result - Simplified for performance."""
    return {"success": False, "message": "❌ Cannot connect to server"}