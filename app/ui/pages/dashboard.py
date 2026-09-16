"""Dashboard page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_stat_metric, render_milestone_banner
from app.ui.components.charts import render_progress_bar
from app.ui.components.common import SVG_ICONS
from app.ui.state import toggle_task_completion


def render_dashboard() -> None:
    """Render the main Dashboard page."""
    # Initialize state aliases for cleaner code
    stats = st.session_state.get("stats", {})
    
    # 1. Hero Header
    render_page_header(
        tag="Tue, 16 Sept 2026",
        title_html='Good morning, <span class="accent-word">Raj.</span>',
        subtitle="Consistent effort today, stronger results tomorrow.",
        banner_key="dashboard",
    )
    
    # 2. Stat Metric Cards
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        render_stat_metric(
            str(stats.get("day_streak", 0)),
            "Day Streak",
            "Keep it going!",
            "🔥",
            "#fdf0eb",
            "#d96b34",
        )
    with c2:
        render_stat_metric(
            str(stats.get("topics_completed", 0)),
            "Topics Completed",
            "This week",
            "🎯",
            "#eef8f2",
            "#2d5f47",
        )
    with c3:
        render_stat_metric(
            f"{stats.get('hours_studied', 0)}",
            "Hours Studied",
            "This week",
            "⏱️",
            "#edf3fc",
            "#2b6cb0",
        )
    with c4:
        render_stat_metric(
            f"{stats.get('average_score', 0)}%",
            "Average Score",
            "Across assessments",
            "📊",
            "#f3f0fb",
            "#6b46c1",
        )
        
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    # 3. Two-Column Dashboard Layout
    col_left, col_right = st.columns([1.9, 1.2], gap="large")
    
    with col_left:
        # Today's Study Plan Section
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">
                    📅 Today's Study Plan
                </div>
                <span class="section-link">View full plan →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Render study plan timeline items
        plan_box = st.container()
        today_plan = st.session_state.get("today_plan", [])
        
        with plan_box:
            for item in today_plan:
                is_done = item["status"] == "completed"
                check_badge = "✓" if is_done else "○"
                badge_bg = "#eef8f2" if is_done else "#f1f3f2"
                check_color = "#2d5f47" if is_done else "#9ca3af"
                btn_label = item["action_label"] if not is_done else "Done"
                
                is_last = item == today_plan[-1]
                line_html = '<div style="position: absolute; top: 34px; left: 10px; width: 2px; height: 110px; background-color: #eae8e2; z-index: -1;"></div>' if not is_last else ''
                
                t_col1, t_col2, t_col3 = st.columns([0.8, 3.2, 0.9])
                with t_col1:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.82rem; font-weight: 600; color: #4b5563; padding-top: 10px; position: relative;">
                            {line_html}
                            <span style="display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: {badge_bg}; color: {check_color}; font-weight: 700; z-index: 2;">{check_badge}</span>
                            <span style="margin-top: 2px;">{item['time']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with t_col2:
                    st.markdown(
                        f"""
                        <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; opacity: {'0.6' if is_done else '1'};">
                            <div style="display: flex; align-items: center; justify-content: space-between;">
                                <span style="font-size: 0.88rem; font-weight: 700; color: #16221c; text-decoration: {'line-through' if is_done else 'none'};">{item['title']}</span>
                                <div style="display: flex; gap: 6px;">
                                    <span class="badge-tag badge-tag-sage">{item['tag']}</span>
                                    <span style="font-size: 0.74rem; color: #718077;">{item['duration']}</span>
                                </div>
                            </div>
                            <div style="font-size: 0.76rem; color: #606c64; margin-top: 3px;">{item['description']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with t_col3:
                    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                    if st.button(btn_label, key=f"plan_btn_{item['id']}", use_container_width=True, type="secondary" if is_done else "primary"):
                        toggle_task_completion(item["id"], is_planner=False)
                        st.rerun()
                        
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        
        # Subject Progress Section
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">
                    📊 Subject Progress
                </div>
                <span class="section-link">View detailed analytics →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        sc1, sc2, sc3 = st.columns(3, gap="small")
        subjects = st.session_state.get("subjects", [])
        from app.ui.components.cards import render_subject_card
        
        for idx, col in enumerate([sc1, sc2, sc3]):
            if idx < len(subjects):
                subj = subjects[idx]
                with col:
                    render_subject_card(subj)
                
        # Milestone bottom banner
        if render_milestone_banner(
            tag="NEXT MILESTONE",
            title="Stay consistent, Raj.",
            subtitle="You're building a stronger, smarter you.",
            button_text="Keep Going",
            button_key="dash_milestone_btn",
        ):
            st.session_state.current_page = "Progress"
            st.rerun()
            
    with col_right:
        # Upcoming Exams
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">
                    📅 Upcoming Exams
                </div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        upcoming_exams = st.session_state.get("upcoming_exams", [])
        from app.ui.components.cards import render_exam_list
        if upcoming_exams:
            render_exam_list(upcoming_exams)
        else:
            from app.ui.components.common import render_empty_state
            render_empty_state("No upcoming exams", "📅")
        
        # Quick Actions
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">
                    ⚡ Quick Actions
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        qa_col1, qa_col2 = st.columns(2, gap="small")
        with qa_col1:
            if st.button("📄  Upload Notes\n\nAdd new material", key="dash_qa_notes", use_container_width=True):
                st.session_state.current_page = "My Knowledge"
                st.rerun()
            if st.button("✦  Ask AI Assistant\n\nGet instant help", key="dash_qa_ai", use_container_width=True):
                st.session_state.current_page = "AI Study Assistant"
                st.rerun()
                
        with qa_col2:
            if st.button("🎯  Take a Quiz\n\nPractice now", key="dash_qa_quiz", use_container_width=True):
                st.session_state.current_page = "Assessment"
                st.rerun()
            if st.button("📅  Plan My Study\n\nCreate schedule", key="dash_qa_plan", use_container_width=True):
                st.session_state.current_page = "Study Planner"
                st.rerun()
                
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        
        # Recent Activity
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">
                    ⏱️ Recent Activity
                </div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        recent_activities = st.session_state.get("recent_activities", [])
        from app.ui.components.cards import render_activity_list
        if recent_activities:
            render_activity_list(recent_activities[:3])
        else:
            from app.ui.components.common import render_empty_state
            render_empty_state("No recent activity", "⏱️")
