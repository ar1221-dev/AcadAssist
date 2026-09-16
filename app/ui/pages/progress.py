"""Progress page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_stat_metric
from app.ui.components.charts import (
    render_progress_bar,
    render_weekly_barchart,
    render_activity_donut,
    render_progress_line_chart,
)



def render_progress() -> None:
    """Render the Progress analytics page."""
    # Initialize state aliases
    stats = st.session_state.get("stats", {})
    subjects = st.session_state.get("subjects", [])
    study_goals = st.session_state.get("study_goals", [])
    milestones = st.session_state.get("milestones", [])
    profile = st.session_state.get("user_profile", {})
    name = profile.get("name", "Raj").split(" ")[0]

    # 1. Hero Header
    render_page_header(
        tag="YOUR PROGRESS",
        title_html='Small Steps. Big <span class="accent-word">Progress.</span>',
        subtitle="Track your learning journey, stay consistent, and become the best version of yourself.",
        banner_key="progress",
    )
    
    # 2. 5 Stat Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_stat_metric("82", "Notes Learned", "↑ 12% this month", "📖", "#eef8f2", "#2d5f47")
    with c2:
        render_stat_metric("143", "Questions Practiced", "↑ 28% this month", "✅", "#eef8f2", "#10b981")
    with c3:
        render_stat_metric(f"{stats.get('hours_studied', 0)} hrs", "Total Study Time", "↑ 16% this month", "⏱️", "#fff7ed", "#ea580c")
    with c4:
        render_stat_metric(str(stats.get('day_streak', 0)), "Day Streak", "Keep it going!", "🔥", "#fef2f2", "#ef4444")
    with c5:
        render_stat_metric("78%", "Overall Progress", "↑ 10% this month", "🎯", "#fdf2f8", "#db2777")
        
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    # 3. Three-Column Analytics Layout
    col_left, col_mid, col_right = st.columns([1.2, 1.3, 1.1])
    
    with col_left:
        # Subject Progress
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📊 Subject Progress</div>
                <span class="section-link">View Details →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        for subj in subjects:
            st.markdown(
                f"""
                <div style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #15221b;">
                        <span>{subj['full_name']}</span>
                        <span>{subj['progress']}%</span>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            render_progress_bar(subj["progress"], color=subj["color"], height=6)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Progress Over Time Chart
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📈 Progress Over Time</div>
                <span style="font-size: 0.72rem; color: #6a7770; background: #f1efe9; padding: 2px 8px; border-radius: 6px;">Last 30 Days</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card">', unsafe_allow_html=True)
        render_progress_line_chart()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_mid:
        # Weekly Study Time Bar Chart
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Study Time</div>
                <span style="font-size: 0.72rem; color: #6a7770; background: #f1efe9; padding: 2px 8px; border-radius: 6px;">This Month</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        weekly_data = [
            ("Mon", 2.8),
            ("Tue", 5.0),
            ("Wed", 5.2),
            ("Thu", 6.8),
            ("Fri", 3.4),
            ("Sat", 4.6),
            ("Sun", 5.8),
        ]
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        render_weekly_barchart(weekly_data)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Activity Distribution Donut Chart
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🏆 Activity Distribution</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        activities = [
            ("Reading Notes", 40, "#193828"),
            ("Practicing Questions", 30, "#4e7d65"),
            ("Taking Assessments", 15, "#e07a5f"),
            ("Using AI Assistant", 10, "#d97706"),
            ("Other", 5, "#9ca3af"),
        ]
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        render_activity_donut(activities, total_time="24.5 hrs")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mountain landscape quote card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1b2e23 0%, #294635 100%); border-radius: 12px; padding: 18px 22px; color: #ffffff; box-shadow: var(--shadow-sm);">
                <div style="font-size: 1.4rem; color: #9ab4a4; font-family: serif; line-height: 1;">“</div>
                <div style="font-family: 'Playfair Display', serif; font-size: 1.05rem; font-style: italic; line-height: 1.4; color: #e5eee8; margin-top: 2px;">
                    Discipline today leads to opportunities tomorrow.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col_right:
        # Your Goals
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🎯 Your Goals</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        for goal in study_goals:
            icon = "✅" if goal["completed"] else "○"
            col_text = "#6b7280; text-decoration: line-through;" if goal["completed"] else "#1f2937;"
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f2f0eb; font-size: 0.8rem;">
                    <span>{icon}</span>
                    <span style="color: {col_text} font-weight: 500;">{goal['text']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Milestones
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🏆 Milestones</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        for m in milestones:
            node_color = "#10b981" if m["completed"] else "#d1d5db"
            st.markdown(
                f"""
                <div style="display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f2f0eb;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: {node_color}; margin-top: 4px; flex-shrink: 0;"></div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 600; color: #17241d;">{m['title']}</div>
                        <div style="font-size: 0.7rem; color: #78857e;">{m['date']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Encouragement card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #101c15 0%, #1e3327 100%); border-radius: 12px; padding: 18px; color: #ffffff; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-family: 'Playfair Display', serif; font-size: 0.98rem; font-weight: 700; margin-bottom: 2px;">You're doing great, {name}.</div>
                    <div style="font-size: 0.72rem; color: #b2c4ba;">Keep going. Your future self will thank you.</div>
                </div>
                <div style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center;">
                    →
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
