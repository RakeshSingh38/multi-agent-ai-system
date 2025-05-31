from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.core.logger import logger

class AgentFactory:
    """Factory class for creating and managing agents."""
    
    _agents = {}
    
    @classmethod
    def _load_agents(cls):
        """Lazy load agents to avoid import errors - Enhanced with caching."""
        if not cls._agents:
            try:
                from src.agents.research_agent import ResearchAgent
                from src.agents.analysis_agent import AnalysisAgent
                from src.agents.report_writer_agent import ReportWriterAgent
                from src.agents.task_coordinator import TaskCoordinator
                
                cls._agents = {
                    "research": ResearchAgent, "analysis": AnalysisAgent,
                    "report": ReportWriterAgent, "coordinator": TaskCoordinator
                }
                logger.info("Successfully loaded all agent classes")
            except Exception as e:
                logger.error(f"Error loading agents: {e}")
                cls._agents = {}
    
    @classmethod
    def create_agent(cls, agent_type: str) -> Optional[BaseAgent]:
        """Create an agent of the specified type."""
        cls._load_agents()
        agent_class = cls._agents.get(agent_type.lower())
        if agent_class:
            return agent_class()
        return None
    
    @classmethod
    def get_available_agents(cls) -> Dict[str, str]:
        """Get list of available agents and their descriptions."""
        cls._load_agents()
        agents_info = {}
        for name, agent_class in cls._agents.items():
            try:
                agent = agent_class()
                agents_info[name] = agent.description
            except Exception as e:
                agents_info[name] = f"Error loading: {str(e)}"
        return agents_info
    
    @classmethod
    def create_coordinator(cls):
        """Create a task coordinator instance."""
        cls._load_agents()
        from src.agents.task_coordinator import TaskCoordinator
        return TaskCoordinator()
