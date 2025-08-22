"""Overview tab for enhanced results page."""
import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_overview_tab(results: Dict[str, Any]):
    """Render the overview tab with key metrics and summary."""
    st.subheader("📈 Analysis Overview")

    # Display basic result info
    st.write(f"**Status:** {results.get('status', 'Unknown').title()}")
    st.write(f"**Task ID:** {results.get('task_id', 'N/A')}")

    # Extract research findings
    research_findings = results.get("results", {}).get("research", {}).get("research_findings", {})

    if research_findings:
        # Key findings
        key_findings = research_findings.get("key_findings", [])
        if key_findings:
            st.subheader("🔑 Key Findings")
            for i, finding in enumerate(key_findings[:5], 1):
                st.write(f"**{i}.** {finding}")

        # Market data summary
        market_data = research_findings.get("market_data", [])
        if market_data:
            st.subheader("💰 Market Data Summary")
            st.write(f"**Data Points:** {len(market_data)}")

            # Show sample data
            market_df_data = [
                {
                    "Company": stock.get("company_name", stock.get("symbol", "Unknown")),
                    "Symbol": stock.get("symbol", "N/A"),
                    "Price": f"${stock.get('current_price', 'N/A')}",
                    "30d Change (%)": f"{stock.get('price_change_30d', 0):+.1f}%",
                }
                for stock in market_data[:5] if "error" not in stock
            ]

            if market_df_data:
                st.dataframe(pd.DataFrame(market_df_data), use_container_width=True)

        # News summary
        news_summary = research_findings.get("news_summary")
        if news_summary:
            st.subheader("📰 News Summary")
            st.info(news_summary)

    # Analysis results
    if "analysis_results" in results.get("results", {}):
        analysis = results["results"]["analysis_results"]

        # Key insights
        if "key_insights" in analysis:
            st.subheader("💡 Key Insights")
            insights = analysis["key_insights"]
            if isinstance(insights, list):
                for i, insight in enumerate(insights[:5], 1):
                    st.write(f"**{i}.** {insight}")

        # Recommendations
        if "recommendations" in analysis:
            st.subheader("🎯 Recommendations")
            recommendations = analysis["recommendations"]
            if isinstance(recommendations, list):
                for i, rec in enumerate(recommendations[:5], 1):
                    st.write(f"**{i}.** {rec}")