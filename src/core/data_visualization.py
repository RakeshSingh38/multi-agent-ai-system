"""Data visualization module for the Multi-Agent AI System."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Any, Optional


class DataVisualizer:
    """Handles data visualization and chart generation."""
    
    def __init__(self):
        self.chart_config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        }
    
    def create_price_chart(self, market_data: List[Dict[str, Any]], 
                          title: str = "Stock Price Analysis") -> go.Figure:
        """Create a price chart for market data - Simplified for performance."""
        return self._empty_chart("Price chart temporarily simplified for performance optimization")
    
    def create_trend_chart(self, data: List[Dict[str, Any]], 
                          metric: str = "price", 
                          title: str = "Trend Analysis") -> go.Figure:
        """Create a trend line chart."""
        if not data:
            return self._empty_chart("No data available for trend analysis")
        
        try:
            df = pd.DataFrame(data)
            
            if metric not in df.columns:
                return self._empty_chart(f"Metric '{metric}' not found")
            
            # Clean numeric data
            df[metric] = pd.to_numeric(df[metric], errors='coerce')
            df = df.dropna(subset=[metric])
            
            if len(df) < 2:
                return self._empty_chart("Insufficient data points for trend")
            
            # Create trend line
            fig = px.line(
                df, 
                y=metric,
                title=title,
                labels={metric: metric.title(), 'index': 'Data Points'}
            )
            
            # Add trend line
            x = np.arange(len(df))
            y = df[metric].values
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            
            fig.add_trace(go.Scatter(
                x=x,
                y=p(x),
                mode='lines',
                name='Trend Line',
                line=dict(dash='dash', color='red')
            ))
            
            fig.update_layout(height=400)
            return fig
            
        except Exception as e:
            return self._error_chart(f"Error creating trend chart: {str(e)}")
    
    def create_correlation_heatmap(self, correlation_matrix: Dict[str, Dict[str, float]], 
                                  title: str = "Correlation Matrix") -> go.Figure:
        """Create a correlation heatmap."""
        if not correlation_matrix:
            return self._empty_chart("No correlation data available")
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(correlation_matrix)
            
            # Create heatmap
            fig = px.imshow(
                df,
                title=title,
                color_continuous_scale='RdBu',
                color_continuous_midpoint=0,
                aspect='auto'
            )
            
            fig.update_layout(height=500)
            return fig
            
        except Exception as e:
            return self._error_chart(f"Error creating correlation heatmap: {str(e)}")
    
    def create_market_sentiment_chart(self, market_data: List[Dict[str, Any]], 
                                     title: str = "Market Sentiment") -> go.Figure:
        """Create a market sentiment pie chart."""
        if not market_data:
            return self._empty_chart("No market data available")
        
        try:
            df = pd.DataFrame(market_data)
            df['change_30d'] = pd.to_numeric(df.get('price_change_30d', 0), errors='coerce')
            
            # Categorize sentiment
            positive = len(df[df['change_30d'] > 0])
            negative = len(df[df['change_30d'] < 0])
            neutral = len(df[df['change_30d'] == 0])
            
            labels = ['Positive', 'Negative', 'Neutral']
            values = [positive, negative, neutral]
            colors = ['green', 'red', 'gray']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors
            )])
            
            fig.update_layout(title=title, height=400)
            return fig
            
        except Exception as e:
            return self._error_chart(f"Error creating sentiment chart: {str(e)}")
    
    def create_dashboard(self, analysis_data: Dict[str, Any]) -> None:
        """Create a comprehensive analytics dashboard."""
        st.subheader("📊 Analytics Dashboard")
        
        # Create columns for different charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Market sentiment
            if "market_data" in analysis_data:
                sentiment_fig = self.create_market_sentiment_chart(
                    analysis_data["market_data"], 
                    "Market Sentiment (30-day)"
                )
                st.plotly_chart(sentiment_fig, use_container_width=True, config=self.chart_config)
            
            # Price chart
            if "market_data" in analysis_data:
                price_fig = self.create_price_chart(
                    analysis_data["market_data"], 
                    "Stock Prices"
                )
                st.plotly_chart(price_fig, use_container_width=True, config=self.chart_config)
        
        with col2:
            # Correlation heatmap
            if "correlation_matrix" in analysis_data:
                corr_fig = self.create_correlation_heatmap(
                    analysis_data["correlation_matrix"],
                    "Variable Correlations"
                )
                st.plotly_chart(corr_fig, use_container_width=True, config=self.chart_config)
            
            # Trend analysis
            if "trend_data" in analysis_data:
                trend_fig = self.create_trend_chart(
                    analysis_data["trend_data"],
                    "price",
                    "Price Trend Analysis"
                )
                st.plotly_chart(trend_fig, use_container_width=True, config=self.chart_config)
    
    def create_summary_metrics(self, analysis_results: Dict[str, Any]) -> None:
        """Create summary metrics display."""
        st.subheader("📈 Key Metrics")
        
        # Create metric columns
        cols = st.columns(4)
        
        # Market overview metrics
        if "market_overview" in analysis_results:
            market = analysis_results["market_overview"]
            
            with cols[0]:
                st.metric(
                    "Market Sentiment",
                    market.get("market_sentiment", "Unknown").title(),
                    delta=f"{market.get('average_change_30d', 0):.1f}%"
                )
            
            with cols[1]:
                st.metric(
                    "Stocks Analyzed",
                    market.get("total_stocks_analyzed", 0),
                    delta=f"{market.get('positive_stocks', 0)} positive"
                )
        
        # Trend metrics
        if "trend_direction" in analysis_results:
            with cols[2]:
                st.metric(
                    "Trend Direction",
                    analysis_results["trend_direction"].title(),
                    delta=f"{analysis_results.get('total_change_percent', 0):.1f}%"
                )
        
        # Volatility metrics
        if "volatility" in analysis_results:
            with cols[3]:
                st.metric(
                    "Volatility Level",
                    analysis_results["volatility"]["volatility_level"].title(),
                    delta=f"{analysis_results['volatility']['standard_deviation']:.1f}"
                )
    
    def _empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        return fig
    
    def _error_chart(self, message: str) -> go.Figure:
        """Create an error chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: {message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="red")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        return fig

