import requests
import json
from .config import settings

class OllamaClient:
    def __init__(self, model=None):
        self.base_url = settings.ollama_base_url
        self.model = model or settings.ollama_model
    
    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """Send request to Ollama using generate endpoint with enhanced error handling"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            raise Exception(f"Ollama error: {response.text}")
