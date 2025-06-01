from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
import pandas as pd

from src.api.models import (
    TaskRequest, TaskResponse, AgentInfo, 
    TaskStatus, HealthCheck, IntegrationRequest, 
    IntegrationResponse
)
from src.core.statistical_analysis import StatisticalAnalyzer
from src.core.predictive_analysis import PredictiveAnalyzer
from src.core.enhanced_data_collector import EnhancedDataCollector
from src.core.custom_algorithms import CustomAlgorithmManager, initialize_builtin_algorithms
from src.agents.agent_factory import AgentFactory
from src.core.database import get_db, TaskExecution
from src.core.logger import logger
from src.core.config import settings

# Utility function to convert numpy/pandas types to native Python types
def convert_to_serializable(obj):
    """Convert numpy/pandas types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_to_serializable(obj.tolist())
    elif isinstance(obj, (pd.Series, pd.DataFrame)):
        return convert_to_serializable(obj.to_dict())
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent AI System",
    description="Production-ready multi-agent system for automated task execution",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store running tasks
running_tasks: Dict[str, Any] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup - Enhanced with comprehensive logging."""
    logger.info("Multi-Agent AI System starting up...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info("Initializing core services and agents...")
    # Log selected LLM backend and models for quick diagnostics
    try:
        logger.info(
            "LLM backend: %s | HF model: %s | Ollama model: %s | Ollama URL: %s",
            settings.llm_backend,
            getattr(settings, "huggingface_model", "-"),
            getattr(settings, "ollama_model", "-"),
            getattr(settings, "ollama_base_url", "-")
        )
    except Exception:
        pass
    logger.info("All systems initialized successfully!")

@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with health check."""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        services={
            "database": "connected",
            "agents": "ready",
            "integrations": "available"
        }
    )

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Detailed health check endpoint."""
    services_status = {}
    
    # Check database
    if settings.enable_database:
        try:
            db = next(get_db())
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            services_status["database"] = "healthy"
        except Exception as e:
            services_status["database"] = f"unhealthy: {str(e)}"
        finally:
            if 'db' in locals():
                db.close()
    else:
        services_status["database"] = "disabled"

    
    # Check agents
    try:
        AgentFactory.get_available_agents()
        services_status["agents"] = "healthy"
    except Exception as e:
        services_status["agents"] = f"unhealthy: {str(e)}"
    
    # Check OpenAI API
    services_status["openai_api"] = "configured" if settings.openai_api_key else "not_configured"
    
    acceptable = {"healthy", "configured", "disabled"}
    return HealthCheck(
        status="healthy" if all(v in acceptable for v in services_status.values()) else "degraded",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        services=services_status
    )

@app.get("/agents", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents."""
    agents = AgentFactory.get_available_agents()
    return [
        AgentInfo(name=name, description=desc) 
        for name, desc in agents.items()
    ]

@app.post("/tasks/execute", response_model=TaskResponse)
async def execute_task(
    task_request: TaskRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Execute a task using the multi-agent system."""
    logger.info(f"Received task request: {task_request.task_type}")
    
    try:
        # Create coordinator
        coordinator = AgentFactory.create_coordinator()
        
        # Prepare input data
        input_data = task_request.model_dump()
        
        # Execute task
        result = await coordinator.execute(input_data)
        
        # Convert numpy types to native Python types for JSON serialization
        result = convert_to_serializable(result)
        
        # Store task in database (optional)
        task_id = result.get("task_id")
        if settings.enable_database:
            try:
                existing_task = db.query(TaskExecution).filter(TaskExecution.task_id == task_id).first()
                if existing_task:
                    existing_task.status = result.get("status", "completed")
                    existing_task.output_data = result
                    existing_task.completed_at = datetime.utcnow()
                    db.commit()
                    db.refresh(existing_task)
                else:
                    task_execution = TaskExecution(
                        task_id=task_id,
                        status=result.get("status", "completed"),
                        input_data=input_data,
                        output_data=result,
                        created_at=datetime.utcnow(),
                        completed_at=datetime.utcnow()
                    )
                    db.add(task_execution)
                    db.commit()
                    db.refresh(task_execution)
            except Exception as db_err:
                logger.warning(f"DB persistence skipped due to error: {db_err}")
        
        # Also store in memory for immediate access
        result_with_input = dict(result)
        result_with_input["input_data"] = input_data
        running_tasks[task_id] = result_with_input
        
        logger.info(f"Task {task_id} completed")
        
        return TaskResponse(**result)
        
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """Get status of a specific task."""
    if not settings.enable_database:
        # Return in-memory if DB is disabled
        if task_id in running_tasks:
            r = running_tasks[task_id]
            return TaskStatus(
                task_id=r.get("task_id", task_id),
                status=r.get("status", "completed"),
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                input_data=r.get("input_data", {}),
                output_data=r
            )
        raise HTTPException(status_code=404, detail="Task not found")

    task = db.query(TaskExecution).filter(TaskExecution.task_id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatus(
        task_id=task.task_id,
        status=task.status,
        created_at=task.created_at,
        completed_at=task.completed_at,
        input_data=task.input_data,
        output_data=task.output_data
    )

@app.get("/tasks", response_model=List[TaskStatus])
async def list_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List recent tasks."""
    if not settings.enable_database:
        # Return from in-memory store if DB disabled
        items = list(running_tasks.values())[skip:skip+limit]
        return [
            TaskStatus(
                task_id=item.get("task_id", "unknown"),
                status=item.get("status", "completed"),
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                input_data=item.get("input_data", {}),
                output_data=item
            ) for item in items
        ]

    tasks = db.query(TaskExecution).offset(skip).limit(limit).all()
    
    return [
        TaskStatus(
            task_id=task.task_id,
            status=task.status,
            created_at=task.created_at,
            completed_at=task.completed_at,
            input_data=task.input_data,
            output_data=task.output_data
        )
        for task in tasks
    ]

@app.post("/integrations/execute", response_model=IntegrationResponse)
async def execute_integration(integration_request: IntegrationRequest):
    """Execute an integration action."""
    # This is a placeholder - we'll implement actual integrations later
    logger.info(f"Integration request: {integration_request.integration} - {integration_request.action}")
    
    return IntegrationResponse(
        status="success",
        integration=integration_request.integration,
        action=integration_request.action,
        result={"message": "Integration endpoint placeholder - implement specific integration"}
    )

@app.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a running task."""
    if task_id in running_tasks:
        del running_tasks[task_id]
        return {"message": f"Task {task_id} cancelled"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

# Enhanced Analytics Endpoints
@app.post("/analytics/statistical")
async def perform_statistical_analysis(data: Dict[str, Any]):
    """Perform statistical analysis on provided data."""
    try:
        analyzer = StatisticalAnalyzer()
        
        # Extract data
        market_data = data.get("market_data", [])
        analysis_type = data.get("analysis_type", "comprehensive")
        
        results = {}
        
        if market_data:
            # Trend analysis
            if analysis_type in ["comprehensive", "trend"]:
                trend_results = analyzer.analyze_trends(market_data, "current_price")
                results["trend_analysis"] = trend_results
            
            # Correlation analysis
            if analysis_type in ["comprehensive", "correlation"]:
                correlation_results = analyzer.calculate_correlations(
                    market_data, ["current_price", "price_change_30d", "market_cap"]
                )
                results["correlation_analysis"] = correlation_results
            
            # Descriptive statistics
            if analysis_type in ["comprehensive", "descriptive"]:
                desc_stats = analyzer.descriptive_statistics(
                    market_data, ["current_price", "price_change_30d", "market_cap"]
                )
                results["descriptive_statistics"] = desc_stats
            
            # Market analysis
            if analysis_type in ["comprehensive", "market"]:
                market_analysis = analyzer.market_analysis(market_data)
                results["market_analysis"] = market_analysis
        
        # Generate insights
        if results:
            results["insights"] = analyzer.generate_insights(results)
        
        # Convert to serializable format
        results = convert_to_serializable(results)
        
        return {"status": "success", "results": results}
        
    except Exception as e:
        logger.error(f"Statistical analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistical analysis failed: {str(e)}")

@app.post("/analytics/predictive")
async def perform_predictive_analysis(data: Dict[str, Any]):
    """Perform predictive analysis and forecasting."""
    try:
        analyzer = PredictiveAnalyzer()
        
        # Extract data
        market_data = data.get("market_data", [])
        periods = data.get("periods", 5)
        
        results = {}
        
        if market_data:
            # Simple linear forecast
            forecast_results = analyzer.simple_linear_forecast(
                market_data, "current_price", periods=periods
            )
            results["price_forecast"] = forecast_results
            
            # Market forecast
            market_forecast = analyzer.market_forecast(market_data, periods=3)
            results["market_forecast"] = market_forecast
            
            # Correlation-based prediction
            if len(market_data) > 5:
                correlation_pred = analyzer.correlation_based_prediction(
                    market_data, "current_price", ["price_change_30d", "market_cap"], periods=3
                )
                results["correlation_prediction"] = correlation_pred
        
        # Generate insights
        if results:
            results["insights"] = analyzer.generate_forecast_insights(results)
        
        # Convert to serializable format
        results = convert_to_serializable(results)
        
        return {"status": "success", "results": results}
        
    except Exception as e:
        logger.error(f"Predictive analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Predictive analysis failed: {str(e)}")

@app.post("/analytics/custom-algorithms")
async def execute_custom_algorithms(data: Dict[str, Any]):
    """Execute custom algorithms on provided data."""
    try:
        # Initialize algorithm manager
        manager = CustomAlgorithmManager()
        initialize_builtin_algorithms(manager)
        
        # Extract data and algorithm names
        market_data = data.get("market_data", [])
        algorithm_names = data.get("algorithms", ["moving_average", "volatility_calculation", "momentum_analysis"])
        
        results = {}
        
        for algo_name in algorithm_names:
            if algo_name in manager.algorithms:
                algo_result = manager.execute_algorithm(algo_name, market_data)
                results[algo_name] = algo_result
            else:
                results[algo_name] = {"error": f"Algorithm '{algo_name}' not found"}
        
        # Convert to serializable format
        results = convert_to_serializable(results)
        
        return {"status": "success", "results": results}
        
    except Exception as e:
        logger.error(f"Custom algorithm execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Custom algorithm execution failed: {str(e)}")

@app.get("/analytics/algorithms")
async def list_available_algorithms():
    """List all available custom algorithms."""
    try:
        manager = CustomAlgorithmManager()
        initialize_builtin_algorithms(manager)
        
        algorithms = manager.list_algorithms()
        return {"status": "success", "algorithms": algorithms}
        
    except Exception as e:
        logger.error(f"Failed to list algorithms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list algorithms: {str(e)}")

@app.post("/analytics/data-collection")
async def collect_data_from_source(data: Dict[str, Any]):
    """Collect data from various sources."""
    try:
        collector = EnhancedDataCollector()
        
        source_type = data.get("source_type")
        source_params = data.get("params", {})
        
        if source_type == "api":
            result = collector.collect_from_api(**source_params)
        elif source_type == "database":
            result = collector.collect_from_database(**source_params)
        elif source_type == "csv":
            result = collector.collect_from_csv(**source_params)
        elif source_type == "json":
            result = collector.collect_from_json(**source_params)
        elif source_type == "custom":
            result = collector.collect_custom_data(**source_params)
        elif source_type == "news":
            result = collector.collect_news_data(**source_params)
        elif source_type == "social":
            result = collector.collect_social_media_data(**source_params)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown source type: {source_type}")
        
        # Convert to serializable format
        result = convert_to_serializable(result)
        
        return {"status": "success", "result": result}
        
    except Exception as e:
        logger.error(f"Data collection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return {"error": "Internal server error", "detail": str(exc)}
