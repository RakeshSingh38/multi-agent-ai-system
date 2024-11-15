"""
Multi-Agent AI System - Main Streamlit Application
Split into modular components for better maintainability.
Enhanced with improved error handling and performance optimizations.
"""
import streamlit as st
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.ui.components import (
    render_custom_css, 
    render_header, 
    render_server_status_bar,
    render_data_sources_info,
    render_footer
)
from pages.research_tool import render_research_tool_page
from pages.results import render_results_page
from pages.enhanced_results import render_enhanced_results
from pages.about import render_about_page
from pages.settings import render_settings_page
from src.ui.utils.server_utils import check_server_status
from src.ui.utils.session_utils import init_session_state


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Multi-Agent AI System | Intelligent Research Platform", 
        page_icon="🤖", 
        layout="wide"
    )

    # Initialize session state
    init_session_state()

    # Render custom CSS
    render_custom_css()

    # Header
    render_header()

    # Check server status
    server_status = check_server_status()
    server_online = server_status["online"]

    # Server status bar
    render_server_status_bar(server_status)

    # Data sources info
    render_data_sources_info(server_online)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Research Tool", 
        "📊 Results",
        "📈 Enhanced Analytics",
        "📖 About", 
        "🛠️ Settings"
    ])

    with tab1:
        render_research_tool_page(server_online)

    with tab2:
        render_results_page(server_online)
    
    with tab3:
        render_enhanced_results()

    with tab4:
        render_about_page()

    with tab5:
        render_settings_page(server_online)

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
