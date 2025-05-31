"""Session state management utilities for the Multi-Agent AI System."""
import streamlit as st


def init_session_state():
    """Initialize session state variables - Enhanced with additional tracking."""
    defaults = {
        "selected_template": None, "topic": "", "questions": [], "show_results": False,
        "last_result": None, "research_in_progress": False, "current_task_id": None,
        "page_refreshed": False, "session_start_time": "2025-05-31T20:15:42Z",
        "user_preferences": {}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_template(template_key, templates):
    """Set the selected template and update session state."""
    if template_key in templates:
        template = templates[template_key]
        st.session_state.update({
            "selected_template": template_key,
            "topic": template["topic"],
            "questions": template["questions"]
        })

def store_research_result(result):
    """Store research result in session state."""
    st.session_state.update({
        "last_result": result, "show_results": True,
        "research_in_progress": False, "current_task_id": None
    })

def set_research_in_progress(task_id):
    """Set research as in progress."""
    st.session_state.update({"research_in_progress": True, "current_task_id": task_id})

def cancel_research():
    """Cancel ongoing research and clear state."""
    st.session_state.update({"research_in_progress": False, "current_task_id": None})

def is_research_in_progress():
    """Check if research is currently in progress."""
    return st.session_state.get("research_in_progress", False)

def get_current_task_id():
    """Get the current task ID if research is in progress."""
    return st.session_state.get("current_task_id")

def clear_results():
    """Clear stored results from session state."""
    st.session_state.update({"show_results": False, "last_result": None})

def has_results():
    """Check if there are results to display."""
    return st.session_state.get("show_results") and st.session_state.get("last_result")

def get_last_result():
    """Get the last research result."""
    return st.session_state.get("last_result")