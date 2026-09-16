"""Assessment page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_milestone_banner
from app.ui.components.charts import render_circular_score



def render_assessment() -> None:
    """Render the Assessment practice page."""
    # Initialize state aliases
    assessment_performance = st.session_state.get("assessment_performance", {})
    recent_attempts = st.session_state.get("recent_attempts", [])
    popular_practice = st.session_state.get("popular_practice", [])

    # 1. Hero Header
    render_page_header(
        tag="ASSESSMENT",
        title_html='Practice with <span class="accent-word">Purpose.</span>',
        subtitle="Sharpen your concepts. Track your progress. Be exam-ready.",
        banner_key="assessment",
    )
    
    # 2. Tabs
    tabs = ["Start Practice", "Previous Attempts", "Weak Areas", "Custom Tests"]
    active_tab = st.radio("Assessment Tabs", tabs, horizontal=True, label_visibility="collapsed")
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # 3. Two-Column Layout
    col_left, col_right = st.columns([2.1, 1.2])
    
    with col_left:
        # Create a New Assessment Form Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: #eef8f2; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; color: #2d5f47;">
                            🎯
                        </div>
                        <div>
                            <div style="font-size: 1.02rem; font-weight: 700; color: #15221b;">Create a New Assessment</div>
                            <div style="font-size: 0.76rem; color: #728078;">Choose your preferences and start practicing.</div>
                        </div>
                    </div>
                    <div style="background: #eef8f2; border: 1px solid #d3ebd9; border-radius: 8px; padding: 6px 12px; font-size: 0.72rem; color: #2d5f47; font-weight: 600; cursor: pointer;">
                        💡 Let AI suggest a test based on weak areas →
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Selectors
        sel_c1, sel_c2 = st.columns(2)
        with sel_c1:
            subject = st.selectbox(
                "Subject",
                ["Data Structures", "DBMS", "Computer Networks", "Java Programming"],
                index=0,
            )
        with sel_c2:
            topic = st.selectbox(
                "Topic",
                ["Linked Lists", "Binary Trees", "Normalization", "SQL Queries", "Routing & IP"],
                index=0,
            )
            
        opt_c1, opt_c2 = st.columns(2)
        with opt_c1:
            difficulty = st.radio(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
                index=1,
                horizontal=True,
            )
        with opt_c2:
            num_q = st.radio(
                "Number of Questions",
                ["5", "10", "20", "50"],
                index=1,
                horizontal=True,
            )
            
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        btn_c1, btn_c2 = st.columns([2, 1.2])
        with btn_c2:
            if st.button("Start Assessment →", key="start_assessment_btn", use_container_width=True):
                st.success(f"Starting {difficulty} Quiz on {topic} ({num_q} questions)...")
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Popular Practice Sets
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">🔥 Popular Practice Sets</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        pps_cols = st.columns(4)
        for idx, pset in enumerate(popular_practice):
            with pps_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; padding: 12px; margin-bottom: 14px; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; justify-content: space-between; min-height: 125px;">
                        <div>
                            <span style="font-size: 1.1rem;">⚡</span>
                            <div style="font-size: 0.82rem; font-weight: 700; color: #16221c; margin-top: 4px;">{pset['title']}</div>
                            <div style="font-size: 0.68rem; color: #738078; margin-top: 2px;">{pset['subtitle']}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 0.72rem; color: #2d5f47; font-weight: 600;">
                            <span>{pset['questions_count']} Questions</span>
                            <span>{pset['type']} →</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
        # Milestone Banner
        render_milestone_banner(
            tag="KEEP GOING",
            title="Every attempt makes you better.",
            subtitle="Practice today. Progress tomorrow.",
            button_text="Keep Practicing",
            button_key="assess_milestone_btn",
        )
        
    with col_right:
        # Your Performance
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📊 Your Performance</div>
                <span class="section-link">View Detailed →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        render_circular_score(
            assessment_performance.get("average_score", 0),
            label="Average Score",
            sublabel=f"↑ {assessment_performance.get('delta', '0%')}",
        )
        
        st.markdown(
            f"""
            <div style="border-top: 1px solid #f0eee8; padding-top: 10px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                    <span style="color: #6a7770;">📋 Questions Attempted</span>
                    <strong style="color: #15221b;">{assessment_performance.get('questions_attempted', 0)}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                    <span style="color: #6a7770;">✅ Correct Answers</span>
                    <strong style="color: #10b981;">{assessment_performance.get('correct_answers', 0)}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                    <span style="color: #6a7770;">📁 Topics Covered</span>
                    <strong style="color: #15221b;">{assessment_performance.get('topics_covered', 0)}</strong>
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Recent Attempts
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Recent Attempts</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        for att in recent_attempts:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f2f0eb;">
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 600; color: #17241d;">{att['topic']} <span style="font-size: 0.7rem; color: #7b8881;">({att['difficulty']})</span></div>
                        <div style="font-size: 0.7rem; color: #7f8c85;">{att['date']}</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.75rem; color: #6a7770;">{att['score_fraction']}</span>
                        <span class="badge-tag badge-tag-sage">{att['percentage']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⚡ Quick Actions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        q_c1, q_c2 = st.columns(2)
        with q_c1:
            st.button("✦ AI Generate Quiz\n\nBased on your notes", key="as_act_ai", use_container_width=True)
            st.button("📄 Take a Mock Test\n\nExam-like setting", key="as_act_mock", use_container_width=True)
        with q_c2:
            st.button("🎯 Practice Weak Areas\n\nTarget your gaps", key="as_act_weak", use_container_width=True)
            st.button("📊 View Analytics\n\nSee your progress", key="as_act_stat", use_container_width=True)
