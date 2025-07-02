"""Results display page for the Multi-Agent AI System."""
import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ui.question_answering import generate_question_answer
from src.ui.utils.server_utils import get_base_url, get_recent_tasks
from src.ui.utils.session_utils import has_results, get_last_result, clear_results


def render_results_page(server_online):
    """Render the results page - Enhanced with improved layout."""
    st.header("📊 Research Results")
    st.caption("View and analyze your research findings with advanced insights")

    if has_results():
        _render_research_results()
    else:
        _render_no_results_message(server_online)


def _render_research_results():
    """Render the research results."""
    result = get_last_result()

    # Header info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", result.get("status", "Unknown").title())
    with col2:
        st.metric("Task ID", result.get("task_id", "N/A")[:8] + "...")
    with col3:
        if "execution_time" in result:
            st.metric("Completed", "✅")

    st.divider()

    # Extract user questions and task data
    task_data = result.get("input_data", {})
    user_questions = task_data.get("questions", [])

    if user_questions:
        _render_question_answers(user_questions, result)
        st.divider()

    if "results" in result:
        results = result["results"]
        _render_research_findings(results)
        _render_analysis_results(results)
        _render_report(results)

    _render_action_buttons(result)
    
    # Enhanced analytics section
    st.divider()
    st.subheader("🚀 Enhanced Analytics")
    st.write("Get advanced statistical analysis, visualizations, and predictive insights!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Enhanced Analytics", use_container_width=True, key="btn_enhanced_analytics"):
            st.switch_page("pages/enhanced_results.py")
    
    with col2:
        st.info("💡 **New Features:** Statistical analysis, data visualization, forecasting, and custom algorithms!")


def _render_question_answers(user_questions, result):
    """Render direct answers to user questions."""
    st.subheader("❓ Your Questions - Answered")

    # Get research findings for answering questions
    research_findings = {}
    if "results" in result and "research" in result["results"]:
        research_data = result["results"]["research"]
        if research_data.get("status") == "success":
            research_findings = research_data.get("research_findings", {})

    for i, question in enumerate(user_questions, 1):
        st.markdown(f"**Question {i}:** {question}")
        answer = generate_question_answer(question, research_findings, result)
        st.success(f"**Answer:** {answer}")
        st.write("")


def _render_research_findings(results):
    """Render research findings section."""
    if "research" not in results:
        return

    research = results["research"]
    st.subheader("🔍 Research Findings")

    if research.get("status") == "success":
        findings = research.get("research_findings", {})

        # Data sources used
        data_sources = findings.get("data_sources", [])
        if data_sources:
            st.success(f"📡 **Data Sources Used:** {', '.join(data_sources)}")

        # Key findings
        key_findings = findings.get("key_findings", [])
        if key_findings:
            st.write("**🔑 Key Findings:**")
            for i, finding in enumerate(key_findings, 1):
                st.write(f"{i}. {finding}")

        # Market data
        if findings.get("market_data"):
            _render_market_data(findings["market_data"])

        # News summary
        if findings.get("news_summary"):
            st.subheader("📰 Recent News")
            st.info(findings["news_summary"])

        # Web insights
        web_insights = findings.get("web_insights", [])
        if web_insights:
            _render_web_insights(web_insights)

    else:
        st.error(f"Research failed: {research.get('error', 'Unknown error')}")


def _render_market_data(market_data):
    """Render market data as a table."""
    st.subheader("💰 Market Data")
    
    market_df_data = [
        {
            "Company": stock.get("company_name", stock.get("symbol", "Unknown")),
            "Symbol": stock.get("symbol", "N/A"),
            "Price": f"${stock.get('current_price', 'N/A')}",
            "30d Change (%)": f"{stock.get('price_change_30d', 0):+.1f}%",
            "Sector": stock.get("sector", "N/A"),
        }
        for stock in market_data if "error" not in stock
    ]

    if market_df_data:
        st.dataframe(pd.DataFrame(market_df_data), use_container_width=True)


def _render_web_insights(web_insights):
    """Render web insights section."""
    st.subheader("🌐 Web Research")
    for insight in web_insights:
        with st.expander(f"📄 {insight.get('title', 'Web Result')}"):
            st.write(f"**URL:** {insight.get('url', 'N/A')}")
            st.write(f"**Summary:** {insight.get('summary', 'No summary available')}")
            for key in ["content", "date", "source"]:
                if insight.get(key):
                    st.write(f"**{key.title()}:** {insight[key]}")


def _render_analysis_results(results):
    """Render analysis results section."""
    if "analysis" not in results:
        return

    analysis = results["analysis"]
    st.subheader("📈 Analysis Results")

    if analysis.get("status") == "success":
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            st.write("**💡 Recommendations:**")
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")

        insights = analysis.get("insights", [])
        if insights:
            st.write("**🧠 Key Insights:**")
            for insight in insights:
                if isinstance(insight, dict):
                    st.write(f"• **{insight.get('type', 'Insight')}**: {insight.get('description', '')}")
                else:
                    st.write(f"• {insight}")


def _render_report(results):
    """Render the generated report section."""
    if "report" not in results:
        return

    report = results["report"]
    st.subheader("📄 Generated Report")

    if report.get("status") == "success":
        exec_summary = report.get("executive_summary", "")
        if exec_summary and "failed" not in exec_summary.lower():
            st.markdown("**Executive Summary:**")
            st.info(exec_summary)

        full_report = report.get("report", "")
        if full_report:
            with st.expander("📋 View Full Report"):
                st.markdown(full_report)

        metadata = report.get("metadata", {})
        if metadata:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Report Type", metadata.get("report_type", "N/A").replace("_", " ").title())
            with col2:
                st.metric("Target Audience", metadata.get("target_audience", "N/A").replace("_", " ").title())
            with col3:
                st.metric("Word Count", metadata.get("word_count", "N/A"))


def _render_action_buttons(result):
    """Render action buttons."""
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Run New Research", use_container_width=True, key="btn_new_research"):
            clear_results()
            st.rerun()
    
    with col2:
        if st.button("🔍 Go to Research Tab", use_container_width=True, key="btn_go_research"):
            st.switch_page("pages/research_tool.py")
    
    with col3:
        if st.button("📥 Download Report", use_container_width=True, key="btn_download"):
            _handle_download_report(result)
    
    with col4:
        if st.button("🔗 View in API", use_container_width=True, key="btn_view_api"):
            st.markdown(f"[Open in API Docs]({get_base_url()}/docs)")


def _handle_download_report(result):
    """Handle report download."""
    if "results" in result and "report" in result["results"]:
        report_content = result["results"]["report"].get("report", "No report content")
        st.download_button(
            label="Download as Text",
            data=report_content,
            file_name=f"research_report_{result['task_id'][:8]}.txt",
            mime="text/plain",
        )


def _render_no_results_message(server_online):
    """Render message when no results are available."""
    st.info("👈 Run a research task in the 'Research Tool' tab to see results here!")

    if server_online:
        st.subheader("📋 Recent Tasks")
        try:
            tasks = get_recent_tasks()
            if tasks:
                for task in tasks[:5]:
                    with st.expander(f"Task {task['task_id'][:8]} - {task['status']}"):
                        st.write(f"**Topic:** {task.get('input_data', {}).get('topic', 'Unknown')}")
                        st.write(f"**Status:** {task['status']}")
                        st.write(f"**Created:** {task.get('created_at', 'Unknown')}")
            else:
                st.write("No recent tasks found.")
        except Exception as e:
            st.error(f"Could not load recent tasks: {e}")