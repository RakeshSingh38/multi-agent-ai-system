"""Enhanced results page with advanced analytics and visualizations."""
import streamlit as st
import json
import pandas as pd
from typing import Dict, Any, List
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import tab modules
from pages.tabs.overview_tab import render_overview_tab
from pages.tabs.visualizations_tab import render_visualizations_tab
from pages.tabs.predictions_tab import render_predictions_tab
from pages.tabs.statistics_tab import render_statistics_tab
from pages.tabs.custom_analysis_tab import render_custom_analysis_tab

# Import components
from pages.components.action_buttons import render_action_buttons

def render_enhanced_results():
    """Render the enhanced results page with advanced analytics - Simplified for performance."""
    st.title("📊 Enhanced Analytics Results")
    
    # Get research results
    results = st.session_state.get("last_result")
    if not results:
        st.warning("No research results found. Please run a research task first.")
        return
    
    # Simplified display
    st.info("Enhanced analytics temporarily simplified for system optimization")


# Main execution - Call the function when the page loads
if __name__ == "__main__":
    render_enhanced_results()
else:
    # When imported as a module (for Streamlit multi-page apps)
    render_enhanced_results()