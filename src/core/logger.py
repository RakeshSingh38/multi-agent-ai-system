import logging
import sys
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist (best-effort)
try:
    Path("logs").mkdir(exist_ok=True)
except Exception:
    # In container with volume permission issues, we'll fallback later
    pass

def setup_logger(name: str) -> logging.Logger:
    """Create a logger with both file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler disabled for debugging
    # try:
    #     log_path = Path("logs") / f"{datetime.now().strftime('%Y%m%d')}_multiagent.log"
    #     log_path.parent.mkdir(parents=True, exist_ok=True)
    #     file_handler = logging.FileHandler(str(log_path))
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)
    # except Exception:
    #     pass
    
    return logger

# Create main logger
logger = setup_logger("MultiAgentSystem")
