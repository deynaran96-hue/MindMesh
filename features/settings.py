"""
Feature 10: AI Settings & Provider Configuration
Manages Ollama local connection, cloud Gemma APIs, and offline fallback options.
"""

import streamlit as st
from ai.gemma import check_ollama_status
from config import AVAILABLE_MODELS

def render_settings_page():
    st.markdown('<div class="page-header"><h1>⚙️ Settings & AI Configuration</h1><p class="subtitle">Configure your open-source Gemma model connection and inference parameters.</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1.2])

    with col1:
        st.markdown("### 🤖 Active AI Engine")
        provider_options = {
            "local_engine": "⚡ MindMesh Local Gemma Engine (Fast, 100% Reliable Offline Fallback)",
            "ollama": "🦙 Ollama Local Daemon (Local Gemma 2B / 9B inference)",
            "api": "☁️ Gemma Cloud API (Groq / HuggingFace OpenAI-compatible)"
        }
        current_provider = st.session_state.get("ai_provider", "local_engine")
        selected_key = st.radio(
            "Select Inference Source:",
            options=list(provider_options.keys()),
            format_func=lambda k: provider_options[k],
            index=list(provider_options.keys()).index(current_provider)
        )
        st.session_state.ai_provider = selected_key

        st.markdown("<hr style='margin:1.2rem 0;'>", unsafe_allow_html=True)

        if selected_key == "ollama":
            st.markdown("#### 🦙 Ollama Configuration")
            ollama_url = st.text_input("Ollama Server URL", value=st.session_state.get("ollama_url", "http://localhost:11434"))
            st.session_state.ollama_url = ollama_url

            model_name = st.selectbox(
                "Gemma Model Variant",
                options=AVAILABLE_MODELS,
                index=0
            )
            st.session_state.ollama_model = model_name

            if st.button("🔌 Test Ollama Connection", type="primary"):
                with st.spinner("Pinging Ollama daemon..."):
                    is_up, models, msg = check_ollama_status(ollama_url)
                    if is_up:
                        st.success(f"✅ Connected to Ollama! Found models: {', '.join(models) if models else 'None pulled yet'}")
                        if model_name not in models:
                            st.warning(f"⚠️ Note: `{model_name}` has not been pulled yet in Ollama. Run `ollama run {model_name}` in your terminal, or MindMesh will use the local fallback.")
                    else:
                        st.error(f"❌ {msg}\n\nMake sure Ollama is installed and running (`ollama serve`). In the meantime, MindMesh will automatically utilize its built-in Local Gemma Engine.")

        elif selected_key == "api":
            st.markdown("#### ☁️ Cloud Inference API")
            api_endpoint = st.text_input("API Endpoint URL", value=st.session_state.get("api_endpoint", "https://api.groq.com/openai/v1/chat/completions"))
            st.session_state.api_endpoint = api_endpoint

            api_key = st.text_input("API Key (e.g. Groq or HuggingFace)", value=st.session_state.get("api_key", ""), type="password")
            st.session_state.api_key = api_key

            api_model = st.text_input("Model ID", value=st.session_state.get("api_model", "gemma2-9b-it"))
            st.session_state.api_model = api_model

        else:
            st.markdown("""
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:1rem; margin-bottom:1rem;">
                <h4 style="margin:0 0 0.3rem 0; color:#166534;">⚡ Built-in MindMesh Local Gemma Engine</h4>
                <p style="margin:0; font-size:0.92rem; color:#15803d; line-height:1.5;">
                    This provider uses specialized educational heuristics and local semantic knowledge patterns modeled on Google Gemma. It operates <strong>100% offline</strong> with zero network latency, zero setup requirements, and guaranteed presentation reliability for college hackathons.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 Status & Information")
        st.markdown(f"""
        <div class="feature-card" style="font-size:0.92rem;">
            <div><strong>Application:</strong> MindMesh AI v1.0</div>
            <div><strong>Target Persona:</strong> College / University Students</div>
            <div><strong>Default Subject:</strong> Operating Systems</div>
            <hr style="margin:0.6rem 0; border:none; border-top:1px dashed #cbd5e1;">
            <div><strong>Active Engine:</strong> <span class="badge badge-info">{selected_key}</span></div>
            <div style="margin-top:0.4rem;"><strong>Context Words:</strong> {len(st.session_state.get('study_material', '').split())}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧹 Reset Application Cache")
        if st.button("Reset All Stored Materials & Sessions", use_container_width=True):
            for key in ["study_material", "summary_data", "mcq_data", "flashcards_data", "exam_questions_data", "chat_history", "revision_plan_data"]:
                st.session_state[key] = None if "data" in key or "history" in key else ""
            st.success("Session state cleared.")
            st.rerun()
