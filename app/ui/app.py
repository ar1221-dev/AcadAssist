"""AcadAssist - Premium AI Study Assistant Streamlit Frontend.

Main application entrypoint routing modular pages and maintaining global design consistency.
"""

import os
import sys

# Ensure repository root is in sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import streamlit as st

# 1. Page Configuration (must be called first)
st.set_page_config(
    page_title="AcadAssist - AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Import components & pages
from app.ui.components.common import load_global_css
from app.ui.components.sidebar import render_sidebar
from app.ui.components.topbar import render_topbar

from app.ui.pages.dashboard import render_dashboard
from app.ui.pages.knowledge import render_knowledge
from app.ui.pages.assessment import render_assessment
from app.ui.pages.planner import render_planner
from app.ui.pages.assistant import render_assistant
from app.ui.pages.progress import render_progress
from app.ui.pages.settings import render_settings
from app.ui.pages.help_support import render_help_support
from app.ui.pages.profile import render_profile

# 3. Session State Initialization
from app.ui.state import init_session_state
init_session_state()
load_global_css()

# 5. Global Navigation Sidebar
render_sidebar()

# 6. Global Topbar
render_topbar()

# 7. Page Router
PAGES = {
    "Dashboard": render_dashboard,
    "My Knowledge": render_knowledge,
    "Assessment": render_assessment,
    "Study Planner": render_planner,
    "AI Study Assistant": render_assistant,
    "Progress": render_progress,
    "Settings": render_settings,
    "Help & Support": render_help_support,
    "Profile": render_profile,
}

current_page = st.session_state.get("current_page", "Dashboard")
render_fn = PAGES.get(current_page, render_dashboard)
render_fn()
