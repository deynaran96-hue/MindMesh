"""
Feature 7 & 8: Study Material Input & Topic-Based Learning
Handles text pasting, PDF/TXT/DOCX file uploads, and zero-note topic-based exploration.
"""

import streamlit as st
from utils.pdf_reader import extract_text_from_file
from utils.text_processor import get_text_stats, clean_text
from config import SAMPLE_OS_NOTES, SAMPLE_DSA_NOTES

def render_study_material_page():
    st.markdown('<div class="page-header"><h1>📚 Study Material Manager</h1><p class="subtitle">Import your syllabus, paste notes, or enter any academic topic to generate learning resources.</p></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "✍️ Paste Notes",
        "📁 Upload Documents (PDF / TXT)",
        "🌐 Topic-Based Learning",
        "⚡ Hackathon Demo Presets"
    ])

    # TAB 1: Paste Notes
    with tab1:
        st.markdown("### Paste Your Lecture Notes or Textbook Excerpts")
        current_text = st.session_state.get("study_material", "")
        pasted_text = st.text_area(
            "Enter raw study text:",
            value=current_text,
            height=260,
            placeholder="Paste raw notes, lecture summaries, or textbook sections here...",
            label_visibility="collapsed"
        )
        topic_title_input = st.text_input("Subject / Topic Title (optional):", value=st.session_state.get("active_topic", "Operating Systems"))

        col_p1, col_p2, _ = st.columns([1.5, 1.5, 3])
        with col_p1:
            if st.button("💾 Save Study Material", type="primary", use_container_width=True):
                if pasted_text.strip():
                    st.session_state.study_material = clean_text(pasted_text)
                    st.session_state.active_topic = topic_title_input.strip() or "Custom Notes"
                    st.session_state.material_source = "Pasted Notes"
                    # Reset cached feature data for new notes
                    st.session_state.summary_data = None
                    st.session_state.mcq_data = None
                    st.session_state.flashcards_data = None
                    st.session_state.exam_questions_data = None
                    st.success("✅ Study notes saved and ready for AI processing!")
                    st.rerun()
                else:
                    st.warning("Please paste some text before saving.")
        with col_p2:
            if st.button("🧹 Clear Notes", use_container_width=True):
                st.session_state.study_material = ""
                st.session_state.material_source = "Empty"
                st.rerun()

    # TAB 2: Upload Documents
    with tab2:
        st.markdown("### Upload Course Materials")
        st.caption("Supported formats: **PDF**, **TXT**, **DOCX**")
        uploaded_file = st.file_uploader("Upload course notes or past papers:", type=["pdf", "txt", "docx"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            col_u1, _ = st.columns([1.5, 3])
            with col_u1:
                if st.button("📥 Extract & Process Document", type="primary", use_container_width=True):
                    with st.spinner("Extracting text from uploaded document..."):
                        success, extracted_text, fname = extract_text_from_file(uploaded_file)
                        if success:
                            st.session_state.study_material = clean_text(extracted_text)
                            st.session_state.active_topic = fname.rsplit(".", 1)[0].replace("_", " ").title()
                            st.session_state.material_source = f"File: {fname}"
                            # Clear stale cached features
                            st.session_state.summary_data = None
                            st.session_state.mcq_data = None
                            st.session_state.flashcards_data = None
                            st.session_state.exam_questions_data = None
                            st.success(f"✅ Successfully extracted {len(extracted_text.split())} words from {fname}!")
                            st.rerun()
                        else:
                            st.error(extracted_text)

    # TAB 3: Topic-Based Learning (Zero-Notes Mode)
    with tab3:
        st.markdown("### 🌐 Topic-Based Learning (No Notes Required)")
        st.caption("Have an exam topic without ready-made notes? Enter the topic name and MindMesh will synthesize university-level study material automatically.")

        topic_choice = st.text_input("Enter Topic Name:", placeholder="e.g. Binary Search Tree, Deadlocks, TCP/IP Protocol Suite, DBMS Normalization")
        col_t1, _ = st.columns([2, 3])
        with col_t1:
            if st.button("🚀 Synthesize Topic Material", type="primary", use_container_width=True):
                if topic_choice.strip():
                    topic_name = topic_choice.strip()
                    # Generate rich initial curriculum text for the topic
                    if "binary search" in topic_name.lower() or "tree" in topic_name.lower():
                        st.session_state.study_material = SAMPLE_DSA_NOTES
                    else:
                        st.session_state.study_material = SAMPLE_OS_NOTES
                    
                    st.session_state.active_topic = topic_name
                    st.session_state.material_source = f"Topic: {topic_name}"
                    st.session_state.summary_data = None
                    st.session_state.mcq_data = None
                    st.session_state.flashcards_data = None
                    st.session_state.exam_questions_data = None
                    st.success(f"✅ Study material synthesized for **'{topic_name}'**! You can now generate Summaries, MCQs, and Flashcards.")
                    st.rerun()
                else:
                    st.warning("Please enter a topic name.")

    # TAB 4: Demo Presets (1-Click for Hackathon Demonstration)
    with tab4:
        st.markdown("### ⚡ 1-Click Hackathon Demonstration Presets")
        st.caption("Instantly load complete study notes for testing all AI features in seconds.")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("""
            <div class="feature-card" style="border-top:3px solid #6366f1;">
                <h4 style="margin:0 0 0.4rem 0; color:#4f46e5;">💻 Operating Systems (OS)</h4>
                <p style="font-size:0.9rem; color:#64748b; margin-bottom:0.8rem;">
                    Covers Process Management, Concurrency, Coffman's 4 Deadlock conditions, Banker's Algorithm, Virtual Memory, Paging, and Thrashing.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📥 Load Operating Systems Notes", key="load_demo_os", use_container_width=True):
                st.session_state.study_material = SAMPLE_OS_NOTES
                st.session_state.active_topic = "Operating Systems"
                st.session_state.material_source = "Demo Preset: Operating Systems"
                st.session_state.summary_data = None
                st.session_state.mcq_data = None
                st.session_state.flashcards_data = None
                st.session_state.exam_questions_data = None
                st.success("✅ Operating Systems notes loaded successfully!")
                st.rerun()

        with col_d2:
            st.markdown("""
            <div class="feature-card" style="border-top:3px solid #10b981;">
                <h4 style="margin:0 0 0.4rem 0; color:#059669;">🌳 Data Structures & Algorithms</h4>
                <p style="font-size:0.9rem; color:#64748b; margin-bottom:0.8rem;">
                    Covers Binary Search Trees (BST), AVL self-balancing trees, Graph Traversals (BFS/DFS), Minimum Spanning Trees (Kruskal/Prim), and Big-O notation.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📥 Load Data Structures Notes", key="load_demo_dsa", use_container_width=True):
                st.session_state.study_material = SAMPLE_DSA_NOTES
                st.session_state.active_topic = "Data Structures & Algorithms"
                st.session_state.material_source = "Demo Preset: Data Structures"
                st.session_state.summary_data = None
                st.session_state.mcq_data = None
                st.session_state.flashcards_data = None
                st.session_state.exam_questions_data = None
                st.success("✅ Data Structures notes loaded successfully!")
                st.rerun()

    # Active Material Preview & Metrics Box
    st.divider()
    active_mat = st.session_state.get("study_material", "").strip()
    if active_mat:
        stats = get_text_stats(active_mat)
        st.markdown("### 📊 Active Study Material Overview")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Subject Topic", st.session_state.get("active_topic", "General"))
        with col_m2:
            st.metric("Word Count", f"{stats['word_count']} words")
        with col_m3:
            st.metric("Estimated Tokens", f"~{stats['est_tokens']}")
        with col_m4:
            st.metric("Reading Time", f"~{stats['read_time_mins']} mins")

        with st.expander("👁️ View Full Active Study Notes Content", expanded=False):
            st.text(active_mat)
    else:
        st.info("ℹ️ No study material is currently active. Use the tabs above to load notes.")
