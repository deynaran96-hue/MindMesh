"""
Feature 3: MCQ Generator & Interactive Quiz Simulator
Generates exam-oriented multiple choice questions with difficulty levels, live scoring, and explanations.
"""

import streamlit as st
from ai.gemma import generate_mcqs

def render_mcq_page():
    st.markdown('<div class="page-header"><h1>❓ MCQ Generator & Quiz</h1><p class="subtitle">Practice university-level multiple-choice questions tailored to your notes.</p></div>', unsafe_allow_html=True)

    study_material = st.session_state.get("study_material", "").strip()
    active_topic = st.session_state.get("active_topic", "General")

    if not study_material:
        st.warning("⚠️ **No study material loaded.** Please paste notes or upload a file in the **📚 Study Material** section first!")
        if st.button("🚀 Load Operating Systems Demo Notes"):
            from config import SAMPLE_OS_NOTES
            st.session_state.study_material = SAMPLE_OS_NOTES
            st.session_state.active_topic = "Operating Systems"
            st.session_state.material_source = "OS Sample"
            st.rerun()
        return

    # Configuration Controls
    with st.expander("⚙️ Quiz Parameters", expanded=True):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            num_questions = st.select_slider("Number of Questions", options=[3, 5, 10], value=5)
        with col2:
            difficulty = st.selectbox("Difficulty Level", options=["Easy", "Medium", "Hard"], index=1)
        with col3:
            generate_mcq_btn = st.button("⚡ Generate MCQs", type="primary", use_container_width=True)

    if generate_mcq_btn:
        with st.spinner("🧠 Gemma is formulating exam-caliber MCQs..."):
            success, mcq_data, source_tag = generate_mcqs(
                material=study_material,
                number=num_questions,
                difficulty=difficulty,
                provider=st.session_state.get("ai_provider", "local_engine"),
                model=st.session_state.get("ollama_model", "gemma:2b"),
                ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                api_key=st.session_state.get("api_key", ""),
                topic=active_topic
            )
            if success:
                st.session_state.mcq_data = mcq_data
                st.session_state.mcq_source = source_tag
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = None
                st.success(f"✅ Generated {len(mcq_data.get('questions', []))} questions! ({source_tag})")
            else:
                st.error("Failed to generate MCQs. Check AI settings.")

    mcqs = st.session_state.get("mcq_data")
    if not mcqs or not mcqs.get("questions"):
        st.info("💡 Click **'⚡ Generate MCQs'** above to generate practice questions from your material.")
        return

    questions = mcqs.get("questions", [])
    total_q = len(questions)

    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin: 1.5rem 0 1rem 0;">
        <span class="badge badge-info">📝 {total_q} Questions</span>
        <span class="badge badge-warning">🎯 Difficulty: {difficulty}</span>
        <span class="badge badge-success">✨ {st.session_state.get('mcq_source', 'Gemma Engine')}</span>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Quiz Form
    with st.form("mcq_quiz_form"):
        for i, q in enumerate(questions):
            q_id = q.get("id", i + 1)
            q_text = q.get("question", "")
            options = q.get("options", [])
            
            st.markdown(f"""
            <div style="font-weight:600; font-size:1.05rem; margin-top:1rem; margin-bottom:0.5rem; color:#1e293b;">
                Q{i+1}. {q_text}
            </div>
            """, unsafe_allow_html=True)

            current_choice = st.session_state.user_answers.get(q_id, None)
            # Find default index if previously selected
            def_idx = options.index(current_choice) if current_choice in options else None

            choice = st.radio(
                label=f"Options for Q{i+1}",
                options=options,
                index=def_idx,
                key=f"mcq_choice_{q_id}",
                label_visibility="collapsed"
            )
            st.session_state.user_answers[q_id] = choice
            st.markdown("<hr style='margin:0.8rem 0; border:none; border-top:1px dashed #e2e8f0;'>", unsafe_allow_html=True)

        col_sub1, col_sub2 = st.columns([1, 3])
        with col_sub1:
            submit_quiz = st.form_submit_button("🏁 Submit Quiz", type="primary", use_container_width=True)

    if submit_quiz:
        st.session_state.quiz_submitted = True
        correct_count = 0
        for q in questions:
            q_id = q.get("id")
            user_ans = st.session_state.user_answers.get(q_id)
            if user_ans and user_ans.strip() == q.get("correct_answer", "").strip():
                correct_count += 1
        st.session_state.quiz_score = correct_count
        st.rerun()

    # Display Results & Explanations if Submitted
    if st.session_state.get("quiz_submitted"):
        score = st.session_state.get("quiz_score", 0)
        percentage = round((score / total_q) * 100) if total_q > 0 else 0

        score_color = "#10b981" if percentage >= 70 else "#f59e0b" if percentage >= 50 else "#ef4444"
        feedback = "Outstanding! You have mastered this concept." if percentage >= 80 else "Good job! Review the explanations below to polish weak areas." if percentage >= 50 else "Needs revision. Walk through the detailed explanations below!"

        st.markdown(f"""
        <div class="feature-card" style="text-align:center; border: 2px solid {score_color}; background: #f8fafc; margin-top:1.5rem;">
            <h2 style="margin:0; color:#1e293b; font-size:1.6rem;">Quiz Results</h2>
            <div style="font-size:3rem; font-weight:800; color:{score_color}; margin:0.5rem 0;">
                {score} / {total_q} <span style="font-size:1.5rem; font-weight:600;">({percentage}%)</span>
            </div>
            <p style="color:#64748b; font-size:1.05rem; margin:0;">{feedback}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Question-by-Question Review")
        for i, q in enumerate(questions):
            q_id = q.get("id", i + 1)
            user_ans = st.session_state.user_answers.get(q_id, "No answer selected")
            correct_ans = q.get("correct_answer", "")
            is_correct = (user_ans.strip() == correct_ans.strip())

            status_badge = "✅ Correct" if is_correct else "❌ Incorrect"
            badge_color = "#10b981" if is_correct else "#ef4444"

            st.markdown(f"""
            <div class="feature-card" style="border-left: 4px solid {badge_color}; margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:#1e293b;">Q{i+1}: {q.get('question')}</span>
                    <span style="font-size:0.85rem; font-weight:600; color:{badge_color};">{status_badge}</span>
                </div>
                <div style="margin:0.5rem 0; font-size:0.92rem;">
                    <div><strong>Your Answer:</strong> <span style="color:{badge_color};">{user_ans}</span></div>
                    <div><strong>Correct Answer:</strong> <span style="color:#10b981; font-weight:600;">{correct_ans}</span></div>
                </div>
                <div style="background:#f1f5f9; padding:0.6rem 0.8rem; border-radius:6px; font-size:0.88rem; color:#475569;">
                    💡 <strong>Explanation:</strong> {q.get('explanation', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Retry / Reset Button
        col_r1, _ = st.columns([1.5, 3])
        with col_r1:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
                st.session_state.quiz_score = None
                st.rerun()
