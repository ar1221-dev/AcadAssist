"""Sidebar navigation component for AcadAssist.

Follows strict design guidelines:
- Deep forest green theme (#111c16)
- Consistent branding and icons
- Exact items (NO Profile item in sidebar)
- Active item highlight pill
- Exactly ONE motivational quote in the sidebar bottom
"""

import streamlit as st
from app.ui.components.common import get_asset_base64, SVG_ICONS
from app.ui.components.quotes import get_quote_for_page

NAV_ITEMS_MAIN = [
    ("Dashboard", "Dashboard", ":material/home:"),
    ("My Knowledge", "My Knowledge", ":material/menu_book:"),
    ("Assessment", "Assessment", ":material/assignment:"),
    ("Study Planner", "Study Planner", ":material/calendar_month:"),
    ("AI Study Assistant", "AI Study Assistant", ":material/auto_awesome:"),
    ("Progress", "Progress", ":material/bar_chart:"),
]

NAV_ITEMS_SECONDARY = [
    ("Settings", "Settings", ":material/settings:"),
    ("Help & Support", "Help & Support", ":material/help:"),
]


def render_sidebar() -> None:
    """Render the global sidebar component."""
    logo_data = get_asset_base64("logo.png")
    sidebar_bg_data = get_asset_base64("sidebar_bg.png")
    
    current_page = st.session_state.get("current_page", "Dashboard")
    
    with st.sidebar:
        # Brand Header
        logo_html = f'<img src="{logo_data}" class="brand-logo-img" alt="AcadAssist" />' if logo_data else ''
        st.markdown(
            f"""
            <div class="sidebar-brand">
                {logo_html}
                <div class="brand-text">
                    <h1>AcadAssist</h1>
                    <p>Learn · Plan · Practice · Grow</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Primary Navigation Group
        for page_name, label, icon in NAV_ITEMS_MAIN:
            is_active = current_page == page_name
            btn_key = f"nav_btn_{page_name}"
            btn_type = "primary" if is_active else "secondary"
                
            if st.button(label, key=btn_key, use_container_width=True, type=btn_type, icon=icon):
                if st.session_state.current_page != page_name:
                    st.session_state.current_page = page_name
                    st.rerun()
            
        # Divider
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Secondary Navigation Group
        for page_name, label, icon in NAV_ITEMS_SECONDARY:
            is_active = current_page == page_name
            btn_key = f"nav_btn_{page_name}"
            btn_type = "primary" if is_active else "secondary"
                
            if st.button(label, key=btn_key, use_container_width=True, type=btn_type, icon=icon):
                if st.session_state.current_page != page_name:
                    st.session_state.current_page = page_name
                    st.rerun()
            
        # Bottom Quote Box
        bg_style = f"background-image: url('{sidebar_bg_data}'); background-size: cover; background-position: bottom left;" if sidebar_bg_data else ""
        
        st.markdown(
            f"""
            <div class="sidebar-bottom-box" style="{bg_style}">
                <div class="sidebar-quote-text" style="font-family: 'Playfair Display', serif; font-size: 0.85rem; line-height: 1.4; color: #c2cec6; margin-bottom: 12px; font-weight: 600;">
                    DISCIPLINE TURNS<br/>GOALS INTO RESULTS.
                </div>
                <div class="sidebar-quote-line" style="width: 30px; height: 2px; background-color: #b89768; margin-bottom: 14px;"></div>
                <div class="sidebar-version" style="font-size: 0.65rem; color: #5d6f64; font-weight: 500;">AcadAssist v0.1.0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
