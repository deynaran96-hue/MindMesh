"""
Feature 1: Ask AI — Interactive Conversational Study Assistant
Empathetic, clear, and contextual tutoring powered by Google Gemma.
"""

import streamlit as st
from ai.gemma import ask_study_assistant

def render_ask_ai_page():
    st.markdown('<div class="page-header"><h1>💬 Ask AI Study Assistant</h1><p class="subtitle">Chat with your personal Gemma tutor grounded directly in your study notes.</p></div>', unsafe_allow_html=True)

    study_material = st.session_state.get("study_material", "").strip()
    active_topic = st.session_state.get("active_topic", "General")

    # Status Bar
    col1, col2 = st.columns([3, 1])
    with col1:
        if study_material:
            st.markdown(f"**Grounding Context:** `{active_topic}` ({len(study_material.split())} words loaded)")
        else:
            st.info("ℹ️ No study notes currently loaded. Gemma will answer using general curriculum knowledge.")
    with col2:
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Quick Suggestion Pills
    st.markdown("**Suggested Quick Inquiries:**")
    pill_col1, pill_col2, pill_col3 = st.columns(3)
    preset_query = None
    with pill_col1:
        if st.button("🔒 Explain Deadlock with an analogy", use_container_width=True):
            preset_query = "Explain deadlock in operating systems with a real-life analogy."
    with pill_col2:
        if st.button("⚙️ Difference: Process vs Thread", use_container_width=True):
            preset_query = "What is the difference between a process and a thread in simple language?"
    with pill_col3:
        if st.button("🧠 Explain Virtual Memory & Paging", use_container_width=True):
            preset_query = "Explain virtual memory and page faults using a simple example."

    # Render Existing Chat History
    chat_container = st.container()
    with chat_container:
        if not st.session_state.get("chat_history"):
            st.markdown("""
            <div style="text-align:center; padding: 2.5rem 1rem; color:#94a3b8;">
                <div style="font-size:3rem; margin-bottom:0.5rem;">🤖</div>
                <h3 style="color:#64748b; font-size:1.15rem; margin:0;">Ask me anything about your notes!</h3>
                <p style="font-size:0.92rem;">Try asking for simple explanations, real-world examples, or exam advice.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"], avatar="🧑‍🎓" if message["role"] == "user" else "🧠"):
                    st.markdown(message["content"])

    # Chat Input Box
    user_query = st.chat_input("Ask a question about your study material...")
    query_to_send = preset_query or user_query

    if query_to_send:
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": query_to_send})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(query_to_send)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Gemma is formulating an intuitive explanation..."):
                success, response_text, source_tag = ask_study_assistant(
                    user_question=query_to_send,
                    study_material=study_material,
                    chat_history=st.session_state.chat_history,
                    provider=st.session_state.get("ai_provider", "local_engine"),
                    model=st.session_state.get("ollama_model", "gemma:2b"),
                    ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                    api_key=st.session_state.get("api_key", "")
                )
                st.markdown(response_text)
                st.caption(f"✨ {source_tag}")

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
