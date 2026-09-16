"""Global Topbar component for AcadAssist."""

import streamlit as st
from app.ui.components.common import get_asset_base64, SVG_ICONS


def render_topbar() -> None:
    """Render the top search and user profile bar."""
    avatar_data = get_asset_base64("avatar_topbar.png")
    if not avatar_data:
        avatar_data = get_asset_base64("avatar_profile.png")
        
    col_search, col_actions = st.columns([2.5, 1.3])
    
    with col_search:
        st.markdown(
            f"""
            <div class="search-box-pill">
                {SVG_ICONS["search"]}
                <input type="text" placeholder="Search your notes, topics, or ask anything..." />
                <span class="search-shortcut-badge">Ctrl K</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col_actions:
        action_col1, action_col2, action_col3 = st.columns([0.8, 0.6, 2.2])
        
        with action_col1:
            # Theme toggle pill
            st.markdown(
                f"""
                <div class="icon-btn-pill" title="Toggle Theme">
                    {SVG_ICONS["sun"]}
                    <span style="font-size: 0.72rem; font-weight: 500;">Light</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        with action_col2:
            # Notifications bell
            st.markdown(
                f"""
                <div class="icon-btn-pill notification-badge-wrap" title="Notifications">
                    {SVG_ICONS["bell"]}
                    <span class="notification-dot"></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        with action_col3:
            # Profile trigger button navigating to Profile page
            current_page = st.session_state.get("current_page", "Dashboard")
            is_on_profile = current_page == "Profile"
            
            profile_btn_label = "👤 Raj (Profile)" if not is_on_profile else "✓ Raj (Active)"
            
            # Render avatar and name with interactive Streamlit button
            if st.button(profile_btn_label, key="topbar_profile_btn", use_container_width=True):
                st.session_state.current_page = "Profile"
                st.rerun()
