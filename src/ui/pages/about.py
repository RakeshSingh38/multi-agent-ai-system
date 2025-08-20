"""About page for the Multi-Agent AI System."""
import streamlit as st


def render_about_page():
    """Render the about page."""
    st.header("📖 About Multi-Agent AI System")

    st.markdown("## 🔥 Enhanced with REAL DATA!")
    st.markdown(
        "This Multi-Agent AI System now gathers **actual information** from the internet to provide you with current, relevant research and analysis."
    )

    col1, col2 = st.columns(2)

    with col1:
        _render_agents_info()
        _render_data_sources_info()

    with col2:
        _render_features_info()
        _render_use_cases_info()

    st.divider()
    _render_architecture_diagram()


def _render_agents_info():
    """Render information about AI agents."""
    st.subheader("🤖 AI Agents")
    st.markdown("- **Research Agent**: Gathers REAL data from web, news, market sources\n- **Analysis Agent**: Processes and analyzes collected information\n- **Report Writer**: Creates professional, structured reports\n- **Task Coordinator**: Orchestrates the entire workflow")

def _render_data_sources_info():
    """Render information about data sources."""
    st.subheader("📡 Real Data Sources")
    st.markdown("- **🌐 Web Search**: DuckDuckGo search results\n- **💰 Market Data**: Yahoo Finance (stocks, crypto)\n- **📰 News**: RSS feeds from CNN, BBC, Reuters\n- **📖 Wikipedia**: Encyclopedia articles\n- **🔍 Web Scraping**: Full webpage content")

def _render_features_info():
    """Render information about key features."""
    st.subheader("✨ Key Features")
    st.markdown("- **Multi-Agent Collaboration**: Specialized agents work together\n- **Real-Time Data**: Live information from the internet\n- **Market Intelligence**: Current stock prices and trends\n- **News Analysis**: Latest articles and developments\n- **Professional Reports**: Executive summaries and detailed analysis")

def _render_use_cases_info():
    """Render information about use cases."""
    st.subheader("💼 Use Cases")
    st.markdown("- **Investment Research**: Stock analysis with real prices\n- **Market Intelligence**: Industry trends and competitor analysis\n- **Business Strategy**: Data-driven decision making\n- **Academic Research**: Current information gathering\n- **News Monitoring**: Latest developments tracking")


def _render_architecture_diagram():
    """Render the system architecture diagram."""
    st.subheader("🏗️ System Architecture")
    st.code(
        """
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ Research Agent  │────▶│ Analysis Agent  │────▶│  Report Writer  │
    │ (REAL DATA)     │     │                 │     │                 │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                     ▼
                              Task Coordinator
                                     │
                              ┌──────┴──────┐
                              │   Database  │
                              │ (SQLite)    │
                              └─────────────┘
    """
    )