"""My Knowledge page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.components.charts import render_progress_bar
from app.ui.components.common import render_empty_state
from app.ui.components.cards import render_activity_list
from app.ui.state import queue_file_upload, step_processing_queue


def render_knowledge() -> None:
    """Render the My Knowledge page."""
    # Simulate queue processing
    if step_processing_queue():
        import time
        time.sleep(0.3)
        st.rerun()

    # Initialize state aliases
    knowledge_materials = st.session_state.get("knowledge_materials", [])
    subjects = st.session_state.get("subjects", [])
    recent_activities = st.session_state.get("recent_activities", [])
    upload_queue = st.session_state.get("upload_queue", [])

    # 1. Hero Header
    render_page_header(
        tag="MY KNOWLEDGE",
        title_html='Your Knowledge, Your <span class="accent-word">Advantage.</span>',
        subtitle="Upload, organize and turn your study material into personalized learning.",
        banner_key="knowledge",
    )
    
    # 2. Navigation Tabs
    tabs = ["All Materials", "Subjects", "Recent", "Starred", "Trash"]
    active_tab = st.radio("Knowledge Nav", tabs, horizontal=True, label_visibility="collapsed")
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # 3. Main Two-Column Layout
    col_left, col_right = st.columns([2.1, 1.2])
    
    with col_left:
        # Upload Area Card
        st.markdown('<div class="acad-card" style="margin-bottom: 20px;">', unsafe_allow_html=True)
        up_col1, up_col2 = st.columns([1.8, 1.2])
        
        with up_col1:
            st.markdown(
                """
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed #d6d3c9; border-radius: 12px; padding: 24px 16px; text-align: center; background: #faf9f6;">
                    <div style="font-size: 2rem; color: #2d5f47; margin-bottom: 6px;">☁️</div>
                    <div style="font-size: 0.96rem; font-weight: 700; color: #15221b;">Drop your files here</div>
                    <div style="font-size: 0.74rem; color: #728077; margin: 4px 0 14px 0;">PDF, PPT, DOCX, TXT (Max 50 MB each)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader("Upload study materials", type=["pdf", "pptx", "docx", "txt"], label_visibility="collapsed")
            if uploaded_file:
                queue_file_upload(uploaded_file.name, "1.2 MB")
                st.success(f"Added {uploaded_file.name} to processing queue!")
                import time
                time.sleep(0.5)
                st.rerun()
                
        with up_col2:
            st.markdown(
                """
                <div style="display: flex; flex-direction: column; gap: 10px; padding-left: 8px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem;">📕</span>
                        <div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #16221c;">PDF</div>
                            <div style="font-size: 0.7rem; color: #718077;">Lecture notes, textbooks</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem;">📙</span>
                        <div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #16221c;">PPT</div>
                            <div style="font-size: 0.7rem; color: #718077;">Class slides</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem;">📘</span>
                        <div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #16221c;">DOCX</div>
                            <div style="font-size: 0.7rem; color: #718077;">Handwritten notes, assignments</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem;">📄</span>
                        <div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #16221c;">TXT</div>
                            <div style="font-size: 0.7rem; color: #718077;">Quick notes</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Your Subjects Section
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">📁 Your Subjects</div>
                <span class="section-link">Manage Subjects →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        subj_cols = st.columns(4)
        for idx, subj in enumerate(subjects[:4]):
            with subj_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; padding: 12px; margin-bottom: 16px; box-shadow: var(--shadow-sm);">
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                            <span style="font-size: 1.1rem;">📁</span>
                            <span style="font-size: 0.82rem; font-weight: 700; color: #15221b;">{subj['name']}</span>
                        </div>
                        <div style="font-size: 0.7rem; color: #728078; margin-bottom: 6px;">{subj['documents_count']} documents</div>
                    """,
                    unsafe_allow_html=True,
                )
                render_progress_bar(subj["progress"], color=subj["color"], height=5)
                st.markdown(
                    f"""
                        <div style="text-align: right; font-size: 0.7rem; font-weight: 700; color: #2d5f47; margin-top: 3px;">{subj['progress']}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
        # All Materials Table
        st.markdown(
            """
            <div class="section-header-wrap" style="margin-top: 10px;">
                <div class="section-title">📄 All Materials (26)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Filter controls
        f_c1, f_c2, f_c3 = st.columns([2, 1, 1])
        with f_c1:
            search_query = st.text_input("Filter files", placeholder="🔍 Search files...", label_visibility="collapsed")
        with f_c2:
            st.selectbox("Filter by Type", ["All Types", "PDF", "PPT", "DOCX", "TXT"], label_visibility="collapsed")
        with f_c3:
            st.selectbox("Filter by Subject", ["All Subjects", "Data Structures", "DBMS", "Computer Networks"], label_visibility="collapsed")
            
        # Custom Rendered Table
        rows_html = ""
        filtered_materials = []
        for mat in knowledge_materials:
            if search_query and search_query.lower() not in mat["name"].lower():
                continue
            filtered_materials.append(mat)
            
        if not filtered_materials:
            render_empty_state("No materials found matching your criteria", ":material/description:")
        else:
            for mat in filtered_materials:
                
            icon = "📕" if mat["type"] == "PDF" else "📙" if mat["type"] == "PPT" else "📘"
            star = "⭐" if mat.get("starred") else ""
            badge_color = "badge-tag-peach" if mat["type"] == "PDF" else "badge-tag-sage"
            
            rows_html += f"""
            <tr>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 600;">
                        <span>{icon}</span>
                        <span>{mat['name']}</span>
                        <span style="font-size: 0.75rem;">{star}</span>
                    </div>
                </td>
                <td><span class="badge-tag badge-tag-peach">{mat['subject']}</span></td>
                <td><span class="badge-tag badge-tag-sage">{mat['type']}</span></td>
                <td style="color: #6a766f; font-size: 0.78rem;">{mat['size']}</td>
                <td style="color: #6a766f; font-size: 0.78rem;">{mat['added_on']}</td>
                <td><span style="color: #10b981; font-weight: 600; font-size: 0.78rem;">● {mat['status']}</span></td>
                <td style="color: #94a3b8; text-align: center; cursor: pointer;">•••</td>
            </tr>
            """
            
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px; overflow: hidden; margin-top: 10px; box-shadow: var(--shadow-sm);">
                    <table class="acad-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Subject</th>
                                <th>Type</th>
                                <th>Size</th>
                                <th>Added On</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
    with col_right:
        # Processing Queue Card
        processing_count = sum(1 for f in upload_queue if f["status"] == "Processing")
        
        st.markdown(
            f"""
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Processing Queue <span class="badge-tag badge-tag-sage" style="margin-left: 6px;">{processing_count}</span></div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if processing_count == 0:
            st.markdown(
                """
                <div class="acad-card" style="margin-bottom: 16px; padding: 16px; text-align: center; color: #9ca3af; font-size: 0.85rem;">
                    Queue is empty
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for file in upload_queue:
                if file["status"] != "Processing":
                    continue
                st.markdown(
                    f"""
                    <div class="acad-card" style="margin-bottom: 16px;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span>📕</span>
                                <span style="font-size: 0.82rem; font-weight: 700; color: #16221c;">{file['name']}</span>
                            </div>
                            <span style="color: #9ca3af; font-size: 0.78rem; cursor: pointer;">✕</span>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
                render_progress_bar(file['progress'], color="#10b981", height=6)
                st.markdown(
                    f"""
                        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #718077; margin-top: 4px;">
                            <span>Processing...</span>
                            <span style="font-weight: 600; color: #15221b;">{file['progress']}%</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        # Storage Overview
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">💾 Storage Overview</div>
                <span class="section-link">View details →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <div class="acad-card" style="margin-bottom: 16px;">
            """,
            unsafe_allow_html=True,
        )
        render_progress_bar(24, color="#10b981", height=8)
        st.markdown(
            """
                <div style="display: flex; justify-content: space-between; font-size: 0.76rem; color: #718077; margin-top: 6px;">
                    <span><strong>1.2 GB</strong> used of 5 GB</span>
                    <span style="font-weight: 700; color: #15221b;">24%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Recent Activity
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Recent Activity</div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if recent_activities:
            render_activity_list(recent_activities[:4])
        else:
            render_empty_state("No recent activity", "⏱️")
        
        # Banner encouragement card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #111e17 0%, #1e3328 100%); border-radius: 12px; padding: 18px; color: #ffffff; box-shadow: var(--shadow-sm); display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 4px;">Turn your notes into understanding.</div>
                    <div style="font-size: 0.75rem; color: #b7c7be;">Upload. Learn. Practice. Grow.</div>
                </div>
                <div style="width: 34px; height: 34px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; font-size: 1rem; cursor: pointer;">
                    →
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
