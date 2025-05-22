"""Predictive analysis module for the Multi-Agent AI System."""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class PredictiveAnalyzer:
    """Handles predictive analysis and forecasting."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
    
    def simple_linear_forecast(self, data: List[Dict[str, Any]], 
                              metric: str = "price", 
                              periods: int = 5) -> Dict[str, Any]:
        """Create a simple linear forecast - Temporarily disabled for optimization."""
        return {"error": "Linear forecasting temporarily disabled for system optimization"}
    
    def market_forecast(self, market_data: List[Dict[str, Any]], 
                       periods: int = 3) -> Dict[str, Any]:
        """Forecast market trends based on historical data."""
        if not market_data:
            return {"error": "No market data provided"}
        
        try:
            df = pd.DataFrame(market_data)
            
            # Clean and prepare data
            df['price'] = pd.to_numeric(df.get('current_price', 0), errors='coerce')
            df['change_30d'] = pd.to_numeric(df.get('price_change_30d', 0), errors='coerce')
            df = df.dropna(subset=['price'])
            
            if len(df) < 3:
                return {"error": "Insufficient market data for forecasting"}
            
            # Calculate market average trend
            avg_price = df['price'].mean()
            avg_change = df['change_30d'].mean()
            
            # Simple trend-based forecast
            forecast_prices = []
            current_avg = avg_price
            
            for i in range(periods):
                # Apply average change rate
                change_factor = 1 + (avg_change / 100)
                current_avg *= change_factor
                forecast_prices.append(current_avg)
            
            # Calculate volatility
            volatility = df['change_30d'].std()
            
            # Market sentiment forecast
            positive_ratio = len(df[df['change_30d'] > 0]) / len(df)
            
            return {
                "market_forecast": {
                    "forecasted_prices": forecast_prices,
                    "periods": [f"Month {i+1}" for i in range(periods)],
                    "current_average_price": avg_price,
                    "expected_change_rate": avg_change
                },
                "market_indicators": {
                    "volatility": volatility,
                    "positive_sentiment_ratio": positive_ratio,
                    "market_stability": "stable" if volatility < 5 else "volatile"
                },
                "confidence": {
                    "data_quality": "high" if len(df) > 10 else "medium" if len(df) > 5 else "low",
                    "forecast_reliability": "high" if volatility < 10 else "medium"
                }
            }
            
        except Exception as e:
            return {"error": f"Market forecasting failed: {str(e)}"}
    
    def correlation_based_prediction(self, data: List[Dict[str, Any]], 
                                   target_var: str, 
                                   predictor_vars: List[str],
                                   periods: int = 3) -> Dict[str, Any]:
        """Make predictions based on correlations between variables."""
        if not data or len(data) < 5:
            return {"error": "Insufficient data for correlation-based prediction"}
        
        try:
            df = pd.DataFrame(data)
            
            # Check if all required variables exist
            all_vars = [target_var] + predictor_vars
            missing_vars = [var for var in all_vars if var not in df.columns]
            if missing_vars:
                return {"error": f"Missing variables: {missing_vars}"}
            
            # Clean numeric data
            for var in all_vars:
                df[var] = pd.to_numeric(df[var], errors='coerce')
            
            df = df.dropna(subset=all_vars)
            
            if len(df) < 5:
                return {"error": "Insufficient valid data after cleaning"}
            
            # Prepare features and target
            X = df[predictor_vars].values
            y = df[target_var].values
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Fit model
            model = LinearRegression()
            model.fit(X_scaled, y)
            
            # Calculate correlations
            correlations = {}
            for var in predictor_vars:
                corr = np.corrcoef(df[var], y)[0, 1]
                correlations[var] = corr
            
            # Generate predictions (using last known values)
            last_features = X[-1:].reshape(1, -1)
            last_features_scaled = scaler.transform(last_features)
            
            predictions = []
            for i in range(periods):
                pred = model.predict(last_features_scaled)[0]
                predictions.append(pred)
                # Simple assumption: features change by average historical change
                for j, var in enumerate(predictor_vars):
                    avg_change = df[var].pct_change().mean()
                    last_features[0, j] *= (1 + avg_change)
                last_features_scaled = scaler.transform(last_features)
            
            # Model evaluation
            y_pred = model.predict(X_scaled)
            r2 = r2_score(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            
            return {
                "predictions": {
                    "values": predictions,
                    "periods": [f"Period {i+1}" for i in range(periods)]
                },
                "correlations": correlations,
                "model_performance": {
                    "r_squared": r2,
                    "mean_squared_error": mse,
                    "feature_importance": dict(zip(predictor_vars, model.coef_))
                },
                "strongest_predictors": sorted(correlations.items(), 
                                             key=lambda x: abs(x[1]), reverse=True)[:3]
            }
            
        except Exception as e:
            return {"error": f"Correlation-based prediction failed: {str(e)}"}
    
    def generate_forecast_insights(self, forecast_results: Dict[str, Any]) -> List[str]:
        """Generate insights from forecast results."""
        insights = []
        
        # Linear forecast insights
        if "forecast" in forecast_results:
            forecast = forecast_results["forecast"]
            model_metrics = forecast_results.get("model_metrics", {})
            
            trend = model_metrics.get("trend", "unknown")
            r2 = model_metrics.get("r_squared", 0)
            
            if r2 > 0.7:
                insights.append(f"Strong predictive model (R² = {r2:.2f}) with {trend} trend")
            elif r2 > 0.4:
                insights.append(f"Moderate predictive model (R² = {r2:.2f}) with {trend} trend")
            else:
                insights.append(f"Weak predictive model (R² = {r2:.2f}) - forecasts may be unreliable")
        
        # Market forecast insights
        if "market_forecast" in forecast_results:
            market = forecast_results["market_forecast"]
            indicators = forecast_results.get("market_indicators", {})
            
            change_rate = market.get("expected_change_rate", 0)
            volatility = indicators.get("volatility", 0)
            
            if change_rate > 0:
                insights.append(f"Market expected to grow at {change_rate:.1f}% rate")
            else:
                insights.append(f"Market expected to decline at {abs(change_rate):.1f}% rate")
            
            if volatility > 10:
                insights.append("High market volatility detected - forecasts have higher uncertainty")
        
        # Correlation insights
        if "strongest_predictors" in forecast_results:
            predictors = forecast_results["strongest_predictors"]
            if predictors:
                best_predictor = predictors[0]
                insights.append(f"Strongest predictor: {best_predictor[0]} (correlation: {best_predictor[1]:.2f})")
        
        return insights

