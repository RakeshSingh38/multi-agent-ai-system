"""Custom analysis tab for enhanced results page."""
import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_custom_analysis_tab(results: Dict[str, Any], stat_analyzer):
    """Render the custom analysis tab with algorithm results."""
    st.subheader("⚙️ Custom Algorithm Analysis")

    # Extract market data
    market_data = results.get("results", {}).get("research", {}).get("research_findings", {}).get("market_data", [])

    if market_data:
        valid_data = [stock for stock in market_data if "error" not in stock and stock.get("current_price")]

        if valid_data:
            # Trend analysis
            st.subheader("📈 Trend Analysis")

            trend_data = [{"price": float(stock.get("current_price", 0))} for stock in valid_data if stock.get("current_price")]

            if len(trend_data) >= 3:
                trend_result = stat_analyzer.analyze_trends(trend_data, metric="price")

                if "error" not in trend_result:
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        trend_dir = trend_result.get("trend_direction", "unknown")
                        trend_icon = "📈" if trend_dir == "increasing" else "📉" if trend_dir == "decreasing" else "➡️"
                        st.metric("Trend Direction", f"{trend_icon} {trend_dir.title()}")

                    with col2:
                        total_change = trend_result.get("total_change_percent", 0)
                        st.metric("Total Change", f"{total_change:+.2f}%")

                    with col3:
                        significance = trend_result.get("statistical_significance", False)
                        sig_text = "✅ Significant" if significance else "⚠️ Not Significant"
                        st.metric("Statistical Significance", sig_text)

                    # Detailed metrics
                    with st.expander("📊 Detailed Trend Metrics"):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.write(f"**Slope:** {trend_result.get('slope', 0):.4f}")
                            st.write(f"**Correlation:** {trend_result.get('correlation', 0):.4f}")

                        with col2:
                            st.write(f"**P-Value:** {trend_result.get('p_value', 0):.4f}")
                            st.write(f"**Mean:** ${trend_result.get('mean', 0):.2f}")

                        with col3:
                            std_dev_val = trend_result.get('std_deviation', 0)
                            # Handle NaN values
                            if pd.isna(std_dev_val) or std_dev_val is None:
                                std_dev_val = 0.0
                            st.write(f"**Std Dev:** ${std_dev_val:.2f}")
                            st.write(f"**Data Points:** {trend_result.get('data_points', 0)}")

            # Correlation analysis
            st.subheader("🔗 Correlation Analysis")

            corr_data = []
            for stock in valid_data:
                try:
                    corr_data.append({
                        "price": float(stock.get("current_price", 0)),
                        "change_30d": float(stock.get("price_change_30d", 0))
                    })
                except:
                    continue

            if len(corr_data) >= 3:
                corr_result = stat_analyzer.calculate_correlations(corr_data)

                if "error" not in corr_result:
                    strong_corr = corr_result.get("strong_correlations", [])

                    if strong_corr:
                        st.success(f"Found {len(strong_corr)} strong correlations")

                        for corr in strong_corr:
                            var1 = corr.get("variable1", "")
                            var2 = corr.get("variable2", "")
                            corr_value = corr.get("correlation", 0)
                            strength = corr.get("strength", "moderate")

                            st.write(f"**{var1}** ↔️ **{var2}**")
                            st.write(f"Correlation: {corr_value:.3f} ({strength})")
                            st.markdown("---")
                    else:
                        st.info("No strong correlations detected (threshold: |r| > 0.7)")

                    # Correlation matrix
                    with st.expander("📊 Full Correlation Matrix"):
                        corr_matrix = corr_result.get("correlation_matrix", {})
                        if corr_matrix:
                            st.write(pd.DataFrame(corr_matrix))

            # Market sentiment
            st.subheader("💭 Market Sentiment Analysis")

            positive_count = len([s for s in valid_data if float(s.get("price_change_30d", 0)) > 0])
            negative_count = len([s for s in valid_data if float(s.get("price_change_30d", 0)) < 0])
            neutral_count = len([s for s in valid_data if float(s.get("price_change_30d", 0)) == 0])

            total = positive_count + negative_count + neutral_count

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📈 Bullish", f"{positive_count} ({positive_count/total*100:.0f}%)")
            with col2:
                st.metric("📉 Bearish", f"{negative_count} ({negative_count/total*100:.0f}%)")
            with col3:
                st.metric("➡️ Neutral", f"{neutral_count} ({neutral_count/total*100:.0f}%)")
        else:
            st.warning("No valid market data available for custom analysis.")
    else:
        st.info("⚙️ No market data found. Run a research task with stock data to see custom analysis!")