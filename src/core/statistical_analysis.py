"""Statistical analysis module for the Multi-Agent AI System."""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from scipy import stats
import json


class StatisticalAnalyzer:
    """Handles statistical analysis of collected data."""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_trends(self, data: List[Dict[str, Any]], metric: str = "price") -> Dict[str, Any]:
        """Analyze trends in time series data - Temporarily disabled for maintenance."""
        return {"error": "Trend analysis temporarily disabled for system maintenance"}
    
    def calculate_correlations(self, data: List[Dict[str, Any]], 
                             variables: List[str] = None) -> Dict[str, Any]:
        """Calculate correlations between variables."""
        if not data:
            return {"error": "No data provided for correlation analysis"}
        
        try:
            df = pd.DataFrame(data)
            
            # Select numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if variables:
                numeric_cols = [col for col in numeric_cols if col in variables]
            
            if len(numeric_cols) < 2:
                return {"error": "Need at least 2 numeric variables for correlation"}
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Find strong correlations (|r| > 0.7)
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_correlations.append({
                            "variable1": corr_matrix.columns[i],
                            "variable2": corr_matrix.columns[j],
                            "correlation": corr_value,
                            "strength": "strong" if abs(corr_value) > 0.8 else "moderate"
                        })
            
            return {
                "correlation_matrix": corr_matrix.to_dict(),
                "strong_correlations": strong_correlations,
                "variables_analyzed": numeric_cols
            }
            
        except Exception as e:
            return {"error": f"Correlation analysis failed: {str(e)}"}
    
    def descriptive_statistics(self, data: List[Dict[str, Any]], 
                              variables: List[str] = None) -> Dict[str, Any]:
        """Calculate descriptive statistics."""
        if not data:
            return {"error": "No data provided for descriptive statistics"}
        
        try:
            df = pd.DataFrame(data)
            
            if variables:
                numeric_cols = [col for col in variables if col in df.columns]
            else:
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_cols:
                return {"error": "No numeric variables found"}
            
            stats_dict = {}
            for col in numeric_cols:
                numeric_data = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(numeric_data) > 0:
                    mean_val = numeric_data.mean()
                    std_val = numeric_data.std()
                    
                    # Handle potential NaN values
                    if pd.isna(mean_val):
                        mean_val = 0.0
                    if pd.isna(std_val):
                        std_val = 0.0
                    
                    stats_dict[col] = {
                        "count": len(numeric_data),
                        "mean": mean_val,
                        "median": numeric_data.median(),
                        "std": std_val,
                        "min": numeric_data.min(),
                        "max": numeric_data.max(),
                        "q25": numeric_data.quantile(0.25),
                        "q75": numeric_data.quantile(0.75)
                    }
            
            return {"descriptive_stats": stats_dict}
            
        except Exception as e:
            return {"error": f"Descriptive statistics failed: {str(e)}"}
    
    def market_analysis(self, market_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive market analysis."""
        if not market_data:
            return {"error": "No market data provided"}
        
        try:
            df = pd.DataFrame(market_data)
            
            # Clean and prepare data
            df['price'] = pd.to_numeric(df.get('current_price', 0), errors='coerce')
            df['change_30d'] = pd.to_numeric(df.get('price_change_30d', 0), errors='coerce')
            
            # Remove invalid data
            df = df.dropna(subset=['price'])
            
            if len(df) == 0:
                return {"error": "No valid market data found"}
            
            # Market overview
            total_market_cap = df['price'].sum() if 'market_cap' not in df.columns else df.get('market_cap', 0).sum()
            avg_change = df['change_30d'].mean()
            positive_stocks = len(df[df['change_30d'] > 0])
            negative_stocks = len(df[df['change_30d'] < 0])
            
            # Top performers
            top_gainers = df.nlargest(3, 'change_30d')[['company_name', 'change_30d']].to_dict('records')
            top_losers = df.nsmallest(3, 'change_30d')[['company_name', 'change_30d']].to_dict('records')
            
            # Volatility analysis - handle NaN values properly
            change_std = df['change_30d'].std()
            if pd.isna(change_std):
                change_std = 0.0
            
            return {
                "market_overview": {
                    "total_stocks_analyzed": len(df),
                    "average_change_30d": avg_change if not pd.isna(avg_change) else 0.0,
                    "positive_stocks": positive_stocks,
                    "negative_stocks": negative_stocks,
                    "market_sentiment": "bullish" if avg_change > 0 else "bearish"
                },
                "top_performers": {
                    "gainers": top_gainers,
                    "losers": top_losers
                },
                "volatility": {
                    "standard_deviation": change_std,
                    "volatility_level": "high" if change_std > 10 else "medium" if change_std > 5 else "low"
                }
            }
            
        except Exception as e:
            return {"error": f"Market analysis failed: {str(e)}"}
    
    def generate_insights(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from analysis results."""
        insights = []
        
        # Trend insights
        if "trend_direction" in analysis_results:
            trend = analysis_results["trend_direction"]
            significance = analysis_results.get("statistical_significance", False)
            change = analysis_results.get("total_change_percent", 0)
            
            if significance:
                if trend == "increasing":
                    insights.append(f"Strong upward trend detected with {change:.1f}% total change")
                elif trend == "decreasing":
                    insights.append(f"Strong downward trend detected with {change:.1f}% total change")
            else:
                insights.append("No statistically significant trend detected")
        
        # Correlation insights
        if "strong_correlations" in analysis_results:
            correlations = analysis_results["strong_correlations"]
            if correlations:
                for corr in correlations[:3]:  # Top 3 correlations
                    insights.append(f"Strong {corr['strength']} correlation between {corr['variable1']} and {corr['variable2']} (r={corr['correlation']:.2f})")
        
        # Market insights
        if "market_overview" in analysis_results:
            market = analysis_results["market_overview"]
            sentiment = market.get("market_sentiment", "neutral")
            avg_change = market.get("average_change_30d", 0)
            insights.append(f"Market sentiment is {sentiment} with average {avg_change:.1f}% change")
        
        return insights
