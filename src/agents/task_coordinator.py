from src.agents.base_agent import BaseAgent
from src.agents.research_agent import ResearchAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.report_writer_agent import ReportWriterAgent
from typing import Dict, Any, List, Optional
from src.core.logger import logger
from src.core.database import TaskExecution, get_db
from src.core.config import settings
from datetime import datetime
import uuid
import json

class TaskCoordinator(BaseAgent):
    """Orchestrates multiple agents to complete complex tasks."""
    
    def __init__(self):
        super().__init__(
            name="TaskCoordinator",
            description="Coordinates and manages task execution across multiple specialized agents.",
            # llm_model removed, always use Ollama
        )
        
        # Initialize specialized agents
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_writer = ReportWriterAgent()
        
        # Agent registry - Enhanced with additional agents
        self.agents = {
            "research": self.research_agent,
            "analysis": self.analysis_agent,
            "report": self.report_writer
        }
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complete workflow with multiple agents."""
        task_type = input_data.get("task_type", "full_analysis")
        task_id = str(uuid.uuid4())
        
        # Set task ID for all agents
        for agent in self.agents.values():
            agent.set_task_id(task_id)
        self.set_task_id(task_id)
        
        # Log task start
        self._create_task_record(task_id, task_type, input_data)
        
        self.log_action(
            action="Starting task coordination",
            reasoning=f"Executing {task_type} workflow",
            metadata={"task_id": task_id, "input": input_data}
        )
        
        try:
            # Execute workflow based on task type
            if task_type == "full_analysis":
                result = await self._execute_full_analysis_workflow(input_data)
            elif task_type == "quick_research":
                result = await self._execute_quick_research_workflow(input_data)
            elif task_type == "report_only":
                result = await self._execute_report_only_workflow(input_data)
            else:
                result = await self._execute_custom_workflow(input_data)
            
            # Update task record
            self._update_task_record(task_id, "completed", result)
            
            return {
                "status": "success",
                "task_id": task_id,
                "task_type": task_type,
                "results": result,
                "execution_time": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Task coordination failed: {str(e)}")
            self._update_task_record(task_id, "failed", {"error": str(e)})
            return {
                "status": "error",
                "task_id": task_id,
                "error": str(e)
            }
    
    async def _execute_full_analysis_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete research -> analysis -> report workflow."""
        workflow_results = {}
        
        # Step 1: Research
        self.log_action(
            action="Workflow step 1/3",
            reasoning="Initiating research phase",
            metadata={"step": "research"}
        )
        
        research_input = {
            "topic": input_data.get("topic"),
            "questions": input_data.get("questions", [])
        }
        research_result = await self.research_agent.execute(research_input)
        workflow_results["research"] = research_result
        
        if research_result["status"] != "success":
            raise Exception("Research phase failed")
        
        # Step 2: Analysis
        self.log_action(
            action="Workflow step 2/3",
            reasoning="Initiating analysis phase",
            metadata={"step": "analysis"}
        )
        
        analysis_input = {
            "research_findings": research_result.get("research_findings"),
            "analysis_type": input_data.get("analysis_type", "comprehensive")
        }
        analysis_result = await self.analysis_agent.execute(analysis_input)
        workflow_results["analysis"] = analysis_result
        
        if analysis_result["status"] != "success":
            raise Exception("Analysis phase failed")
        
        # Step 3: Report Generation
        self.log_action(
            action="Workflow step 3/3",
            reasoning="Initiating report generation",
            metadata={"step": "report"}
        )
        
        report_input = {
            "research_findings": research_result.get("research_findings"),
            "analysis_results": analysis_result.get("analysis_results"),
            "report_type": input_data.get("report_type", "comprehensive"),
            "target_audience": input_data.get("target_audience", "executive")
        }
        report_result = await self.report_writer.execute(report_input)
        workflow_results["report"] = report_result
        
        # Add workflow summary
        workflow_results["summary"] = {
            "total_agents_used": 3,
            "workflow_complete": True,
            "final_output": report_result.get("executive_summary", "")
        }
        
        return workflow_results
    
    async def _execute_quick_research_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research-only workflow."""
        research_result = await self.research_agent.execute(input_data)
        return {"research": research_result}
    
    async def _execute_report_only_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute report generation from existing data."""
        report_result = await self.report_writer.execute(input_data)
        return {"report": report_result}
    
    async def _execute_custom_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom workflow based on specified agents."""
        workflow_results = {}
        agents_to_use = input_data.get("agents", ["research"])
        
        for agent_name in agents_to_use:
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                result = await agent.execute(input_data)
                workflow_results[agent_name] = result
        
        return workflow_results
    
    def _create_task_record(self, task_id: str, task_type: str, input_data: Dict[str, Any]):
        """Create a new task execution record."""
        if not settings.enable_database:
            return
        try:
            db = next(get_db())
            task = TaskExecution(
                task_id=task_id,
                task_type=task_type,
                status="in_progress",
                input_data=input_data,
                agents_involved=list(self.agents.keys())
            )
            db.add(task)
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to create task record (continuing): {e}")
        finally:
            db.close()
    
    def _update_task_record(self, task_id: str, status: str, output_data: Dict[str, Any]):
        """Update task execution record."""
        if not settings.enable_database:
            return
        try:
            db = next(get_db())
            task = db.query(TaskExecution).filter(TaskExecution.task_id == task_id).first()
            if task:
                task.status = status
                task.output_data = output_data
                task.completed_at = datetime.utcnow()
                db.commit()
        except Exception as e:
            logger.warning(f"Failed to update task record (continuing): {e}")
        finally:
            db.close()
