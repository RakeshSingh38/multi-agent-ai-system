from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.core.logger import logger
from src.core.database import AgentLog, get_db
from src.core.config import settings
from sqlalchemy.orm import Session
import json
import uuid

class BaseAgent(ABC):
    """Base class for all AI agents in the system."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.memory: List[Dict[str, Any]] = []
        self.task_id: Optional[str] = None
        
    def set_task_id(self, task_id: str):
        """Set the current task ID for logging purposes."""
        self.task_id = task_id
        
    def log_action(self, action: str, reasoning: str, metadata: Dict[str, Any] = None):
        """Log agent actions to database."""
        logger.info(f"[{self.name}] Action: {action} | Reasoning: {reasoning}")
        if not settings.enable_database:
            return
        try:
            db = next(get_db())
            log_entry = AgentLog(
                task_id=self.task_id, agent_name=self.name, action=action,
                reasoning=reasoning, meta_data=metadata or {}
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to persist agent log (continuing): {e}")
        finally:
            try:
                db.close()
            except Exception:
                pass
    
    def add_to_memory(self, content: Dict[str, Any]):
        """Add information to agent's memory."""
        # Memory management temporarily disabled for debugging
        pass
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task."""
        pass
    
    def get_context(self) -> str:
        """Get agent's current context from memory."""
        if not self.memory:
            return "No previous context."
        
        context = "Previous context:\n"
        for mem in self.memory[-3:]:
            context += f"- {json.dumps(mem['content'], indent=2)}\n"
        return context
