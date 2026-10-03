"""
Feature 2: AI Summary Generator
Generates Quick Summary, Detailed Explanation, Important Points, and Key Terms.
"""

import streamlit as st
from ai.gemma import generate_summary
from utils.helpers import export_as_markdown

def render_summary_page():
    st.markdown('<div class="page-header"><h1>✨ AI Summary Generator</h1><p class="subtitle">Transform extensive academic notes into structured, high-retention revision summaries.</p></div>', unsafe_allow_html=True)

    study_material = st.session_state.get("study_material", "").strip()
    active_topic = st.session_state.get("active_topic", "General")

    if not study_material:
        st.warning("⚠️ **No study material loaded.** Please paste notes or upload a file in the **📚 Study Material** section, or load our sample topic!")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🚀 Load Operating Systems Notes", use_container_width=True):
                from config import SAMPLE_OS_NOTES
                st.session_state.study_material = SAMPLE_OS_NOTES
                st.session_state.active_topic = "Operating Systems"
                st.session_state.material_source = "OS Sample"
                st.rerun()
        return

    # Generation Trigger Bar
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"**Target Topic:** `{active_topic}`")
    with col2:
        provider_name = st.session_state.get("ai_provider", "local_engine")
        st.markdown(f"**Active AI Engine:** `{provider_name.replace('_', ' ').title()}`")
    with col3:
        generate_btn = st.button("⚡ Generate Summary", type="primary", use_container_width=True)

    if generate_btn or (st.session_state.get("summary_data") is None and st.session_state.get("auto_generate")):
        with st.spinner("🧠 Gemma is analyzing your study material..."):
            success, summary_data, source_tag = generate_summary(
                material=study_material,
                provider=st.session_state.get("ai_provider", "local_engine"),
                model=st.session_state.get("ollama_model", "gemma:2b"),
                ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                api_key=st.session_state.get("api_key", ""),
                topic=active_topic
            )
            if success:
                st.session_state.summary_data = summary_data
                st.session_state.summary_source = source_tag
                st.session_state.auto_generate = False
                st.success(f"✅ Summary generated successfully! ({source_tag})")
            else:
                st.error("Failed to generate summary. Please check your AI configuration in Settings.")

    # Render Summary Cards if available
    summary = st.session_state.get("summary_data")
    if summary:
        # Source badge & Actions
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem;">
            <span class="badge badge-success">✨ {st.session_state.get('summary_source', 'Gemma Engine')}</span>
        </div>
        """, unsafe_allow_html=True)

        # 1. Quick Summary Card
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #6366f1;">
            <div style="display:flex; align-items:center; gap: 0.6rem; margin-bottom: 0.5rem;">
                <span style="font-size:1.4rem;">⚡</span>
                <h3 style="margin:0; color:#4f46e5; font-size:1.15rem;">Quick Summary</h3>
            </div>
            <p style="font-size:1.05rem; line-height:1.6; color:#334155; margin:0;">
                {quick_summary}
            </p>
        </div>
        """.format(quick_summary=summary.get("quick_summary", "No quick summary available.")), unsafe_allow_html=True)

        # 2. Detailed Explanation Card
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #8b5cf6;">
            <div style="display:flex; align-items:center; gap: 0.6rem; margin-bottom: 0.5rem;">
                <span style="font-size:1.4rem;">📖</span>
                <h3 style="margin:0; color:#7c3aed; font-size:1.15rem;">Detailed Explanation</h3>
            </div>
            <p style="font-size:0.98rem; line-height:1.65; color:#334155; margin:0;">
                {detailed_summary}
            </p>
        </div>
        """.format(detailed_summary=summary.get("detailed_summary", "No detailed summary available.")), unsafe_allow_html=True)

        # 3. Important Points
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #10b981;">
            <div style="display:flex; align-items:center; gap: 0.6rem; margin-bottom: 0.8rem;">
                <span style="font-size:1.4rem;">📌</span>
                <h3 style="margin:0; color:#059669; font-size:1.15rem;">Important Points to Remember</h3>
            </div>
        """, unsafe_allow_html=True)
        
        points = summary.get("important_points", [])
        for pt in points:
            st.markdown(f"""
            <div style="display:flex; gap:0.6rem; align-items:flex-start; margin-bottom:0.4rem;">
                <span style="color:#10b981; font-weight:bold;">•</span>
                <span style="color:#334155; font-size:0.95rem; line-height:1.5;">{pt}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 4. Key Terms Chips/Grid
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #f59e0b;">
            <div style="display:flex; align-items:center; gap: 0.6rem; margin-bottom: 0.8rem;">
                <span style="font-size:1.4rem;">🔑</span>
                <h3 style="margin:0; color:#d97706; font-size:1.15rem;">Key Terminology Glossary</h3>
            </div>
        """, unsafe_allow_html=True)

        terms = summary.get("key_terms", [])
        if terms:
            term_cols = st.columns(2)
            for idx, item in enumerate(terms):
                col = term_cols[idx % 2]
                with col:
                    st.markdown(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                        <span style="font-weight:700; color:#1e293b; font-size:0.95rem;">{item.get('term', '')}</span>
                        <p style="margin:0.25rem 0 0 0; color:#64748b; font-size:0.88rem; line-height:1.4;">{item.get('definition', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Export & Action Tools
        st.divider()
        md_text = f"""# {active_topic} — AI Revision Summary

## Quick Summary
{summary.get('quick_summary', '')}

## Detailed Explanation
{summary.get('detailed_summary', '')}

## Important Points
""" + "\n".join([f"- {p}" for p in points]) + "\n\n## Key Terms\n" + "\n".join([f"- **{t.get('term')}**: {t.get('definition')}" for t in terms])

        col_d1, col_d2, _ = st.columns([1.5, 1.5, 3])
        with col_d1:
            st.download_button(
                label="📥 Download Markdown",
                data=md_text,
                file_name=f"{active_topic.lower().replace(' ', '_')}_summary.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.summary_data = None
                st.rerun()
