import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app
from src.core.logger import logger
from src.core.config import settings

if __name__ == "__main__":
    logger.info("Starting Multi-Agent AI System API...")
    logger.info(f"Server will be available at: http://{settings.api_host}:{settings.api_port}")
    uvicorn.run(app, host=settings.api_host, port=settings.api_port, log_level="info")
