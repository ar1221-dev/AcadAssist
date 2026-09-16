"""Study Planner page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.cards import render_milestone_banner
from app.ui.components.charts import render_progress_bar
from app.ui.state import toggle_task_completion


def render_planner() -> None:
    """Render the Study Planner page."""
    # Initialize state aliases
    planner_tasks = st.session_state.get("planner_tasks", [])
    upcoming_exams = st.session_state.get("upcoming_exams", [])
    upcoming_deadlines = st.session_state.get("upcoming_deadlines", [])

    # 1. Hero Header
    render_page_header(
        tag="STUDY PLANNER",
        title_html='Plan Today. Progress <span class="accent-word">Tomorrow.</span>',
        subtitle="Stay organized, study smarter, and reach your goals.",
        banner_key="planner",
    )
    
    # 2. Controls row: Date selector & View mode
    ctrl_col1, ctrl_col2 = st.columns([1.5, 1])
    with ctrl_col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="display: flex; gap: 4px;">
                    <button class="btn-outlined-acad" style="padding: 4px 10px;">‹</button>
                    <button class="btn-outlined-acad" style="padding: 4px 10px;">›</button>
                </div>
                <span style="font-size: 1.1rem; font-weight: 700; color: #16221c;">September 2026</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ctrl_col2:
        view_mode = st.radio("Calendar View", ["Day", "Week", "Month"], horizontal=True, label_visibility="collapsed")
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # 3. Three-Column Layout
    col_cal, col_tasks, col_focus = st.columns([1.0, 1.8, 1.1])
    
    with col_cal:
        # Mini Calendar Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: 700; font-size: 0.88rem; color: #15221b;">September 2026</span>
                    <span style="font-size: 0.76rem; color: #75837b;">‹  ›</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-size: 0.7rem; gap: 4px; color: #728077; font-weight: 600; margin-bottom: 6px;">
                    <div>S</div><div>M</div><div>T</div><div>W</div><div>T</div><div>F</div><div>S</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-size: 0.74rem; row-gap: 6px;">
                    <div style="color: #9ca3af;">31</div><div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div>
                    <div>7</div><div>8</div><div>9</div><div>10</div><div>11</div><div>12</div><div>13</div>
                    <div>14</div><div>15</div>
                    <div style="background: #2d5f47; color: #ffffff; border-radius: 50%; font-weight: 700; width: 22px; height: 22px; line-height: 22px; margin: 0 auto;">16</div>
                    <div>17</div><div>18</div><div>19</div><div>20</div>
                    <div>21</div><div>22</div><div>23</div><div>24</div><div>25</div><div>26</div><div>27</div>
                    <div>28</div><div>29</div><div>30</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # My Exams list
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📅 My Exams</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        from app.ui.components.cards import render_exam_list
        if upcoming_exams:
            render_exam_list(upcoming_exams)
        else:
            from app.ui.components.common import render_empty_state
            render_empty_state("No exams scheduled", "📅")
        
    with col_tasks:
        # Today's Timeline Tasks
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">Today, 16 September</div>
                <div style="display: flex; align-items: center; gap: 8px;">
        # Calculate completed
        total_tasks = len(planner_tasks)
        completed_tasks = sum(1 for t in planner_tasks if t["completed"])
        progress_pct = int((completed_tasks / max(total_tasks, 1)) * 100)
        
        st.markdown(
            f"""
            <div class="section-header-wrap">
                <div class="section-title">Today, 16 September</div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.76rem; color: #6a7770; font-weight: 600;">{completed_tasks} / {total_tasks} tasks completed</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_progress_bar(progress_pct, color="#2d5f47", height=6)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        for task in planner_tasks:
            is_last = task == planner_tasks[-1]
            line_html = '<div style="position: absolute; top: 22px; left: 4px; width: 2px; height: 110px; background-color: #eae8e2; z-index: -1;"></div>' if not is_last else ''
            
            t_col_time, t_col_body, t_col_action = st.columns([0.8, 2.7, 0.7])
            with t_col_time:
                node_color = "#2d5f47" if task["completed"] else "#cbd5e1"
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; gap: 8px; padding-top: 10px; font-size: 0.78rem; font-weight: 600; color: #4b5563; position: relative;">
                        {line_html}
                        <span style="width: 10px; height: 10px; border-radius: 50%; background: {node_color}; display: inline-block; margin-top: 4px; z-index: 2;"></span>
                        <span>{task['time']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with t_col_body:
                card_bg = "#ffffff"
                strike = "text-decoration: line-through; color: #8c9790;" if task["completed"] else "color: #17241d;"
                opacity = "0.6" if task["completed"] else "1"
                st.markdown(
                    f"""
                    <div style="background: {card_bg}; border: 1px solid #eae8e2; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; box-shadow: var(--shadow-sm); display: flex; align-items: center; justify-content: space-between; opacity: {opacity};">
                        <div>
                            <div style="font-size: 0.86rem; font-weight: 700; {strike}">{task['title']}</div>
                            <div style="font-size: 0.74rem; color: #6e7a73; margin-top: 2px;">{task['description']}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span class="badge-tag badge-tag-sage">{task['subject_tag']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with t_col_action:
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                if st.button("Done" if task["completed"] else "✓", key=f"p_btn_{task['id']}", use_container_width=True, type="secondary" if task["completed"] else "primary"):
                    toggle_task_completion(task["id"], is_planner=True)
                    st.rerun()
                
        # Add Task Button
        st.button("+ Add a new task", key="planner_add_task_btn", use_container_width=True)
        
        # Bottom Milestone Banner
        render_milestone_banner(
            tag="A SMALL REMINDER",
            title="Progress is a series of small, consistent steps.",
            subtitle="Plan with care. Execute with focus.",
            button_text="Keep Going",
            button_key="planner_milestone_btn",
        )
        
    with col_focus:
        # Focus Mode Card
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <div style="font-size: 0.94rem; font-weight: 700; color: #16221c;">⏱️ Focus Mode</div>
                </div>
                <div style="font-size: 0.75rem; color: #718078; margin-bottom: 12px;">Block distractions. Get things done.</div>
            """,
            unsafe_allow_html=True,
        )
        st.radio("Focus Duration", ["25 min", "50 min", "Custom"], horizontal=True, label_visibility="collapsed")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.button("Start Focus Session →", key="start_focus_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Upcoming Deadlines
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📌 Upcoming Deadlines</div>
                <span class="section-link">View All →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="acad-card" style="margin-bottom: 16px;">', unsafe_allow_html=True)
        for dl in upcoming_deadlines:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f2f0eb;">
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 600; color: #16221c;">{dl['title']}</div>
                        <div style="font-size: 0.68rem; color: #728078;">{dl['date_str']}</div>
                    </div>
                    <span style="font-size: 0.74rem; font-weight: 700; color: #d96b34;">{dl['days_left']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Suggested for You
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">💡 Suggested for You</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 10px; cursor: pointer;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #16221c;">Practice Tree Problems</div>
                        <div style="font-size: 0.72rem; color: #6f7c75; margin-top: 2px;">You've been consistent with Linked Lists. Now strengthen Trees.</div>
                    </div>
                    <span style="color: #2d5f47; font-weight: 700;">›</span>
                </div>
            </div>
            <div class="acad-card" style="cursor: pointer;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #16221c;">Revise Normal Forms</div>
                        <div style="font-size: 0.72rem; color: #6f7c75; margin-top: 2px;">Your DBMS test is in 14 days.</div>
                    </div>
                    <span style="color: #2d5f47; font-weight: 700;">›</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
