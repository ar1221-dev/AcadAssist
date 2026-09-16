"""Help & Support page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_milestone_banner



def render_help_support() -> None:
    """Render the Help & Support center page."""
    # Initialize state aliases
    help_categories = st.session_state.get("help_categories", [])
    system_status = st.session_state.get("system_status", [])

    # 1. Hero Header
    render_page_header(
        tag="HELP & SUPPORT",
        title_html='We\'re Here to <span class="accent-word">Help.</span>',
        subtitle="Find answers, get support, and make the most of AcadAssist.",
        banner_key="help_support",
    )
    
    # 2. Two-Column Layout
    col_left, col_right = st.columns([2.1, 1.2])
    
    with col_left:
        # Search Help Center Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: #eef8f2; color: #2d5f47; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
                        🔍
                    </div>
                    <div>
                        <div style="font-size: 1rem; font-weight: 700; color: #15221b;">Search Help Center</div>
                        <div style="font-size: 0.76rem; color: #728078;">Find answers to common questions, guides, and troubleshooting steps.</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        
        s_c1, s_c2 = st.columns([3.5, 1])
        with s_c1:
            st.text_input("Search query", placeholder="Search for help (e.g., 'how to upload notes', 'quiz not working')...", label_visibility="collapsed")
        with s_c2:
            st.button("Search", key="help_search_btn", use_container_width=True)
            
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 10px; font-size: 0.74rem;">
                <span style="color: #6a766f; font-weight: 600;">Popular:</span>
                <span class="action-chip">Upload Notes</span>
                <span class="action-chip">Create Quiz</span>
                <span class="action-chip">Study Planner</span>
                <span class="action-chip">Account & Login</span>
                <span class="action-chip">AI Assistant</span>
                <span class="action-chip">Data & Privacy</span>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Browse Help Topics
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🧭 Browse Help Topics</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        row1_cols = st.columns(4)
        for idx, cat in enumerate(help_categories[:4]):
            with row1_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; padding: 12px; margin-bottom: 12px; box-shadow: var(--shadow-sm); min-height: 115px; cursor: pointer;">
                        <span style="font-size: 1.1rem;">📁</span>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #16221c; margin-top: 4px;">{cat['title']}</div>
                        <div style="font-size: 0.68rem; color: #728078; margin-top: 2px;">{cat['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
        row2_cols = st.columns(4)
        for idx, cat in enumerate(help_categories[4:]):
            with row2_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; padding: 12px; margin-bottom: 12px; box-shadow: var(--shadow-sm); min-height: 115px; cursor: pointer;">
                        <span style="font-size: 1.1rem;">⚙️</span>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #16221c; margin-top: 4px;">{cat['title']}</div>
                        <div style="font-size: 0.68rem; color: #728078; margin-top: 2px;">{cat['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
        # Milestone Banner
        render_milestone_banner(
            tag="STILL HAVE QUESTIONS?",
            title="Learning is a journey, and you're not alone.",
            subtitle="We're here to support you at every step.",
            button_text="Contact Support",
            button_key="help_milestone_btn",
        )
        
    with col_right:
        # Get in Touch
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span>✉️</span>
                    <div>
                        <div style="font-size: 0.92rem; font-weight: 700; color: #16221c;">Get in Touch</div>
                        <div style="font-size: 0.72rem; color: #728078;">Still need help? Reach out to our support team.</div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <div>
                            <div style="font-weight: 600; color: #16221c;">Send a Support Request</div>
                            <div style="font-size: 0.68rem; color: #74817a;">We usually respond within 24 hours.</div>
                        </div>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f2f0eb; cursor: pointer;">
                        <div>
                            <div style="font-weight: 600; color: #16221c;">Live Chat (Beta)</div>
                            <div style="font-size: 0.68rem; color: #74817a;">Chat with our support assistant.</div>
                        </div>
                        <span>›</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 7px 0; cursor: pointer;">
                        <div>
                            <div style="font-weight: 600; color: #16221c;">Email Us</div>
                            <div style="font-size: 0.68rem; color: #2d5f47; font-weight: 600;">support@acadassist.app</div>
                        </div>
                        <span>›</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # System Status
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🟢 System Status</div>
                <span class="section-link">View Status →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="font-size: 0.74rem; color: #10b981; font-weight: 700; margin-bottom: 8px;">
                    ● All Systems Operational
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.78rem;">
            """,
            unsafe_allow_html=True,
        )
        for s in system_status:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #f2f0eb;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: #10b981;"></span>
                        <span style="color: #243229;">{s['name']}</span>
                    </div>
                    <span style="color: #10b981; font-weight: 600; font-size: 0.72rem;">{s['status']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Feedback Card
        st.markdown(
            """
            <div class="acad-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span>💡</span>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #16221c;">Give Feedback</div>
                </div>
                <div style="font-size: 0.74rem; color: #728078; margin-bottom: 12px;">
                    Help us improve AcadAssist! Share your ideas, report issues, or suggest new features.
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("Share Feedback →", key="share_fb_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
