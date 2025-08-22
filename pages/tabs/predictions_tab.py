"""Predictions tab for enhanced results page."""
import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_predictions_tab(results: Dict[str, Any], pred_analyzer):
    """Render the predictions tab with forecasting results."""
    st.subheader("🔮 Predictive Analysis")

    # Extract market data
    market_data = results.get("results", {}).get("research", {}).get("research_findings", {}).get("market_data", [])

    if market_data:
        valid_data = [stock for stock in market_data if "error" not in stock and stock.get("current_price")]

        if len(valid_data) >= 3:
            # Perform market forecast
            forecast_result = pred_analyzer.market_forecast(valid_data, periods=3)

            if "error" not in forecast_result:
                # Display forecast results
                st.subheader("📊 Market Forecast (Next 3 Months)")

                forecast_data = forecast_result.get("market_forecast", {})
                forecasted_prices = forecast_data.get("forecasted_prices", [])
                periods = forecast_data.get("periods", [])

                if forecasted_prices:
                    forecast_df = pd.DataFrame({
                        "Period": periods,
                        "Forecasted Average Price": [f"${price:.2f}" for price in forecasted_prices]
                    })
                    st.dataframe(forecast_df, use_container_width=True)

                    # Key metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        current_avg = forecast_data.get("current_average_price", 0)
                        st.metric("Current Avg Price", f"${current_avg:.2f}")
                    with col2:
                        expected_change = forecast_data.get("expected_change_rate", 0)
                        st.metric("Expected Monthly Change", f"{expected_change:+.1f}%")
                    with col3:
                        final_price = forecasted_prices[-1] if forecasted_prices else 0
                        price_diff = final_price - current_avg if current_avg > 0 else 0
                        st.metric("3-Month Projection", f"${final_price:.2f}", f"{price_diff:+.2f}")

                # Market indicators
                st.subheader("📈 Market Indicators")
                indicators = forecast_result.get("market_indicators", {})

                col1, col2, col3 = st.columns(3)
                with col1:
                    volatility = indicators.get("volatility", 0)
                    st.metric("Volatility", f"{volatility:.2f}%")
                with col2:
                    sentiment_ratio = indicators.get("positive_sentiment_ratio", 0)
                    st.metric("Bullish Stocks", f"{sentiment_ratio*100:.0f}%")
                with col3:
                    stability = indicators.get("market_stability", "unknown")
                    st.metric("Market Stability", stability.title())

                # Insights
                insights = pred_analyzer.generate_forecast_insights(forecast_result)
                if insights:
                    st.subheader("🔍 Forecast Insights")
                    for insight in insights:
                        st.info(f"• {insight}")

                # Individual predictions
                st.subheader("📊 Individual Stock Forecasts")
                for stock in valid_data[:5]:
                    current_price = float(stock.get("current_price", 0))
                    change_30d = float(stock.get("price_change_30d", 0))
                    company = stock.get("company_name", "Unknown")

                    if current_price > 0 and change_30d != 0:
                        predicted_price = current_price * (1 + change_30d/100)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{company}**")
                        with col2:
                            st.write(f"Current: ${current_price:.2f}")
                        with col3:
                            trend_icon = "📈" if predicted_price > current_price else "📉"
                            st.write(f"Predicted: ${predicted_price:.2f} {trend_icon}")

                st.warning("⚠️ Predictions are based on historical trends and statistical models.")
            else:
                st.error(f"Forecast Error: {forecast_result.get('error')}")
        else:
            st.warning(f"Need at least 3 stocks for forecasting. Currently have {len(valid_data)}.")
    else:
        st.info("🔮 No market data found. Run a research task with stock data to see predictions!")