"""Settings page for the Multi-Agent AI System."""
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ui.utils.server_utils import get_base_url, get_server_health, get_recent_tasks, test_server_connection


def render_settings_page(server_online):
    """Render the settings page - Enhanced with better organization."""
    st.header("🛠️ System Settings")
    st.caption("Configure and monitor your Multi-Agent AI System")

    if server_online:
        _render_server_info()

    st.divider()
    _render_system_config()
    
    st.divider()
    _render_quick_actions()


def _render_server_info():
    """Render server information section."""
    st.subheader("🖥️ Server Information")
    
    try:
        health_data = get_server_health()
        if health_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("System Status", health_data.get("status", "Unknown").title())
            with col2:
                st.metric("Version", health_data.get("version", "Unknown"))
            with col3:
                st.metric("Environment", "Development")

            services = health_data.get("services", {})
            if services:
                st.subheader("🔧 Services Status")
                for service, status in services.items():
                    if status == "healthy":
                        st.write(f"✅ {service.title()}: {status}")
                    else:
                        st.write(f"❌ {service.title()}: {status}")
        else:
            st.error("Could not retrieve server health information")
    except Exception as e:
        st.error(f"Could not retrieve server information: {e}")


def _render_system_config():
    """Render system configuration section."""
    st.subheader("📊 System Configuration")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**API Endpoints:**\n- Health Check: `/health`\n- Execute Task: `/tasks/execute`\n- List Tasks: `/tasks`\n- Agent Info: `/agents`")

    with col2:
        st.markdown("**Data Sources:**\n- Web Search: DuckDuckGo API\n- Market Data: Yahoo Finance\n- News: RSS Feeds\n- Encyclopedia: Wikipedia API")


def _render_quick_actions():
    """Render quick actions section."""
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    base_url = get_base_url()

    with col1:
        if st.button("📋 View API Docs", use_container_width=True, key="btn_api_docs"):
            st.markdown(f"[Open API Documentation]({base_url}/docs)")

    with col2:
        if st.button("🔄 Test Connection", use_container_width=True, key="btn_test_conn"):
            _test_connection()

    with col3:
        if st.button("📈 System Stats", use_container_width=True, key="btn_system_stats"):
            _show_system_stats()

def _test_connection():
    """Test server connection and show result."""
    result = test_server_connection()
    if result["success"]:
        st.write("✅ Connection successful")
    else:
        st.write("❌ Connection failed")


def _show_system_stats():
    """Show system statistics."""
    try:
        tasks = get_recent_tasks()
        st.write(f"📊 Total tasks: {len(tasks)}")
    except Exception as e:
        st.write(f"❌ Could not retrieve stats: {e}")