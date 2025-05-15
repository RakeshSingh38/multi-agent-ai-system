"""Custom algorithm support module for user-defined analysis functions."""
import ast
import inspect
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Callable, Optional, Union
import logging
import traceback


class CustomAlgorithmManager:
    """Manages custom user-defined analysis algorithms."""
    
    def __init__(self):
        self.algorithms = {}
        self.logger = logging.getLogger(__name__)
    
    def register_algorithm(self, name: str, function: Callable, 
                          description: str = "", parameters: Dict[str, Any] = None) -> bool:
        """Register a custom algorithm function - Simplified registration."""
        try:
            # Simplified registration for performance
            self.algorithms[name] = {
                "function": function,
                "description": description,
                "registered_at": pd.Timestamp.now().isoformat()
            }
            
            self.logger.info(f"Successfully registered algorithm: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register algorithm {name}: {str(e)}")
            return False
    
    def execute_algorithm(self, name: str, data: Any, **kwargs) -> Dict[str, Any]:
        """Execute a registered custom algorithm."""
        if name not in self.algorithms:
            return {
                "success": False,
                "error": f"Algorithm '{name}' not found",
                "available_algorithms": list(self.algorithms.keys())
            }
        
        try:
            algorithm = self.algorithms[name]
            function = algorithm["function"]
            
            # Prepare arguments
            args = [data] if data is not None else []
            
            # Execute the function
            result = function(*args, **kwargs)
            
            return {
                "success": True,
                "result": result,
                "algorithm_name": name,
                "execution_time": pd.Timestamp.now().isoformat(),
                "parameters_used": kwargs
            }
            
        except Exception as e:
            error_trace = traceback.format_exc()
            self.logger.error(f"Algorithm execution failed for {name}: {error_trace}")
            
            return {
                "success": False,
                "error": str(e),
                "traceback": error_trace,
                "algorithm_name": name
            }
    
    def list_algorithms(self) -> Dict[str, Any]:
        """List all registered algorithms."""
        algorithm_list = {}
        
        for name, info in self.algorithms.items():
            algorithm_list[name] = {
                "description": info["description"],
                "parameters": info["parameters"],
                "signature": info["signature"],
                "registered_at": info["registered_at"]
            }
        
        return {
            "algorithms": algorithm_list,
            "total_count": len(self.algorithms)
        }
    
    def create_algorithm_from_code(self, name: str, code: str, 
                                  description: str = "") -> bool:
        """Create an algorithm from Python code string."""
        try:
            # Parse and compile the code
            tree = ast.parse(code)
            
            # Extract function definitions
            functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            
            if not functions:
                raise ValueError("No function definitions found in code")
            
            # Use the first function
            func_node = functions[0]
            func_name = func_node.name
            
            # Compile and execute the code
            compiled_code = compile(tree, f"<algorithm_{name}>", "exec")
            namespace = {}
            exec(compiled_code, namespace)
            
            # Get the function
            if func_name not in namespace:
                raise ValueError(f"Function '{func_name}' not found in compiled code")
            
            function = namespace[func_name]
            
            # Register the algorithm
            return self.register_algorithm(name, function, description)
            
        except Exception as e:
            self.logger.error(f"Failed to create algorithm from code: {str(e)}")
            return False
    
    def validate_algorithm_code(self, code: str) -> Dict[str, Any]:
        """Validate algorithm code without executing it."""
        try:
            # Parse the code
            tree = ast.parse(code)
            
            # Check for function definitions
            functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            
            if not functions:
                return {
                    "valid": False,
                    "error": "No function definitions found"
                }
            
            # Check for dangerous operations
            dangerous_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    dangerous_nodes.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dangerous_nodes.append(node.module)
            
            # Check for allowed imports (basic data science libraries)
            allowed_imports = ['pandas', 'numpy', 'math', 'statistics', 'collections']
            dangerous_imports = [imp for imp in dangerous_nodes if imp not in allowed_imports]
            
            return {
                "valid": True,
                "functions_found": [func.name for func in functions],
                "dangerous_imports": dangerous_imports,
                "warnings": dangerous_imports if dangerous_imports else []
            }
            
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }


class BuiltInAlgorithms:
    """Collection of built-in analysis algorithms."""
    
    @staticmethod
    def moving_average(data: List[Dict[str, Any]], 
                      value_column: str = "value", 
                      window: int = 5) -> Dict[str, Any]:
        """Calculate moving average."""
        try:
            df = pd.DataFrame(data)
            if value_column not in df.columns:
                return {"error": f"Column '{value_column}' not found"}
            
            values = pd.to_numeric(df[value_column], errors='coerce')
            moving_avg = values.rolling(window=window).mean()
            
            return {
                "moving_average": moving_avg.tolist(),
                "window": window,
                "data_points": len(values)
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def volatility_calculation(data: List[Dict[str, Any]], 
                              value_column: str = "value") -> Dict[str, Any]:
        """Calculate volatility metrics."""
        try:
            df = pd.DataFrame(data)
            if value_column not in df.columns:
                return {"error": f"Column '{value_column}' not found"}
            
            values = pd.to_numeric(df[value_column], errors='coerce').dropna()
            
            # Calculate returns
            returns = values.pct_change().dropna()
            
            # Volatility metrics
            volatility = returns.std() * np.sqrt(252)  # Annualized
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            
            return {
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "mean_return": returns.mean(),
                "std_return": returns.std(),
                "data_points": len(returns)
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def momentum_analysis(data: List[Dict[str, Any]], 
                         value_column: str = "value",
                         periods: List[int] = [5, 10, 20]) -> Dict[str, Any]:
        """Calculate momentum indicators."""
        try:
            df = pd.DataFrame(data)
            if value_column not in df.columns:
                return {"error": f"Column '{value_column}' not found"}
            
            values = pd.to_numeric(df[value_column], errors='coerce').dropna()
            
            momentum_results = {}
            for period in periods:
                if len(values) >= period:
                    momentum = (values.iloc[-1] - values.iloc[-period]) / values.iloc[-period] * 100
                    momentum_results[f"momentum_{period}d"] = momentum
            
            # RSI calculation (simplified)
            if len(values) >= 14:
                delta = values.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                momentum_results["rsi"] = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            
            return momentum_results
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def sector_analysis(data: List[Dict[str, Any]], 
                       sector_column: str = "sector",
                       value_column: str = "value") -> Dict[str, Any]:
        """Analyze performance by sector."""
        try:
            df = pd.DataFrame(data)
            
            if sector_column not in df.columns or value_column not in df.columns:
                return {"error": f"Required columns not found"}
            
            df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
            df = df.dropna(subset=[sector_column, value_column])
            
            # Group by sector
            sector_stats = df.groupby(sector_column)[value_column].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            
            # Calculate sector performance
            sector_performance = {}
            for sector in sector_stats.index:
                sector_data = df[df[sector_column] == sector]
                if len(sector_data) > 1:
                    performance = sector_data[value_column].pct_change().mean() * 100
                    sector_performance[sector] = performance
            
            return {
                "sector_statistics": sector_stats.to_dict('index'),
                "sector_performance": sector_performance,
                "total_sectors": len(sector_stats)
            }
        except Exception as e:
            return {"error": str(e)}


def initialize_builtin_algorithms(manager: CustomAlgorithmManager) -> None:
    """Initialize built-in algorithms in the manager."""
    builtin_algs = BuiltInAlgorithms()
    
    # Register built-in algorithms
    manager.register_algorithm(
        "moving_average", 
        builtin_algs.moving_average,
        "Calculate moving average with specified window"
    )
    
    manager.register_algorithm(
        "volatility_calculation",
        builtin_algs.volatility_calculation,
        "Calculate volatility and risk metrics"
    )
    
    manager.register_algorithm(
        "momentum_analysis",
        builtin_algs.momentum_analysis,
        "Calculate momentum indicators and RSI"
    )
    
    manager.register_algorithm(
        "sector_analysis",
        builtin_algs.sector_analysis,
        "Analyze performance by sector"
    )

