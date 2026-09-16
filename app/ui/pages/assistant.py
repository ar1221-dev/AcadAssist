"""AI Study Assistant page for AcadAssist."""

import streamlit as st
from app.ui.components.headers import render_page_header
from app.ui.state import add_chat_message


def render_assistant() -> None:
    """Render the AI Study Assistant page."""
    # 1. Hero Header
    render_page_header(
        tag="AI STUDY ASSISTANT",
        title_html='Your Personal Study <span class="accent-word">Companion.</span>',
        subtitle="Ask doubts, get explanations, generate notes, solve problems, summarize material — all in one place.",
        banner_key="assistant",
    )
    chat_history = st.session_state.get("chat_history", [])
        
    # 2. Two-Column Layout
    col_chat, col_tools = st.columns([2.1, 1.2])
    
    with col_chat:
        # Chat Header Card
        st.markdown(
            """
            <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 12px 12px 0 0; padding: 12px 18px; border-bottom: 1px solid #eae8e2; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 34px; height: 34px; border-radius: 50%; background: #121d18; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem;">
                        A
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span style="font-size: 0.88rem; font-weight: 700; color: #16221c;">AcadAssist AI</span>
                            <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 0.7rem; color: #10b981; font-weight: 600;">● Online</span>
                        </div>
                        <div style="font-size: 0.72rem; color: #738078;">Your study assistant, always here to help.</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.74rem; color: #6a766f; background: #f2f1ec; padding: 3px 8px; border-radius: 6px;">Model: Gemini 1.5 Flash</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Chat History Container
        st.markdown('<div style="background: #ffffff; border-left: 1px solid #eae8e2; border-right: 1px solid #eae8e2; padding: 18px; min-height: 380px;">', unsafe_allow_html=True)
        for msg in chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-end; align-items: flex-start; gap: 8px; margin-bottom: 14px;">
                        <div style="background: #e9f3ec; border: 1px solid #dbeae0; border-radius: 14px 14px 2px 14px; padding: 10px 16px; max-width: 80%; font-size: 0.88rem; color: #17261d;">
                            {msg['text']}
                            <div style="font-size: 0.65rem; color: #77857d; text-align: right; margin-top: 3px;">{msg.get('time', 'Just now')}</div>
                        </div>
                        <div style="width: 28px; height: 28px; border-radius: 50%; background: #2d5f47; color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; font-weight: 700;">
                            R
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-start; align-items: flex-start; gap: 8px; margin-bottom: 14px;">
                        <div style="width: 28px; height: 28px; border-radius: 50%; background: #121d18; color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; font-weight: 700;">
                            A
                        </div>
                        <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 2px 14px 14px 14px; padding: 14px 18px; max-width: 90%; font-size: 0.88rem; color: #18231c; line-height: 1.6; box-shadow: var(--shadow-sm);">
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(msg["text"])
                st.markdown("</div></div>", unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Composer box
        st.markdown('<div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 0 0 12px 12px; padding: 12px 16px;">', unsafe_allow_html=True)
        c_in, c_btn = st.columns([4, 1])
        with c_in:
            prompt_input = st.text_input(
                "Ask question",
                placeholder="Ask a question, upload a file, or give a topic...",
                label_visibility="collapsed",
                key="chat_prompt_input",
            )
        with c_btn:
            send_clicked = st.button("Send →", key="send_chat_btn", use_container_width=True)
            
        if send_clicked and prompt_input:
            add_chat_message("user", prompt_input)
            # Realistic mock answer
            mock_reply = f"Here is a targeted breakdown for **{prompt_input}**:\n\n1. **Overview**: This concept plays a critical role in system architecture.\n2. **Key Formulas / Rules**: Always keep invariance principles in mind.\n3. **Recommended Next Step**: Practice 3 questions on this topic to solidify understanding!"
            add_chat_message("assistant", mock_reply)
            st.rerun()
            
        # Quick Action Chips
        st.markdown(
            """
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                <span class="action-chip">💡 Explain</span>
                <span class="action-chip">📝 Summarize</span>
                <span class="action-chip">📄 Generate Notes</span>
                <span class="action-chip">📐 Solve Problem</span>
                <span class="action-chip">⚖️ Compare</span>
                <span class="action-chip">🎯 Create Quiz</span>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col_tools:
        # Quick Tools
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⚡ Quick Tools</div>
                <span class="section-link">See all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 16px;">', unsafe_allow_html=True)
        tools = [
            ("Explain Concept", "Get clear explanations", "📖", "#3b82f6"),
            ("Summarize Notes", "Concise summaries", "📝", "#ef4444"),
            ("Solve Problems", "Step-by-step math/code", "📐", "#10b981"),
            ("Generate Quiz", "Practice instantly", "🎯", "#f59e0b"),
            ("Compare Topics", "Side-by-side view", "⚖️", "#6366f1"),
            ("Create Flashcards", "Quick revision cards", "🗂️", "#8b5cf6"),
        ]
        for name, desc, icon, col in tools:
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1px solid #eae8e2; border-radius: 10px; padding: 10px; box-shadow: var(--shadow-sm); cursor: pointer;">
                    <div style="font-size: 1.1rem;">{icon}</div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #16221c; margin-top: 3px;">{name}</div>
                    <div style="font-size: 0.66rem; color: #75837b; margin-top: 1px;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Suggested Prompts
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">💬 Suggested Prompts</div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        prompts = [
            "Explain [topic] in simple words",
            "Summarize this PDF",
            "Create a 10 question quiz on [topic]",
            "Compare [A] vs [B]",
            "Give me important formulas for [topic]",
            "Solve this problem step by step",
        ]
        st.markdown('<div class="acad-card" style="margin-bottom: 16px; padding: 10px 14px;">', unsafe_allow_html=True)
        for p in prompts:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid #f2f0eb; font-size: 0.78rem; color: #233128; cursor: pointer;">
                    <span>🗨️ {p}</span>
                    <span style="color: #2d5f47; font-weight: 700;">›</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Your Recent Chats
        st.markdown(
            """
            <div class="section-header-wrap">
                <div class="section-title">⏱️ Your Recent Chats</div>
                <span class="section-link">View all →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        chats = [
            ("Normalization in DBMS", "Today, 10:14 AM"),
            ("Difference between TCP and UDP", "Yesterday, 8:21 PM"),
            ("Explain DSA Time Complexity", "14 Sep 2026"),
        ]
        st.markdown('<div class="acad-card">', unsafe_allow_html=True)
        for title, date in chats:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid #f2f0eb;">
                    <span style="font-size: 0.78rem; font-weight: 600; color: #17241d;">{title}</span>
                    <span style="font-size: 0.7rem; color: #828e87;">{date}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
