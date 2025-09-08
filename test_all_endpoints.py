import requests
import json
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.core.config import settings

BASE_URL = f"http://{settings.api_host}:{settings.api_port}"

def test_all_endpoints():
    print("🧪 Testing Multi-Agent AI System\n")
    
    # 1. Health Check
    print("1️ Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data['status']}")
            print(f"   Services: {json.dumps(data['services'], indent=2)}\n")
        else:
            print(f"   Error: Status code {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 2. List Agents
    print("\n2️ Available Agents:")
    try:
        response = requests.get(f"{BASE_URL}/agents")
        if response.status_code == 200 and response.text:
            agents = response.json()
            for agent in agents:
                print(f"   - {agent['name']}: {agent['description']}")
        else:
            print(f"   Error: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 3. Root endpoint
    print("\n3️ Root Endpoint Test:")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"   ✓ API is responding")
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: Status {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nCheck the API documentation:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    test_all_endpoints()
