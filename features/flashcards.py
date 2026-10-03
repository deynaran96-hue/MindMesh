"""
Feature 4: Flashcard Generator & 3D Interactive Deck
Generates active-recall revision flashcards with flip card animations, progress tracking, and mastery status.
"""

import streamlit as st
from ai.gemma import generate_flashcards

def render_flashcards_page():
    st.markdown('<div class="page-header"><h1>🧠 Revision Flashcards</h1><p class="subtitle">Reinforce memory retention through spaced repetition and active recall.</p></div>', unsafe_allow_html=True)

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

    # Generation Bar
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        num_cards = st.select_slider("Number of Flashcards", options=[4, 6, 8, 12], value=6)
    with col2:
        view_mode = st.radio("Display Mode", options=["🎴 Deck View (One by One)", "🗂️ Grid View (All Cards)"], horizontal=True)
    with col3:
        generate_btn = st.button("⚡ Generate Flashcards", type="primary", use_container_width=True)

    if generate_btn:
        with st.spinner("🧠 Gemma is curating active-recall flashcards from your uploaded material..."):
            success, flashcards_data, source_tag = generate_flashcards(
                material=study_material,
                number=num_cards,
                provider=st.session_state.get("ai_provider", "local_engine"),
                model=st.session_state.get("ollama_model", "gemma:2b"),
                ollama_url=st.session_state.get("ollama_url", "http://localhost:11434"),
                api_key=st.session_state.get("api_key", ""),
                topic=active_topic
            )
            if success:
                st.session_state.flashcards_data = flashcards_data
                st.session_state.flashcards_source = source_tag
                st.session_state.flashcard_index = 0
                st.session_state.flashcard_flipped = False
                st.session_state.mastered_cards = set()
                st.success(f"✅ Generated {len(flashcards_data.get('flashcards', []))} flashcards from your material! ({source_tag})")
            else:
                st.error("Failed to generate flashcards. Please try again.")

    cards_data = st.session_state.get("flashcards_data")
    if not cards_data or not cards_data.get("flashcards"):
        st.info("💡 Click '⚡ Generate Flashcards' to create your revision deck.")
        return

    cards = cards_data.get("flashcards", [])
    total_cards = len(cards)

    # Mode 1: Deck View (Interactive One-by-One with Flip Animation)
    if "Deck View" in view_mode:
        idx = st.session_state.get("flashcard_index", 0)
        # Boundary guard
        if idx >= total_cards:
            idx = 0
            st.session_state.flashcard_index = 0

        current_card = cards[idx]
        is_flipped = st.session_state.get("flashcard_flipped", False)
        card_id = current_card.get("id", idx + 1)
        is_mastered = card_id in st.session_state.get("mastered_cards", set())

        # Progress bar
        progress_val = (idx + 1) / total_cards
        st.progress(progress_val)
        
        col_meta1, col_meta2 = st.columns([2, 1])
        with col_meta1:
            st.markdown(f"**Card {idx + 1} of {total_cards}** &nbsp;•&nbsp; Category: `{current_card.get('category', 'Revision')}`")
        with col_meta2:
            mastered_count = len(st.session_state.get("mastered_cards", set()))
            st.markdown(f"<div style='text-align:right;'><span class='badge badge-success'>🏆 Mastered: {mastered_count}/{total_cards}</span></div>", unsafe_allow_html=True)

        # 3D Flip Flashcard Container
        st.markdown(f"""
        <div class="flashcard-container">
            <div class="flashcard-inner {'flipped' if is_flipped else ''}">
                <div class="flashcard-front">
                    <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#6366f1; margin-bottom:0.8rem;">
                        Question • Tap Flip to Reveal Answer
                    </div>
                    <div style="font-size:1.35rem; font-weight:600; line-height:1.5; color:#1e293b;">
                        {current_card.get('question')}
                    </div>
                </div>
                <div class="flashcard-back">
                    <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#10b981; margin-bottom:0.8rem;">
                        Model Answer
                    </div>
                    <div style="font-size:1.15rem; font-weight:500; line-height:1.6; color:#0f172a;">
                        {current_card.get('answer')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Controls Bar
        col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1.5, 1, 1])
        with col_nav1:
            if st.button("⬅️ Previous", disabled=(idx == 0), use_container_width=True):
                st.session_state.flashcard_index -= 1
                st.session_state.flashcard_flipped = False
                st.rerun()

        with col_nav2:
            flip_label = "🔄 Flip to Question" if is_flipped else "👁️ Reveal Answer"
            if st.button(flip_label, type="primary", use_container_width=True):
                st.session_state.flashcard_flipped = not is_flipped
                st.rerun()

        with col_nav3:
            if st.button("Next ➡️", disabled=(idx == total_cards - 1), use_container_width=True):
                st.session_state.flashcard_index += 1
                st.session_state.flashcard_flipped = False
                st.rerun()

        with col_nav4:
            if st.button("🔁 Restart Deck", use_container_width=True):
                st.session_state.flashcard_index = 0
                st.session_state.flashcard_flipped = False
                st.rerun()

        # Mastery toggle
        st.markdown("<div style='margin-top:1rem; text-align:center;'>", unsafe_allow_html=True)
        col_m1, col_m2, _ = st.columns([1.5, 1.5, 2])
        with col_m1:
            if not is_mastered:
                if st.button("✅ Mark as Mastered", use_container_width=True):
                    st.session_state.mastered_cards.add(card_id)
                    st.rerun()
            else:
                if st.button("↩️ Needs More Practice", use_container_width=True):
                    st.session_state.mastered_cards.remove(card_id)
                    st.rerun()

    # Mode 2: Grid View (All Cards Overview)
    else:
        st.markdown("### 🗂️ All Flashcards Overview")
        grid_cols = st.columns(2)
        for i, card in enumerate(cards):
            col = grid_cols[i % 2]
            with col:
                st.markdown(f"""
                <div class="feature-card" style="border-top: 3px solid #6366f1; min-height: 180px; margin-bottom:1rem;">
                    <div style="font-size:0.78rem; font-weight:700; color:#6366f1; text-transform:uppercase;">Card #{i+1} • {card.get('category', 'Revision')}</div>
                    <div style="font-weight:600; font-size:1.05rem; margin:0.4rem 0; color:#1e293b;">{card.get('question')}</div>
                    <hr style="margin:0.5rem 0; border:none; border-top:1px dashed #cbd5e1;">
                    <div style="font-size:0.92rem; color:#475569; line-height:1.5;">{card.get('answer')}</div>
                </div>
                """, unsafe_allow_html=True)
