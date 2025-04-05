import requests
from src.core.config import settings
from src.core.logger import logger


class HuggingFaceClient:
    """Simple Hugging Face Inference API client for text generation/chat with fallback."""

    def __init__(self, model: str | None = None):
        if not settings.huggingface_api_key:
            raise RuntimeError("Hugging Face API key not configured. Set HUGGINGFACE_API_KEY or HUGGING_FACE_API.")
        self.model = model or settings.huggingface_model
        self.fallback_model = settings.huggingface_fallback_model
        self.api_key = settings.huggingface_api_key
        self.base_url = "https://api-inference.huggingface.co/models/"

    def _generate_for_model(self, model_id: str, prompt: str, max_new_tokens: int, temperature: float) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Wait-For-Model": "true",
            "User-Agent": "MultiAgent-AI-System/1.0"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False,
            },
        }
        url = f"{self.base_url}{model_id}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
        except requests.HTTPError as http_err:
            try:
                err = http_err.response.json() if http_err.response is not None else {"error": str(http_err)}
            except Exception:
                err = {"error": str(http_err)}
            raise RuntimeError(f"Hugging Face API error: {err}")
        except Exception as e:
            raise RuntimeError(f"Hugging Face request failed: {e}")

        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        return str(data)

    def generate(self, prompt: str, max_new_tokens: int = 512, temperature: float = 0.7) -> str:
        try:
            return self._generate_for_model(self.model, prompt, max_new_tokens, temperature)
        except RuntimeError as e:
            msg = str(e)
            # If model is gated/forbidden/not found, use fallback
            if any(code in msg for code in ["401", "403", "404"]) or "agree" in msg.lower() or "not found" in msg.lower():
                if self.fallback_model and self.fallback_model != self.model:
                    logger.info(f"HF primary model unavailable; falling back to {self.fallback_model}")
                    return self._generate_for_model(self.fallback_model, prompt, max_new_tokens, temperature)
            raise RuntimeError(
                f"Hugging Face call failed: {msg}. If using a gated model (e.g., Meta Llama), "
                f"request access and accept the license on the model page."
            )
