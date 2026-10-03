"""
Feature 6: Personalized Revision Planner
Builds practical, day-by-day study timetables tailored to exam deadlines and student schedule.
"""

import streamlit as st
import datetime
from ai.gemma import generate_revision_plan

def render_revision_page():
    st.markdown('<div class="page-header"><h1>📅 Personalized Revision Plan</h1><p class="subtitle">Generate an optimized, step-by-step revision timetable before your exam.</p></div>', unsafe_allow_html=True)

    default_subject = st.session_state.get("active_topic", "Operating Systems")

    with st.form("revision_plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject_input = st.text_input("Subject / Course Name", value=default_subject)
            exam_date_input = st.date_input("Target Exam Date", value=datetime.date.today() + datetime.timedelta(days=7))
        with col2:
            study_time_input = st.selectbox("Available Daily Study Time", ["1 hour / day", "1.5 hours / day", "2 hours / day", "3+ hours / day"], index=2)
            current_level = st.selectbox("Current Preparedness Level", ["Beginner (Starting from scratch)", "Intermediate (Know the basics)", "Advanced (Final revision & mock tests)"], index=1)

        generate_plan_btn = st.form_submit_button("⚡ Generate My Revision Schedule", type="primary", use_container_width=True)

    if generate_plan_btn:
        with st.spinner("🧠 Gemma is organizing your revision schedule from your uploaded material..."):
            level_clean = current_level.split()[0]
            success, plan_data, source_tag = generate_revision_plan(
                subject=subject_input,
                exam_date=str(exam_date_input),
                study_time=study_time_input,
                level=level_clean,
                provider=st.session_state.get("ai_provider", "local_engine"),
                model=st.session_state.get("ollama_model", "gemma:2b"),
                ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                api_key=st.session_state.get("api_key", "")
            )
            if success:
                st.session_state.revision_plan_data = plan_data
                st.session_state.revision_plan_source = source_tag
                st.success(f"✅ Revision plan generated! ({source_tag})")
            else:
                st.error("Failed to generate plan. Please try again.")

    plan = st.session_state.get("revision_plan_data")
    if not plan:
        return

    st.markdown(f"""
    <div class="feature-card" style="border-left: 4px solid #3b82f6; margin: 1rem 0;">
        <h3 style="margin:0 0 0.4rem 0; color:#1e40af; font-size:1.15rem;">🎯 Revision Strategy</h3>
        <p style="margin:0; color:#334155; font-size:1rem; line-height:1.5;">{plan.get('plan_overview')}</p>
    </div>
    """, unsafe_allow_html=True)

    days = plan.get("daily_schedule", [])
    st.markdown(f"### 🗓️ Day-by-Day Roadmap ({len(days)} Days)")

    for d in days:
        day_num = d.get("day", 1)
        topic = d.get("topic", "")
        duration = d.get("duration", "45 mins")
        pro_tip = d.get("pro_tip", "")
        tasks = d.get("tasks", [])

        with st.expander(f"**Day {day_num}: {topic}** &nbsp;⏱️ `{duration}`", expanded=True):
            col_t1, col_t2 = st.columns([2, 1.2])
            with col_t1:
                st.markdown("**Tasks & Action Items:**")
                for t_idx, t in enumerate(tasks):
                    st.checkbox(f"{t}", key=f"rev_task_d{day_num}_{t_idx}")
            with col_t2:
                if pro_tip:
                    st.markdown(f"""
                    <div style="background:#fef3c7; border:1px solid #fde68a; border-radius:6px; padding:0.6rem 0.8rem; font-size:0.88rem; color:#92400e;">
                        💡 <strong>Pro Tip:</strong><br>{pro_tip}
                    </div>
                    """, unsafe_allow_html=True)

    # Export plan
    st.divider()
    plan_md = f"# Revision Timetable: {subject_input}\n"
    plan_md += f"**Target Exam Date:** {exam_date_input} | **Study Time:** {study_time_input}\n\n"
    plan_md += f"{plan.get('plan_overview')}\n\n"
    for d in days:
        plan_md += f"### Day {d.get('day')}: {d.get('topic')} ({d.get('duration')})\n"
        for t in d.get("tasks", []):
            plan_md += f"- [ ] {t}\n"
        if d.get("pro_tip"):
            plan_md += f"  *Pro Tip: {d.get('pro_tip')}*\n"
        plan_md += "\n"

    col_dp1, _ = st.columns([1.5, 3])
    with col_dp1:
        st.download_button(
            label="📥 Export Revision Checklist (Markdown)",
            data=plan_md,
            file_name=f"{subject_input.lower().replace(' ', '_')}_revision_plan.md",
            mime="text/markdown",
            use_container_width=True
        )
