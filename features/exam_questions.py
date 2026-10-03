"""
Feature 5: Important Exam Questions Generator
Generates university-style exam questions categorized by weightage:
1-2 marks (Very Short), 3-5 marks (Short), and 8-10 marks (Long).
"""

import streamlit as st
from ai.gemma import generate_exam_questions

def render_exam_questions_page():
    st.markdown('<div class="page-header"><h1>📝 Important Exam Questions</h1><p class="subtitle">Anticipate university examination papers categorized by mark weightage.</p></div>', unsafe_allow_html=True)

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

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Target Subject:** `{active_topic}`")
    with col2:
        generate_btn = st.button("⚡ Generate Exam Questions", type="primary", use_container_width=True)

    if generate_btn:
        with st.spinner("🧠 Gemma is formulating probable university exam questions from your uploaded material..."):
            success, exam_data, source_tag = generate_exam_questions(
                material=study_material,
                provider=st.session_state.get("ai_provider", "local_engine"),
                model=st.session_state.get("ollama_model", "gemma:2b"),
                ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                api_key=st.session_state.get("api_key", "")
            )
            if success:
                st.session_state.exam_questions_data = exam_data
                st.session_state.exam_questions_source = source_tag
                st.success(f"✅ Exam questions generated from your uploaded material! ({source_tag})")
            else:
                st.error("Failed to generate exam questions. Please try again.")

    eq_data = st.session_state.get("exam_questions_data")
    if not eq_data:
        return

    tab1, tab2, tab3 = st.tabs([
        "🎯 Very Short Questions (1-2 Marks)",
        "📝 Short Questions (3-5 Marks)",
        "📚 Long Questions (8-10 Marks)"
    ])

    with tab1:
        vsq = eq_data.get("very_short_questions", [])
        st.markdown(f"### 🎯 Very Short Answer Questions ({len(vsq)} Questions)")
        st.caption("Focus on definitions, formulas, acronyms, and single-sentence answers.")
        for idx, item in enumerate(vsq):
            with st.expander(f"**Q{idx+1} ({item.get('marks', 2)} Marks):** {item.get('question')}", expanded=True):
                st.markdown(f"""
                <div style="background:#f1f5f9; padding:0.8rem; border-radius:6px; font-size:0.95rem; color:#334155;">
                    <strong>💡 Model Answer / Key Points:</strong><br>
                    {item.get('model_answer')}
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        sq = eq_data.get("short_questions", [])
        st.markdown(f"### 📝 Short Answer Questions ({len(sq)} Questions)")
        st.caption("Focus on differences, explanations, steps, and working mechanisms.")
        for idx, item in enumerate(sq):
            with st.expander(f"**Q{idx+1} ({item.get('marks', 5)} Marks):** {item.get('question')}", expanded=True):
                st.markdown(f"""
                <div style="background:#f1f5f9; padding:0.8rem; border-radius:6px; font-size:0.95rem; color:#334155;">
                    <strong>💡 Model Answer Outline:</strong><br>
                    {item.get('model_answer')}
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        lq = eq_data.get("long_questions", [])
        st.markdown(f"### 📚 Long In-Depth Questions ({len(lq)} Questions)")
        st.caption("Comprehensive questions requiring architectural diagrams, derivations, or problem-solving.")
        for idx, item in enumerate(lq):
            with st.expander(f"**Q{idx+1} ({item.get('marks', 10)} Marks):** {item.get('question')}", expanded=True):
                st.markdown(f"""
                <div style="background:#f1f5f9; padding:0.8rem; border-radius:6px; font-size:0.95rem; color:#334155;">
                    <strong>💡 Comprehensive Answer Structure:</strong><br>
                    {item.get('model_answer')}
                </div>
                """, unsafe_allow_html=True)

    # Printable / Download Section
    st.divider()
    all_q_text = f"# University Revision Question Paper — {active_topic}\n\n"
    all_q_text += "## Section A: Very Short Questions (1-2 Marks)\n"
    for i, q in enumerate(vsq):
        all_q_text += f"{i+1}. {q.get('question')} [{q.get('marks')} Marks]\n   Answer: {q.get('model_answer')}\n\n"
    all_q_text += "\n## Section B: Short Questions (3-5 Marks)\n"
    for i, q in enumerate(sq):
        all_q_text += f"{i+1}. {q.get('question')} [{q.get('marks')} Marks]\n   Answer: {q.get('model_answer')}\n\n"
    all_q_text += "\n## Section C: Long Questions (8-10 Marks)\n"
    for i, q in enumerate(lq):
        all_q_text += f"{i+1}. {q.get('question')} [{q.get('marks')} Marks]\n   Answer: {q.get('model_answer')}\n\n"

    col_e1, _ = st.columns([1.5, 3])
    with col_e1:
        st.download_button(
            label="📥 Download Exam Paper (Markdown)",
            data=all_q_text,
            file_name=f"{active_topic.lower().replace(' ', '_')}_exam_questions.md",
            mime="text/markdown",
            use_container_width=True
        )
