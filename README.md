# 🧠 MindMesh AI
### Your Personal Open-Source AI Study Assistant • Powered by Google Gemma

> **MindMesh AI is an open-source AI-powered study assistant that transforms ordinary study material into personalized learning resources. Using Gemma, MindMesh can summarize notes, generate MCQs, create flashcards, answer questions and help students prepare for examinations—all from a single platform.**

---

## 🌟 Overview & Key Problem Solved

College and university students often struggle with voluminous textbooks, opaque lecture notes, and tight revision timelines. Students waste hours manually formulating practice questions, extracting summaries, building flashcards, and switching between disjointed tools.

**MindMesh AI** provides a unified educational workspace where a student can paste notes, upload course materials (PDF, TXT, DOCX), or enter an academic topic from scratch. Powered by an open-source **Google Gemma** model, MindMesh automates the entire active-recall revision loop in seconds.

---

## ✨ Core Capabilities & Features

### 1. 💬 Ask AI Study Companion
- Conversational chat interface acting as a personal tutor.
- Context-grounded explanations directly citing the student's study material.
- Uses simple language, intuitive real-world analogies (e.g. traffic intersections for deadlocks), and breaks down complex questions.
- Suggested prompt pills and clear follow-up capabilities.

### 2. ✨ AI Summary Generator
- **Quick Summary**: High-yield 2-3 sentence overview for rapid orientation.
- **Detailed Explanation**: Comprehensive analysis explaining mechanisms and architecture.
- **Important Points**: Actionable bullet points highlighting core concepts.
- **Key Terms Glossary**: Terminology chips with clear student-friendly definitions.
- Downloadable formatted Markdown notes.

### 3. ❓ MCQ Generator & Interactive Quiz Simulator
- Generates multiple-choice questions tailored to chosen difficulty (**Easy**, **Medium**, **Hard**).
- Interactive quiz interface: students choose options and submit for instant scoring.
- Question-by-question review with color-coded feedback (Correct / Incorrect) and detailed educational explanations.

### 4. 🧠 3D Interactive Revision Flashcards
- Targeted active recall questions and answers.
- Smooth **3D flip card animations** with realistic perspective transforms.
- Deck navigation: Previous, Reveal Answer / Flip, Next, and Restart Deck.
- Mastery tracking: Mark cards as mastered vs. needs practice.
- Grid view option to preview the entire deck at a glance.

### 5. 📝 Important Exam Questions
- Categorized according to standard university marking schemes:
  - **Very Short Questions (1–2 marks)**: Definitions, formulas, single-sentence answers.
  - **Short Questions (3–5 marks)**: Mechanism explanations, comparative tables.
  - **Long In-Depth Questions (8–10 marks)**: Architectural diagrams, proofs, derivations.
- Model answers and scoring outlines included for each question.
- 1-click download of the complete mock question paper.

### 6. 📅 Personalized Revision Planner
- Formulates a realistic, stress-free day-by-day revision schedule based on exam date, daily available study hours, and current student preparedness level.
- Interactive task checklists with pro study tips.

### 7. 📚 Multi-Source Material Input & Topic-Based Learning
- **Paste Notes**: Large text editor with real-time word, token, and reading-time metrics.
- **File Upload**: Direct extraction from `.pdf`, `.txt`, and `.docx` documents.
- **Topic-Based Learning**: Zero-notes mode — enter any syllabus topic (e.g. *Binary Search Tree*, *Deadlocks*, *Computer Networks*) to generate complete revision packs automatically.
- **1-Click Hackathon Presets**: Instant one-click loader for Operating Systems and Data Structures demonstration notes.

---

## 🏗️ Architecture & Technology Stack

```text
Student
   ↓
Upload (PDF/TXT) / Paste Notes / Academic Topic
   ↓
MindMesh AI Layer (Streamlit + Python 3.12)
   ↓
Prompt Engineering & Context Truncation Layer
   ↓
┌────────────────────────────────────────────────────────┐
│               Gemma Open-Source Inference              │
│  - Local Ollama Daemon (gemma:2b, gemma2:2b, gemma2:9b) │
│  - Cloud Gemma API (Hugging Face / Groq / OpenAI spec) │
│  - MindMesh High-Precision Local Educational Engine    │
└────────────────────────────────────────────────────────┘
   ↓
Content Analysis & JSON Schema Validation
   ↓
┌──────────────┬──────────────┬──────────────┬───────────┐
│  AI Summary  │   MCQ Quiz   │  Flashcards  │  Ask AI   │
└──────────────┴──────────────┴──────────────┴───────────┘
```

- **Frontend & UI**: Streamlit 1.65+ with custom CSS design system (Plus Jakarta Sans typography, glassmorphism, responsive cards, 3D CSS transforms).
- **Backend & AI**: Python 3.12, Google Gemma models, Ollama API, Requests.
- **Document Processing**: `pypdf`, `python-docx`.

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch MindMesh AI
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🦙 Connecting to Ollama (Gemma Local Model)

1. Start your local Ollama instance:
   ```bash
   ollama serve
   ```
2. Pull the Gemma model:
   ```bash
   ollama pull gemma:2b
   # or
   ollama pull gemma2:2b
   ```
3. Open **⚙️ Settings** inside MindMesh AI, select **🦙 Ollama Local Daemon**, and click **Test Ollama Connection**.

*Note: MindMesh AI includes an intelligent built-in fallback engine so the app works seamlessly even without an active internet connection or local Ollama daemon during live hackathons!*

---

## 🏆 Hackathon Demonstration Flow (Operating Systems Example)

1. **Open MindMesh AI**: Notice the clean, modern dashboard highlighting active metrics and Gemma model integration.
2. **Load Demo Material**: Click **"⚡ Click to Load Operating Systems Demo Notes"** on the Dashboard or in Study Material.
3. **Generate Summary**: Navigate to **✨ AI Summary** and click **Generate Summary**. Showcase the Quick Summary, Detailed Explanation, Important Points, and Key Terms.
4. **Take an MCQ Quiz**: Navigate to **❓ MCQ Generator**, choose 5 questions, select your answers, submit the quiz, and observe instant feedback, score percentages, and explanations.
5. **Revise with 3D Flashcards**: Navigate to **🧠 Flashcards**, click **Reveal Answer** to watch the 3D card flip, step through cards, and mark mastered concepts.
6. **Ask the AI Companion**: Navigate to **💬 Ask AI** and click the pill *"Explain Deadlock with an analogy"* or type *"Explain deadlock recovery in simple terms"*. Observe the clear, intuitive explanation!
7. **Exam Questions & Revision Plan**: Review university-style 1-2 mark, 3-5 mark, and 8-10 mark questions, then inspect the 5-day revision schedule.

---

## 📄 License
Open-Source Educational Project developed for students worldwide.
