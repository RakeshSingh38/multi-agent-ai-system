"""Action buttons component for enhanced results page."""
import streamlit as st
import json
import pandas as pd
from typing import Dict, Any


def render_action_buttons(results: Dict[str, Any]):
    """Render action buttons for the results."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔍 New Research", use_container_width=True, key="btn_new_research_enhanced"):
            try:
                # Clear session state manually
                st.session_state["last_result"] = None
                st.session_state["show_results"] = False
                st.switch_page("pages/research_tool.py")
            except Exception as e:
                st.error(f"Could not start new research: {e}")
                st.info("Try refreshing the page manually.")

    with col2:
        if st.button("📊 Standard Results", use_container_width=True, key="btn_standard_results"):
            try:
                st.switch_page("pages/results.py")
            except Exception as e:
                st.error(f"Could not navigate to results: {e}")
                st.info("Try refreshing the page manually.")

    with col3:
        # Download enhanced results
        if st.button("💾 Download Results", use_container_width=True, key="btn_download_enhanced"):
            # Create enhanced results JSON
            enhanced_results = {
                "timestamp": pd.Timestamp.now().isoformat(),
                "analysis_type": "enhanced",
                "results": results
            }

            json_str = json.dumps(enhanced_results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"enhanced_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="btn_download_json_enhanced"
            )

    with col4:
        # API documentation link
        try:
            from src.ui.utils.server_utils import get_base_url
            base_url = get_base_url()
            if st.button("📚 API Docs", use_container_width=True, key="btn_api_docs_enhanced"):
                st.markdown(f"[Open API Documentation]({base_url}/docs)")
        except:
            st.info("API documentation not available")