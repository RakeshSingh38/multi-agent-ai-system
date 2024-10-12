import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # LLM backend selector (ollama | huggingface | openai)
        self.llm_backend = os.getenv("LLM_BACKEND", "huggingface").lower()
        
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY", os.getenv("HUGGING_FACE_API", ""))
        
        # Hugging Face models - Updated with latest model versions
        self.huggingface_model = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        self.huggingface_fallback_model = os.getenv("HUGGINGFACE_FALLBACK_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        
        # Database
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./data/multiagent.db")
        self.enable_database = os.getenv("ENABLE_DATABASE", "1").lower() not in ("0", "false", "no", "")
        
        # Redis
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Integration Keys
        self.notion_api_key = os.getenv("NOTION_API_KEY", "")
        self.slack_bot_token = os.getenv("SLACK_BOT_TOKEN", "")
        self.gmail_credentials_path = os.getenv("GMAIL_CREDENTIALS_PATH", "")
        self.jira_url = os.getenv("JIRA_URL", "")
        self.jira_username = os.getenv("JIRA_USERNAME", "")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN", "")
        
        # App Settings
        self.app_env = os.getenv("APP_ENV", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # API Server Settings
        self.api_host = os.getenv("API_HOST", "localhost")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        
        # Ollama Settings
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma2:2b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

settings = Settings()
