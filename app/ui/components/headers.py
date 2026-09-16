"""Hero Page Header Component for AcadAssist."""

import streamlit as st
from app.ui.components.common import get_asset_base64


def render_page_header(
    tag: str,
    title_html: str,
    subtitle: str,
    banner_key: str,
) -> None:
    """Render the standard editorial page header with the authentic banner asset.

    Args:
        tag: Uppercase small category label (e.g. 'MY KNOWLEDGE').
        title_html: HTML formatted title string with accented word.
        subtitle: Descriptive subtitle string.
        banner_key: Unique identifier matching extracted banner image (e.g. 'dashboard').
    """
    banner_img_file = f"header_{banner_key}.png"
    banner_b64 = get_asset_base64(banner_img_file)
    
    banner_html = (
        f'<div class="hero-banner-col"><img src="{banner_b64}" class="hero-banner-img" alt="{tag}" /></div>'
        if banner_b64
        else ""
    )
    
    st.markdown(
        f"""
        <div class="hero-header-card">
            <div class="hero-text-col">
                <div class="hero-tag">{tag}</div>
                <h1 class="hero-title">{title_html}</h1>
                <p class="hero-subtitle">{subtitle}</p>
            </div>
            {banner_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
