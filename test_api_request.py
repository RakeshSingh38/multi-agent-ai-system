import requests
import json

# Test the API with a proper Python request
def test_api():
    url = "http://localhost:8000/tasks/execute"
    
    data = {
        "task_type": "quick_research",
        "topic": "Tesla stock performance October 2025",
        "questions": ["What is Tesla current stock price?"],
        "analysis_type": "market_analysis", 
        "report_type": "executive_summary",
        "target_audience": "investors"
    }
    
    print("🚀 Testing API request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n📊 Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Error Response: {response.text}")
            
    except Exception as e:
        print(f"\n💥 Exception: {e}")

if __name__ == "__main__":
    test_api()