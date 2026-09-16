"""Profile page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_milestone_banner
from app.ui.components.charts import render_progress_bar
from app.ui.components.common import get_asset_base64



def render_profile() -> None:
    """Render the User Profile page."""
    avatar_b64 = get_asset_base64("avatar_profile.png")
    
    # Initialize state aliases
    profile = st.session_state.get("user_profile", {})
    subjects = st.session_state.get("subjects", [])
    recent_activities = st.session_state.get("recent_activities", [])
    badges = st.session_state.get("badges", [])
    study_goals = st.session_state.get("study_goals", [])

    # 1. Hero Header
    render_page_header(
        tag="MY PROFILE",
        title_html='Same Student. Brighter <span class="accent-word">Tomorrow.</span>',
        subtitle="Track your journey, showcase your progress, and stay motivated.",
        banner_key="profile",
    )
    
    # 2. Profile Summary Card & Right Quote/Streak
    top_col1, top_col2 = st.columns([2.2, 1.1])
    
    with top_col1:
        avatar_img_html = f'<img src="{avatar_b64}" style="width: 96px; height: 96px; border-radius: 50%; object-fit: cover; border: 3px solid #ffffff; box-shadow: var(--shadow-md);" alt="Avatar" />' if avatar_b64 else '<div style="width: 96px; height: 96px; border-radius: 50%; background: #2d5f47; color: white; display: flex; align-items: center; justify-content: center; font-size: 2rem;">R</div>'
        
        tags_html = "".join([f'<span class="badge-tag badge-tag-sage">{t}</span>' for t in profile.get('tags', [])])
        
        st.markdown(
            f"""
            <div class="acad-card" style="display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 18px;">
                    <div style="position: relative;">
                        {avatar_img_html}
                        <span style="position: absolute; bottom: 2px; right: 2px; background: #ffffff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; box-shadow: var(--shadow-sm); border: 1px solid #d1d5db;">📷</span>
                    </div>
                    <div>
                        <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #16221c;">{profile.get('name', '')}</div>
                        <div style="font-size: 0.8rem; font-weight: 600; color: #3b4741;">{profile.get('role', '')}</div>
                        <div style="font-size: 0.75rem; color: #728078;">{profile.get('field', '')}</div>
                        <div style="font-size: 0.78rem; color: #526058; margin-top: 6px; max-width: 480px; line-height: 1.4;">{profile.get('bio', '')}</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;">
                            {tags_html}
                        </div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("✏️ Edit Profile", key="profile_edit_btn")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with top_col2:
        # Personal Quote card
        st.markdown(
            f"""
            <div class="acad-card" style="margin-bottom: 12px; padding: 14px 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.74rem; font-weight: 700; color: #2d5f47; letter-spacing: 0.04em;">“ YOUR QUOTE</span>
                    <span style="font-size: 0.74rem; color: #2d5f47; cursor: pointer;">✏️</span>
                </div>
                <div style="font-family: 'Playfair Display', serif; font-size: 0.95rem; font-style: italic; color: #18261e; margin-top: 6px; line-height: 1.35;">
                    “{profile.get('quote', 'Keep pushing forward.')}”
                </div>
            </div>
            
            <div class="acad-card" style="padding: 14px 16px; cursor: pointer;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5rem;">🔥</span>
                        <div>
                            <div style="font-size: 0.72rem; color: #728078;">Study Streak</div>
                            <div style="font-size: 1.2rem; font-weight: 800; color: #15221b;">{profile.get('streak_days', 0)} days</div>
                            <div style="font-size: 0.68rem; color: #2d5f47; font-weight: 600;">{profile.get('streak_status', '')}</div>
                        </div>
                    </div>
                    <span style="color: #2d5f47; font-size: 1.1rem; font-weight: 700;">›</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # 3. Middle 3-Column Info Layout
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        # Personal Information
        st.markdown(
            f"""
            <div class="section-header-wrap">
                <div class="section-title">👤 Personal Information</div>
                <span class="section-link">Edit</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px; font-size: 0.78rem;">
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb;">
                    <span style="color: #6f7c75;">✉️ Email</span>
                    <strong style="color: #15221b;">{profile.get('email', '') or '--'}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb;">
                    <span style="color: #6f7c75;">🎓 Academic Level</span>
                    <strong style="color: #15221b;">{profile.get('academic_level', '') or '--'}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb;">
                    <span style="color: #6f7c75;">📖 Field of Study</span>
                    <strong style="color: #15221b;">{profile.get('field', '') or '--'}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb;">
                    <span style="color: #6f7c75;">📍 Location</span>
                    <strong style="color: #15221b;">{profile.get('location', '') or '--'}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0;">
                    <span style="color: #6f7c75;">📅 Member Since</span>
                    <strong style="color: #15221b;">{profile.get('member_since', '') or '--'}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with m_col2:
        # Goals
        goals_html = ""
        for g in study_goals[:3]:
            color = "#10b981" if g["completed"] else "#f59e0b"
            goals_html += f'''
                <div style="padding: 6px 0; border-bottom: 1px solid #f2f0eb;">
                    <div style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: {color};">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: {color};"></span>
                        Goal
                    </div>
                    <div style="color: #3b4841; margin-top: 2px;">{g['text']}</div>
                </div>
            '''
        if not study_goals:
            goals_html = '<div style="color: #728078; font-style: italic; padding: 6px 0;">No goals set yet.</div>'
            
        st.markdown(
            f"""
            <div class="section-header-wrap">
                <div class="section-title">🎯 Goals</div>
                <span class="section-link">Edit</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px; font-size: 0.78rem;">
                {goals_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with m_col3:
        # Interests
        interests_html = "".join([f'<span class="badge-tag badge-tag-sage">{t}</span>' for t in profile.get('tags', [])])
        if not profile.get('tags'):
            interests_html = '<div style="color: #728078; font-style: italic; font-size: 0.78rem;">No interests added.</div>'
            
        st.markdown(
            f"""
            <div class="section-header-wrap">
                <div class="section-title">💚 Interests</div>
                <span class="section-link">Edit</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                    {interests_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    # 4. Bottom 3-Column: Achievements, Subjects, Recent Activity
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        # Achievements & Badges
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🏆 Achievements & Badges</div>
                <span class="section-link">View All →</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div style="font-size: 1.5rem;">🔥</div>
                        <div style="font-size: 0.68rem; font-weight: 700; color: #16221c; margin-top: 2px;">7-Day<br/>Streak</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem;">🎯</div>
                        <div style="font-size: 0.68rem; font-weight: 700; color: #16221c; margin-top: 2px;">100<br/>Questions</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem;">📖</div>
                        <div style="font-size: 0.68rem; font-weight: 700; color: #16221c; margin-top: 2px;">First<br/>Note</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem;">📁</div>
                        <div style="font-size: 0.68rem; font-weight: 700; color: #16221c; margin-top: 2px;">5<br/>Subjects</div>
                    </div>
                    <div style="opacity: 0.4;">
                        <div style="font-size: 1.5rem;">🔒</div>
                        <div style="font-size: 0.68rem; font-weight: 700; color: #16221c; margin-top: 2px;">Assess<br/>Pro</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with b_col2:
        # Subjects Overview
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📊 Subjects Overview</div>
                <span class="section-link">View All →</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px;">
            """,
            unsafe_allow_html=True,
        )
        if not subjects:
            st.markdown('<div style="color: #728078; font-style: italic; font-size: 0.78rem; text-align: center; padding: 10px 0;">No subjects added.</div>', unsafe_allow_html=True)
        for s in subjects[:5]:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; font-size: 0.74rem; font-weight: 600; color: #15221b;">
                    <span>{s['name']}</span>
                    <span>{s['progress']}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_progress_bar(s["progress"], color=s["color"], height=5)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with b_col3:
        # Recent Activity
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Recent Activity</div>
                <span class="section-link">View All →</span>
            </div>
            <div class="acad-card" style="margin-bottom: 16px;">
            """,
            unsafe_allow_html=True,
        )
        from app.ui.components.cards import render_activity_list
        if not recent_activities:
            st.markdown('<div style="color: #728078; font-style: italic; font-size: 0.78rem; text-align: center; padding: 10px 0;">No recent activity.</div>', unsafe_allow_html=True)
        else:
            render_activity_list(recent_activities[:3])
        
    # Milestone Banner
    if render_milestone_banner(
        tag="KEEP LEARNING. KEEP GROWING.",
        title="Your future self will thank you.",
        subtitle="Every session counts towards mastery.",
        button_text="Continue Learning",
        button_key="profile_continue_btn",
    ):
        st.session_state.current_page = "Dashboard"
        st.rerun()
