"""Research Tool page for the Multi-Agent AI System."""

import streamlit as st
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ui.components import render_template_buttons, render_research_form
from src.ui.utils.server_utils import get_base_url, submit_research_task, cancel_task
from src.ui.utils.session_utils import (
    set_template, store_research_result, set_research_in_progress, 
    cancel_research, is_research_in_progress, get_current_task_id
)
from src.core.config import settings


def render_research_tool_page(server_online):
    """Render the research tool page."""
    st.header("🔍 Real Data Research Tool")

    if not server_online:
        st.error("⚠️ API server is not running. Please start it to use the research tool.")
        st.code(f"uvicorn src.api.main:app --reload --host {settings.api_host} --port {settings.api_port}")
        return

    _handle_page_refresh()
    if is_research_in_progress():
        _show_research_in_progress_warning()

    st.subheader("⚡ Quick Examples")
    templates, selected_template = render_template_buttons()
    if selected_template:
        set_template(selected_template, templates)
        st.rerun()

    st.divider()
    st.subheader("🎯 Custom Research")
    form_data = render_research_form()

    if form_data["submitted"] and form_data["topic"]:
        _handle_research_submission(form_data)
    elif form_data["submitted"]:
        st.error("Please enter a research topic!")


def _handle_research_submission(form_data):
    """Handle research form submission."""
    task_data = {k: form_data[k] for k in ["task_type", "topic", "questions", "analysis_type", "report_type", "target_audience"]}
    
    with st.spinner("🔄 Multi-Agent System is researching with REAL DATA..."):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            _show_submission_progress(progress_bar, status_text)
            response = submit_research_task(task_data)

            if response.status_code == 200:
                result = response.json()
                task_id = result.get("task_id")
                set_research_in_progress(task_id)
                _show_research_progress(progress_bar, status_text)
                store_research_result(result)

                progress_bar.progress(100)
                status_text.text("🎉 Research completed successfully!")
                st.write(f"✅ Research completed! Task ID: {task_id}")
                
                base_url = get_base_url()
                st.markdown(f"🔗 **View API Details:** [{base_url}/tasks/{task_id}]({base_url}/tasks/{task_id})")
                
                if st.button("📊 Go to Results Tab", use_container_width=True, key="btn_go_results_from_submission"):
                    st.switch_page("pages/results.py")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
            cancel_research()


def _show_research_progress(progress_bar, status_text):
    """Show dynamic progress messages during research - Optimized for performance."""
    messages = [
        "🔍 Research Agent: Gathering data from web sources...",
        "📊 Analysis Agent: Processing market data and insights...",
        "📝 Report Writer: Creating professional analysis report...",
        "✅ Finalizing results and generating answers...",
    ]

    for i, message in enumerate(messages):
        status_text.text(message)
        progress_value = 10 + int((i + 1) / len(messages) * 85)
        progress_bar.progress(min(progress_value, 95))
        time.sleep(0.8)


def _show_submission_progress(progress_bar, status_text):
    """Show dynamic progress messages during submission."""
    messages = [
        "📡 Submitting to Multi-Agent System...",
        "🔄 Initializing research agents...",
        "⚡ Connecting to analysis pipeline...",
        "🚀 Starting multi-agent workflow...",
        "📊 Preparing research parameters...",
        "🔍 Activating research protocols...",
    ]

    for i, message in enumerate(messages):
        status_text.text(message)
        progress_value = 5 + int((i + 1) / len(messages) * 15)
        progress_bar.progress(min(progress_value, 20))
        time.sleep(3)


def _handle_page_refresh():
    """Handle page refresh by canceling ongoing research."""
    if is_research_in_progress():
        task_id = get_current_task_id()
        if task_id:
            try:
                response = cancel_task(task_id)
                status = "cancelled" if response.status_code in [200, 404] else "unable to cancel"
                st.warning(f"🔄 Page refreshed - Previous research operation was {status}.")
            except Exception as e:
                st.warning(f"🔄 Page refreshed - Could not cancel previous research: {str(e)}")
            cancel_research()


def _show_research_in_progress_warning():
    """Show warning when research is in progress."""
    task_id = get_current_task_id()
    st.warning(f"⚠️ Research is currently in progress (Task ID: {task_id[:8]}...). Please wait for completion or refresh to cancel.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh to Cancel", use_container_width=True, key="btn_refresh_cancel"):
            st.rerun()
    with col2:
        if st.button("📊 Check Results", use_container_width=True, key="btn_check_results"):
            st.switch_page("pages/results.py")
