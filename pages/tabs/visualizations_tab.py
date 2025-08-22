"""Visualizations tab for enhanced results page."""
import streamlit as st
from typing import Dict, Any


def render_visualizations_tab(results: Dict[str, Any], visualizer):
    """Render the visualizations tab with charts and graphs."""
    st.subheader("📊 Data Visualizations")

    # Extract market data
    market_data = results.get("results", {}).get("research", {}).get("research_findings", {}).get("market_data", [])

    if market_data:
        # Filter out error entries
        valid_data = [stock for stock in market_data if "error" not in stock and stock.get("current_price")]

        if valid_data:
            # Create visualizations
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🧠 Market Sentiment Analysis")
                sentiment_fig = visualizer.create_market_sentiment_chart(valid_data, "30-Day Market Sentiment")
                st.plotly_chart(sentiment_fig, use_container_width=True)

            with col2:
                st.subheader("💰 Stock Price Comparison")
                price_fig = visualizer.create_price_chart(valid_data, "Current Stock Prices")
                st.plotly_chart(price_fig, use_container_width=True)

            # Full-width trend chart
            if len(valid_data) >= 3:
                st.subheader("📈 Price Trend Analysis")
                trend_fig = visualizer.create_trend_chart(valid_data, "current_price", "Stock Price Trend")
                st.plotly_chart(trend_fig, use_container_width=True)

            # Summary metrics
            st.subheader("📊 Market Summary")
            visualizer.create_summary_metrics({
                "market_overview": {
                    "market_sentiment": "bullish" if sum(1 for s in valid_data if s.get("price_change_30d", 0) > 0) > len(valid_data)/2 else "bearish",
                    "average_change_30d": sum(s.get("price_change_30d", 0) for s in valid_data) / len(valid_data),
                    "total_stocks_analyzed": len(valid_data),
                    "positive_stocks": sum(1 for s in valid_data if s.get("price_change_30d", 0) > 0)
                }
            })
        else:
            st.warning("No valid market data available for visualization.")
    else:
        st.info("📊 No market data found. Run a research task with stock data to see visualizations!")