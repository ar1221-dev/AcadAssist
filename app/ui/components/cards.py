"""Card components for AcadAssist."""

from typing import Optional
import streamlit as st
from app.ui.components.common import get_asset_base64, SVG_ICONS


def render_stat_metric(
    number: str,
    label: str,
    sublabel: str,
    icon_char: str,
    bg_color: str,
    icon_color: str,
) -> None:
    """Render a clean stat metric card with icon in pastel circle."""
    st.markdown(
        f"""
        <div class="stat-metric-card">
            <div class="stat-icon-circle" style="background-color: {bg_color}; color: {icon_color};">
                {icon_char}
            </div>
            <div class="stat-info">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-sublabel">{sublabel}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_milestone_banner(
    tag: str,
    title: str,
    subtitle: str,
    button_text: str,
    button_key: str,
) -> bool:
    """Render the panoramic dark mountain milestone banner."""
    milestone_b64 = get_asset_base64("milestone_banner.png")
    
    col_text, col_btn = st.columns([3.5, 1])
    
    with col_text:
        bg_img_html = f'<img src="{milestone_b64}" class="milestone-bg-img" alt="Milestone" />' if milestone_b64 else ""
        st.markdown(
            f"""
            <div class="milestone-banner-box" style="margin-top: 1rem; margin-bottom: 0.5rem;">
                {bg_img_html}
                <div class="milestone-content">
                    <div class="milestone-tag">{tag}</div>
                    <div class="milestone-title">{title}</div>
                    <div class="milestone-subtitle">{subtitle}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col_btn:
        # Button aligned nicely with milestone banner
        st.write("")
        st.write("")
        return st.button(f"{button_text} →", key=button_key, use_container_width=True)

def render_subject_card(subj: dict) -> None:
    """Render a standard subject progress card."""
    from app.ui.components.charts import render_progress_bar
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; padding: 14px; box-shadow: var(--shadow-sm); height: 100%;">
            <div style="font-size: 0.84rem; font-weight: 700; color: #15221b;">{subj['name']}</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #15221b; margin: 4px 0;">{subj['progress']}%</div>
        """,
        unsafe_allow_html=True,
    )
    render_progress_bar(subj["progress"], color=subj["color"], height=6)
    st.markdown(
        f"""
            <div style="font-size: 0.72rem; color: #728078; margin-top: 4px;">{subj['topics_completed']} / {subj['total_topics']} topics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_activity_list(activities: list) -> None:
    """Render a card containing a list of activity timeline items."""
    items_html = ""
    for act in activities:
        items_html += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f2f0eb;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background-color: {act['icon_color']};"></span>
                <span style="font-size: 0.8rem; color: #233128; font-weight: 500;">{act['text']}</span>
            </div>
            <span style="font-size: 0.72rem; color: #7f8b84;">{act['time']}</span>
        </div>
        """
    st.markdown(f'<div class="acad-card" style="margin-bottom: 16px;">{items_html}</div>', unsafe_allow_html=True)

def render_exam_list(exams: list) -> None:
    """Render a card containing a list of upcoming exams."""
    items_html = ""
    for exam in exams:
        badge_class = "badge-tag-peach" if exam.get("urgency") == "high" else "badge-tag-blue"
        items_html += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f2f0eb;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1rem;">📄</span>
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #15221b;">{exam['subject']}</div>
                    <div style="font-size: 0.72rem; color: #7b8880;">{exam['date_str']}</div>
                </div>
            </div>
            <span class="badge-tag {badge_class}">{exam['days_left']} days</span>
        </div>
        """
    st.markdown(f'<div class="acad-card" style="margin-bottom: 16px;">{items_html}</div>', unsafe_allow_html=True)
