"""
Feature 9: Interactive Dashboard
Central command hub displaying study metrics, active material status, and direct tool navigation.
"""

import streamlit as st
from config import SAMPLE_OS_NOTES

def render_dashboard_page():
    # Hero Welcome Banner
    st.markdown("""
    <div class="dashboard-hero">
        <div style="font-size:3.2rem; margin-bottom:0.2rem;">🧠</div>
        <h1 style="font-size:2.3rem; margin:0 0 0.5rem 0; font-weight:800; letter-spacing:-0.5px;">MindMesh AI</h1>
        <p style="font-size:1.15rem; margin:0; opacity:0.92; font-weight:400;">
            Your Personal Open-Source AI Study & Revision Assistant • Powered by <strong>Google Gemma</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Study Metrics Strip
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    mat_loaded = bool(st.session_state.get("study_material", "").strip())
    word_count = len(st.session_state.get("study_material", "").split()) if mat_loaded else 0
    cards_count = len(st.session_state.get("flashcards_data", {}).get("flashcards", [])) if st.session_state.get("flashcards_data") else 0
    mastered_count = len(st.session_state.get("mastered_cards", set()))
    quiz_score = st.session_state.get("quiz_score")

    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📚 Active Material</div>
            <div class="metric-val">{word_count} words</div>
            <div class="metric-desc">{st.session_state.get('active_topic', 'None') if mat_loaded else 'No notes loaded'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🧠 Flashcards Reviewed</div>
            <div class="metric-val">{mastered_count} / {cards_count}</div>
            <div class="metric-desc">Mastery progress</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎯 Latest Quiz Score</div>
            <div class="metric-val">{f'{quiz_score} pts' if quiz_score is not None else '--'}</div>
            <div class="metric-desc">{'Submitted' if quiz_score is not None else 'No quiz taken yet'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⚡ Study Streak</div>
            <div class="metric-val">🔥 3 Days</div>
            <div class="metric-desc">Keep revising!</div>
        </div>
        """, unsafe_allow_html=True)

    # Hackathon Fast-Demo Callout
    if not mat_loaded:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e0e7ff 0%, #ede9fe 100%); border:1px solid #c7d2fe; border-radius:12px; padding:1.2rem; margin:1.5rem 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <h3 style="margin:0; color:#3730a3; font-size:1.15rem;">🚀 Running a Hackathon Demonstration?</h3>
                    <p style="margin:0.25rem 0 0 0; color:#4338ca; font-size:0.95rem;">
                        Load our pre-configured <strong>Operating Systems (Deadlocks & Memory Management)</strong> curriculum with one click!
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Click to Load Operating Systems Demo Notes", type="primary", use_container_width=True):
            st.session_state.study_material = SAMPLE_OS_NOTES
            st.session_state.active_topic = "Operating Systems"
            st.session_state.material_source = "OS Demo Preset"
            st.rerun()

    # AI Tools Hub (Section 13 Grid)
    st.markdown("<h2 style='font-size:1.4rem; color:#1e293b; margin:1.5rem 0 1rem 0;'>🛠️ AI Revision Suite</h2>", unsafe_allow_html=True)

    grid_col1, grid_col2, grid_col3 = st.columns(3)

    with grid_col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">✨</div>
            <div class="tool-title">AI Summary</div>
            <div class="tool-desc">Condense lengthy textbook chapters into quick summaries, detailed explanations, bullet points, and key terms.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Summary ➡️", key="btn_dash_summary", use_container_width=True):
            st.session_state.current_page = "✨ AI Summary"
            st.rerun()

    with grid_col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">❓</div>
            <div class="tool-title">MCQ Generator</div>
            <div class="tool-desc">Test your understanding with university-level multiple choice questions, difficulty settings, and real-time scoring.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open MCQ Quiz ➡️", key="btn_dash_mcq", use_container_width=True):
            st.session_state.current_page = "❓ MCQ Generator"
            st.rerun()

    with grid_col3:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🧠</div>
            <div class="tool-title">Flashcards</div>
            <div class="tool-desc">Active recall flashcards with smooth 3D flip card animations, deck navigation, and mastery tracking.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Flashcards ➡️", key="btn_dash_flashcards", use_container_width=True):
            st.session_state.current_page = "🧠 Flashcards"
            st.rerun()

    grid_col4, grid_col5, grid_col6 = st.columns(3)

    with grid_col4:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">💬</div>
            <div class="tool-title">Ask AI Tutor</div>
            <div class="tool-desc">Chat with an empathetic Gemma AI study buddy. Ask follow-up questions grounded directly in your syllabus notes.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Chat with Ask AI ➡️", key="btn_dash_ask_ai", use_container_width=True):
            st.session_state.current_page = "💬 Ask AI"
            st.rerun()

    with grid_col5:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📝</div>
            <div class="tool-title">Exam Questions</div>
            <div class="tool-desc">Generate typical semester exam questions categorized into 1-2 marks (Very Short), 3-5 marks, and 8-10 marks (Long).</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Exam Qs ➡️", key="btn_dash_exam_q", use_container_width=True):
            st.session_state.current_page = "📝 Exam Questions"
            st.rerun()

    with grid_col6:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📅</div>
            <div class="tool-title">Revision Plan</div>
            <div class="tool-desc">Create a realistic day-by-day revision schedule with milestones and checklists based on your exam deadline.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Revision Plan ➡️", key="btn_dash_plan", use_container_width=True):
            st.session_state.current_page = "📅 Revision Plan"
            st.rerun()
