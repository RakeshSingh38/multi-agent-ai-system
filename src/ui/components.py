"""Reusable UI components for the Multi-Agent AI System."""

import streamlit as st
from src.ui.utils.server_utils import get_base_url
from src.core.config import settings


def render_custom_css():
    """Render custom CSS styles - Enhanced with modern design."""
    st.markdown(
        """
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .modern-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the clean, professional header - Simplified for performance."""
    st.markdown(
        """
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 0.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 600; margin: 0; color: #1e293b;">
            🤖 Multi-Agent AI System
        </h1>
        <p style="font-size: 1rem; margin: 0.25rem 0 0 0; color: #64748b;">
            Intelligent Research & Analysis Platform
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_server_status_bar(server_status):
    """Render the server status bar."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Server Status:** {server_status['status']}")
    with col2:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
        if not server_status["online"]:
            st.error(
                f"Start server: `uvicorn src.api.main:app --reload --host {settings.api_host} --port {settings.api_port}`"
            )


def render_data_sources_info(server_online):
    """Render data sources information box."""
    if server_online:
        st.success("✅ **System Online** - Real-time data integration active")
    else:
        st.error("⚠️ **API Server Offline** - Start the FastAPI server to enable real-time data features")


def render_template_buttons():
    """Render quick template buttons and return templates configuration."""
    templates = {
        "tesla": {
            "button": "🚗 Tesla Stock Analysis",
            "topic": "Tesla stock performance and market trends",
            "questions": [
                "What is Tesla's current stock price?",
                "How is Tesla performing vs competitors?",
                "What recent news affects Tesla?",
            ],
        },
        "real_estate": {
            "button": "🏠 Real Estate Market",
            "topic": "US housing market trends October 2025",
            "questions": [
                "Are house prices rising?",
                "What are mortgage rates?",
                "Which cities are hottest?",
            ],
        },
        "ai_news": {
            "button": "🤖 AI Industry News",
            "topic": "Artificial Intelligence industry developments 2025",
            "questions": [
                "Latest AI breakthroughs?",
                "Which AI companies are growing?",
                "AI market valuations?",
            ],
        },
    }

    cols = st.columns(3)
    selected_template = None

    for i, (key, template) in enumerate(templates.items()):
        with cols[i]:
            if st.button(template["button"], use_container_width=True):
                selected_template = key

    return templates, selected_template


def render_research_form():
    """Render the research form and return form data."""
    with st.form("research_form"):
        topic = st.text_input(
            "📝 Research Topic",
            value=st.session_state.get("topic", ""),
            placeholder="e.g., Apple iPhone 15 sales performance",
            help="Enter any topic you want to research with real data",
        )

        st.write("❓ Specific Questions (optional)")
        questions = []
        template_selected = st.session_state.get("selected_template", None)

        for i in range(3):
            default_q = (
                st.session_state.get("questions", ["", "", ""])[i]
                if i < len(st.session_state.get("questions", []))
                else ""
            )
            key_suffix = f"_{template_selected}" if template_selected else ""
            q = st.text_input(
                f"Question {i+1}", value=default_q, key=f"q_{i}{key_suffix}"
            )
            if q:
                questions.append(q)

        with st.expander("⚙️ Advanced Settings"):
            col1, col2 = st.columns(2)
            with col1:
                analysis_type = st.selectbox(
                    "Analysis Type",
                    [
                        "market_analysis",
                        "competitive_analysis",
                        "technology_assessment",
                        "risk_assessment",
                        "trend_analysis",
                        "industry_analysis",
                    ],
                )
                task_type = st.selectbox(
                    "Task Type",
                    ["full_analysis", "quick_research"],
                    help="full_analysis: comprehensive multi-source research, quick_research: faster results",
                )

            with col2:
                report_type = st.selectbox(
                    "Report Type",
                    [
                        "executive_summary",
                        "detailed_report",
                        "market_report",
                        "technical_report",
                        "investment_brief",
                    ],
                )
                target_audience = st.selectbox(
                    "Target Audience",
                    [
                        "executives",
                        "investors",
                        "technical",
                        "general",
                        "marketing_professionals",
                        "financial_analysts",
                    ],
                )

        submitted = st.form_submit_button(
            "🚀 Start Research", use_container_width=True, type="primary"
        )

        return {
            "submitted": submitted,
            "topic": topic,
            "questions": questions,
            "analysis_type": analysis_type,
            "task_type": task_type,
            "report_type": report_type,
            "target_audience": target_audience,
        }


def render_footer():
    """Render the clean footer."""
    st.divider()
    st.markdown(
        """
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem; padding: 1rem;'>
        <div style='margin-bottom: 0.5rem;'>
            <strong>🤖 Multi-Agent AI System</strong> • Intelligent Research Platform
        </div>
        <div>
            Built with Streamlit & FastAPI •
            <a href='https://github.com/RakeshSingh38/multi-agent-ai-system' style='color: #3b82f6; text-decoration: none;'>View on GitHub</a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
