"""Statistics tab for enhanced results page."""
import streamlit as st
from typing import Dict, Any
import pandas as pd


def render_statistics_tab(results: Dict[str, Any], stat_analyzer):
    """Render the statistics tab with statistical analysis."""
    st.subheader("🧮 Statistical Analysis")

    # Extract market data
    market_data = results.get("results", {}).get("research", {}).get("research_findings", {}).get("market_data", [])

    if market_data:
        valid_data = [stock for stock in market_data if "error" not in stock and stock.get("current_price")]

        if valid_data:
            # Perform market analysis
            analysis_result = stat_analyzer.market_analysis(valid_data)

            if "error" not in analysis_result:
                # Market overview
                st.subheader("📊 Market Overview")
                market_overview = analysis_result.get("market_overview", {})

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_stocks = market_overview.get("total_stocks_analyzed", 0)
                    st.metric("Stocks Analyzed", total_stocks)
                with col2:
                    avg_change = market_overview.get("average_change_30d", 0)
                    st.metric("Avg 30d Change", f"{avg_change:+.1f}%")
                with col3:
                    positive = market_overview.get("positive_stocks", 0)
                    st.metric("Positive Stocks", positive)
                with col4:
                    sentiment = market_overview.get("market_sentiment", "neutral")
                    sentiment_icon = "📈" if sentiment == "bullish" else "📉"
                    st.metric("Market Sentiment", f"{sentiment_icon} {sentiment.title()}")

                # Top performers
                st.subheader("🏆 Top Performers")
                top_performers = analysis_result.get("top_performers", {})

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**📈 Top Gainers**")
                    gainers = top_performers.get("gainers", [])
                    for i, stock in enumerate(gainers, 1):
                        company = stock.get("company_name", "Unknown")
                        change = stock.get("change_30d", 0)
                        st.write(f"{i}. **{company}**: {change:+.2f}%")

                with col2:
                    st.write("**📉 Top Losers**")
                    losers = top_performers.get("losers", [])
                    for i, stock in enumerate(losers, 1):
                        company = stock.get("company_name", "Unknown")
                        change = stock.get("change_30d", 0)
                        st.write(f"{i}. **{company}**: {change:+.2f}%")

                # Volatility analysis
                st.subheader("📊 Volatility Analysis")
                volatility = analysis_result.get("volatility", {})

                col1, col2 = st.columns(2)
                with col1:
                    std_dev = volatility.get("standard_deviation", 0)
                    # Handle NaN values
                    if pd.isna(std_dev) or std_dev is None:
                        std_dev = 0.0
                    st.metric("Standard Deviation", f"{std_dev:.2f}%")
                with col2:
                    vol_level = volatility.get("volatility_level", "unknown")
                    vol_color = "🟢" if vol_level == "low" else "🟡" if vol_level == "medium" else "🔴"
                    st.metric("Volatility Level", f"{vol_color} {vol_level.title()}")

                # Descriptive statistics
                desc_stats = stat_analyzer.descriptive_statistics(valid_data, variables=["current_price", "price_change_30d"])

                if "error" not in desc_stats:
                    st.subheader("📈 Descriptive Statistics")
                    stats_data = desc_stats.get("descriptive_stats", {})

                    for variable, stats in stats_data.items():
                        st.write(f"**{variable.replace('_', ' ').title()}**")

                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Mean", f"{stats.get('mean', 0):.2f}")
                        with col2:
                            st.metric("Median", f"{stats.get('median', 0):.2f}")
                        with col3:
                            st.metric("Min", f"{stats.get('min', 0):.2f}")
                        with col4:
                            st.metric("Max", f"{stats.get('max', 0):.2f}")
                        with col5:
                            std_val = stats.get('std', 0)
                            # Handle NaN values
                            if pd.isna(std_val) or std_val is None:
                                std_val = 0.0
                            st.metric("Std Dev", f"{std_val:.2f}")

                        st.markdown("---")

                # Insights
                insights = stat_analyzer.generate_insights(analysis_result)
                if insights:
                    st.subheader("💡 Statistical Insights")
                    for insight in insights:
                        st.info(f"• {insight}")
            else:
                st.error(f"Analysis Error: {analysis_result.get('error')}")
        else:
            st.warning("No valid market data available for statistical analysis.")
    else:
        st.info("🧮 No market data found. Run a research task with stock data to see statistics!")