"""Settings page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_milestone_banner



def render_settings() -> None:
    """Render the Settings and Preferences page."""
    # 1. Hero Header
    render_page_header(
        tag="SETTINGS",
        title_html='Customize Your <span class="accent-word">Experience.</span>',
        subtitle="Tailor AcadAssist to match your goals, preferences, and workflow.",
        banner_key="settings",
    )
    
    # 2. Tabs
    tabs = [
        "General",
        "Study Preferences",
        "Notifications",
        "Appearance",
        "Account",
        "Data & Privacy",
        "Integrations",
    ]
    st.radio("Settings Tabs", tabs, horizontal=True, label_visibility="collapsed")
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # 3. Two-Column Layout
    col_left, col_right = st.columns([2.1, 1.2])
    
    with col_left:
        # General Settings Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 18px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                    <span style="font-size: 1.2rem;">👤</span>
                    <div>
                        <div style="font-size: 0.96rem; font-weight: 700; color: #15221b;">General Settings</div>
                        <div style="font-size: 0.74rem; color: #728078;">Set up your basic preferences.</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        g_c1, g_c2 = st.columns(2)
        profile = st.session_state.get("user_profile", {})
        with g_c1:
            name_val = st.text_input("Name", value=profile.get("name", "Raj"))
            email_val = st.text_input("Email", value=profile.get("email", ""))
        with g_c2:
            acad_val = st.selectbox("Academic Level", ["Undergraduate (B.E)", "Postgraduate (M.Tech)", "High School", "Doctoral"], index=0)
            field_val = st.selectbox("Field of Study", ["Computer Science (AI & ML)", "Information Technology", "Data Science", "Electronics"], index=0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Study Preferences Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 18px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                    <span style="font-size: 1.2rem;">📖</span>
                    <div>
                        <div style="font-size: 0.96rem; font-weight: 700; color: #15221b;">Study Preferences</div>
                        <div style="font-size: 0.74rem; color: #728078;">Customize how AcadAssist helps you learn.</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        p_c1, p_c2 = st.columns(2)
        with p_c1:
            st.selectbox("Default Study Duration", ["25 minutes", "40 minutes", "50 minutes", "90 minutes"], index=2)
            st.selectbox("Preferred Difficulty Level", ["Easy", "Medium", "Hard"], index=1)
        with p_c2:
            st.markdown("<label style='font-size: 0.82rem; font-weight: 600; color: #374151;'>Active Subjects</label>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;">
                    <span class="badge-tag badge-tag-sage">Data Structures</span>
                    <span class="badge-tag badge-tag-sage">DBMS</span>
                    <span class="badge-tag badge-tag-sage">Computer Networks</span>
                    <span class="badge-tag badge-tag-sage">Java</span>
                    <span class="badge-tag badge-tag-sage">AI & ML</span>
                    <span class="badge-tag badge-tag-sage">Operating Systems</span>
                    <span class="badge-tag" style="background: #f1efe9; cursor: pointer;">+ Add Subject</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Notifications Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 18px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                    <span style="font-size: 1.2rem;">🔔</span>
                    <div>
                        <div style="font-size: 0.96rem; font-weight: 700; color: #15221b;">Notifications</div>
                        <div style="font-size: 0.74rem; color: #728078;">Choose what updates you want to receive.</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        n_c1, n_c2 = st.columns(2)
        settings = st.session_state.get("settings", {})
        with n_c1:
            settings["daily_reminders"] = st.checkbox("Daily Study Reminder (stay on track)", value=settings.get("daily_reminders", True))
            st.checkbox("Upcoming Exam Alerts", value=True)
            st.checkbox("Study Streak Updates", value=True)
        with n_c2:
            st.checkbox("Assessment Feedback", value=True)
            st.checkbox("Weekly Progress Report", value=True)
            settings["email_summaries"] = st.checkbox("Email Summaries", value=settings.get("email_summaries", False))
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bottom milestone banner
        if render_milestone_banner(
            tag="YOUR LEARNING. YOUR WAY.",
            title="Small settings. A big difference.",
            subtitle="Personalize, focus, and make the most of your journey.",
            button_text="Save Changes",
            button_key="settings_save_btn",
        ):
            st.success("Settings saved successfully!")
            
    with col_right:
        # Appearance Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span>🎨</span>
                    <div>
                        <div style="font-size: 0.92rem; font-weight: 700; color: #16221c;">Appearance</div>
                        <div style="font-size: 0.72rem; color: #728078;">Make it look and feel right for you.</div>
                    </div>
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: #374151; margin: 10px 0 4px 0;">Theme</div>
            """,
            unsafe_allow_html=True,
        )
        st.radio("Appearance Theme", ["Light", "Dark", "System"], horizontal=True, label_visibility="collapsed")
        st.markdown(
            """
                <div style="font-size: 0.78rem; font-weight: 600; color: #374151; margin: 12px 0 6px 0;">Accent Color</div>
                <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #2d5f47; border: 2px solid #111e17; cursor: pointer;"></span>
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #6366f1; cursor: pointer;"></span>
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #0ea5e9; cursor: pointer;"></span>
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #f59e0b; cursor: pointer;"></span>
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #ef4444; cursor: pointer;"></span>
                    <span style="width: 22px; height: 22px; border-radius: 50%; background: #ec4899; cursor: pointer;"></span>
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: #374151; margin: 8px 0 4px 0;">Font Size</div>
            """,
            unsafe_allow_html=True,
        )
        st.radio("Font Size", ["Small", "Medium", "Large"], index=1, horizontal=True, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Account Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span>🛡️</span>
                    <div>
                        <div style="font-size: 0.92rem; font-weight: 700; color: #16221c;">Account</div>
                        <div style="font-size: 0.72rem; color: #728078;">Manage your account and security.</div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <span>🔒 Change Password</span>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <span>🛡️ Two-Factor Authentication</span>
                        <span style="color: #ef4444; font-size: 0.72rem;">Not enabled ›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <span>💻 Manage Sessions</span>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; color: #ef4444; font-weight: 600; cursor: pointer;">
                        <span>🗑️ Delete Account</span>
                        <span>›</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Data & Privacy Card
        st.markdown(
            """
            <div class="acad-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span>🔒</span>
                    <div>
                        <div style="font-size: 0.92rem; font-weight: 700; color: #16221c;">Data & Privacy</div>
                        <div style="font-size: 0.72rem; color: #728078;">Control your data and privacy settings.</div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <span>📂 Manage Your Data</span>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <span>📥 Export My Notes</span>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 6px 0; cursor: pointer;">
                        <span>🗑️ Clear Chat History</span>
                        <span>›</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
