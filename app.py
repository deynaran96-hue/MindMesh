"""
MindMesh AI — AI-Powered Study & Revision Assistant
Main Application Entrypoint
Powered by Google Gemma
"""

import os
import streamlit as st
from config import APP_NAME, APP_SUBTITLE, APP_ICON, APP_VERSION
from utils.helpers import init_session_state
from features.dashboard import render_dashboard_page
from features.study_material import render_study_material_page
from features.summary import render_summary_page
from features.mcq import render_mcq_page
from features.flashcards import render_flashcards_page
from features.ask_ai import render_ask_ai_page
from features.exam_questions import render_exam_questions_page
from features.revision import render_revision_page
from features.settings import render_settings_page

# Set Page Config
st.set_page_config(
    page_title=f"{APP_NAME} — {APP_SUBTITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS Design System
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State Variables
init_session_state(st)

# Navigation Menu Options (Section 15 Specification)
NAV_OPTIONS = [
    "🏠 Dashboard",
    "📚 Study Material",
    "✨ AI Summary",
    "❓ MCQ Generator",
    "🧠 Flashcards",
    "💬 Ask AI",
    "📝 Exam Questions",
    "📅 Revision Plan",
    "⚙️ Settings"
]

# Sidebar Interface
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)

    st.markdown(f"""
    <div style="padding: 0.2rem 0 0.8rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
        <div style="display:flex; align-items:center; gap:0.6rem;">
            <span style="font-size:2rem;">{APP_ICON}</span>
            <div>
                <h2 style="margin:0; font-size:1.35rem; font-weight:800; color:#1e1b4b; letter-spacing:-0.5px;">{APP_NAME}</h2>
                <div style="font-size:0.75rem; color:#6366f1; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Gemma-Powered Assistant</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active Provider Status Badge
    active_prov = st.session_state.get("ai_provider", "local_engine")
    prov_label = "Local Gemma Engine" if active_prov == "local_engine" else "Ollama (Gemma)" if active_prov == "ollama" else "Cloud Gemma API"
    st.markdown(f"""
    <div style="margin-bottom:1rem;">
        <span class="badge badge-success" style="width:100%; text-align:center;">🟢 {prov_label}</span>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation Radio
    # Sync with session_state current_page if it was updated by a button on Dashboard
    curr = st.session_state.get("current_page", "🏠 Dashboard")
    # Clean match with options
    default_index = 0
    for i, opt in enumerate(NAV_OPTIONS):
        if opt == curr or opt.split(maxsplit=1)[-1] == curr.split(maxsplit=1)[-1]:
            default_index = i
            break

    selected_nav = st.radio(
        "Navigation",
        options=NAV_OPTIONS,
        index=default_index,
        label_visibility="collapsed"
    )
    st.session_state.current_page = selected_nav

    # Study Context Indicator
    st.markdown("<hr style='margin:1.5rem 0 1rem 0; border:none; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)
    active_mat = st.session_state.get("study_material", "").strip()
    active_top = st.session_state.get("active_topic", "None")

    if active_mat:
        word_cnt = len(active_mat.split())
        st.markdown(f"""
        <div style="background:#f1f5f9; border-radius:8px; padding:0.8rem; font-size:0.85rem;">
            <div style="font-weight:700; color:#334155; margin-bottom:0.2rem;">📖 Current Study Topic</div>
            <div style="color:#0f172a; font-weight:600;">{active_top}</div>
            <div style="color:#64748b; font-size:0.8rem; margin-top:0.2rem;">{word_cnt} words loaded</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#fffbeb; border:1px solid #fef3c7; border-radius:8px; padding:0.8rem; font-size:0.82rem; color:#92400e;">
            ⚠️ No notes loaded.<br>Head to <strong>📚 Study Material</strong> or load demo notes.
        </div>
        """, unsafe_allow_html=True)

    # Footer Branding
    st.markdown("""
    <div style="position:fixed; bottom:12px; left:16px; font-size:0.75rem; color:#94a3b8;">
        MindMesh AI v1.0 • Built for Students
    </div>
    """, unsafe_allow_html=True)

# Main Application Routing
if "Dashboard" in selected_nav:
    render_dashboard_page()
elif "Study Material" in selected_nav:
    render_study_material_page()
elif "AI Summary" in selected_nav:
    render_summary_page()
elif "MCQ Generator" in selected_nav:
    render_mcq_page()
elif "Flashcards" in selected_nav:
    render_flashcards_page()
elif "Ask AI" in selected_nav:
    render_ask_ai_page()
elif "Exam Questions" in selected_nav:
    render_exam_questions_page()
elif "Revision Plan" in selected_nav:
    render_revision_page()
elif "Settings" in selected_nav:
    render_settings_page()
