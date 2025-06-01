from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TaskRequest(BaseModel):
    """Request model for task execution - Enhanced with additional validation."""
    task_type: str = Field(..., description="Type of task: full_analysis, quick_research, report_only, custom")
    topic: str = Field(..., description="Main topic for research/analysis")
    questions: List[str] = Field(default=[], description="Specific questions to address")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis to perform")
    report_type: str = Field(default="executive_summary", description="Type of report to generate")
    target_audience: str = Field(default="general", description="Target audience for the report")
    agents: List[str] = Field(default=[], description="Specific agents to use (for custom workflow)")
    priority: str = Field(default="normal", description="Task priority: low, normal, high, urgent")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_type": "full_analysis",
                "topic": "AI trends in healthcare 2025",
                "questions": ["What are the main AI applications in healthcare?", "What are the regulatory challenges?"],
                "analysis_type": "comprehensive",
                "report_type": "executive_summary",
                "target_audience": "executive"
            }
        }

class TaskResponse(BaseModel):
    """Response model for task execution."""
    status: str
    task_id: str
    task_type: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[str] = None

class AgentInfo(BaseModel):
    """Information about an available agent."""
    name: str
    description: str

class TaskStatus(BaseModel):
    """Task execution status."""
    task_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None

class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

class IntegrationRequest(BaseModel):
    """Request for integration actions."""
    integration: str = Field(..., description="Integration to use: slack, notion, gmail, jira")
    action: str = Field(..., description="Action to perform")
    data: Dict[str, Any] = Field(..., description="Data for the action")
    
    class Config:
        json_schema_extra = {
            "example": {
                "integration": "slack",
                "action": "send_message",
                "data": {"channel": "#general", "message": "Task completed successfully!"}
            }
        }

class IntegrationResponse(BaseModel):
    """Response from integration action."""
    status: str
    integration: str
    action: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
