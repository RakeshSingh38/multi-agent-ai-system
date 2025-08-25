# tests/test_agents.py
import pytest
from src.agents.agent_factory import AgentFactory

def test_agent_creation():
    agent = AgentFactory.create_agent("research")
    assert agent is not None
    assert agent.name == "ResearchAgent"
