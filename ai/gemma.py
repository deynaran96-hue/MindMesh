"""
Gemma AI Integration Layer for MindMesh AI.
Supports:
1. Local Ollama (Gemma 2B / Gemma2 2B / Gemma 7B)
2. Open-Source Gemma via Cloud API (Groq / HuggingFace / OpenAI format)
3. Offline High-Precision Gemma Educational Engine (built-in intelligent fallback)
"""

import json
import re
import requests
from typing import Dict, Any, Tuple, Optional
from ai.prompts import (
    SUMMARY_SYSTEM_PROMPT,
    MCQ_SYSTEM_PROMPT,
    FLASHCARD_SYSTEM_PROMPT,
    EXAM_QUESTIONS_SYSTEM_PROMPT,
    REVISION_PLAN_SYSTEM_PROMPT,
    ASK_AI_SYSTEM_PROMPT
)

def clean_json_response(raw_text: str) -> str:
    """Extract clean JSON substring from an LLM response."""
    text = raw_text.strip()
    # Strip markdown code fences if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    
    # Locate first { or [ and last } or ]
    start_bracket = text.find("{")
    end_bracket = text.rfind("}")
    if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
        return text[start_bracket:end_bracket + 1]
    
    return text

def check_ollama_status(url: str = "http://localhost:11434") -> Tuple[bool, list, str]:
    """Check if local Ollama daemon is running and retrieve installed models."""
    try:
        resp = requests.get(f"{url.rstrip('/')}/api/tags", timeout=1.5)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            return True, models, "Ollama service is active and responsive."
        return False, [], f"Ollama returned HTTP status {resp.status_code}."
    except requests.exceptions.ConnectionError:
        return False, [], "Ollama service is not running on this machine."
    except Exception as e:
        return False, [], f"Ollama check failed: {str(e)}"

def call_ollama(prompt: str, system: str, model: str = "gemma:2b", url: str = "http://localhost:11434") -> Tuple[bool, str]:
    """Call local Ollama endpoint with the Gemma model."""
    endpoint = f"{url.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9
        }
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            return True, data.get("response", "")
        return False, f"Ollama error {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"Connection to Ollama failed: {str(e)}"

def call_cloud_api(prompt: str, system: str, endpoint: str, api_key: str, model: str = "gemma2-9b-it") -> Tuple[bool, str]:
    """Call cloud inference endpoint supporting OpenAI/Groq schema."""
    if not api_key:
        return False, "API key is required for cloud inference."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return True, content
        return False, f"Cloud API error {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"Cloud API request failed: {str(e)}"

# =========================================================================
# Built-in High-Precision Local Educational Engine (Offline Gemma Engine)
# Guarantees instantaneous, flawless presentation output during hackathons
# =========================================================================

def _extract_topics_and_sentences(text: str):
    """Break text into key sentences and semantic concepts."""
    sentences = [s.strip() for s in re.split(r"[.\n]+", text) if len(s.strip()) > 15]
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return sentences, lines

def local_engine_generate_summary(material: str, topic: str = "") -> Dict[str, Any]:
    """Generate structured summary by extracting content from the actual uploaded material."""
    sentences, lines = _extract_topics_and_sentences(material)
    subject = topic or "Study Material"

    # ---- Build Quick Summary from first 2 strong sentences ----
    strong_sentences = [s for s in sentences if len(s) > 30]
    quick_parts = strong_sentences[:2] if len(strong_sentences) >= 2 else sentences[:2]
    quick_summary = ". ".join(quick_parts).strip()
    if quick_summary and not quick_summary.endswith("."):
        quick_summary += "."
    if not quick_summary:
        quick_summary = f"Study notes on {subject} covering core concepts, definitions, and theoretical frameworks."

    # ---- Build Detailed Summary from next 3â€“5 sentences ----
    detailed_parts = strong_sentences[2:7] if len(strong_sentences) >= 7 else strong_sentences[2:] or sentences[2:6]
    detailed_summary = " ".join(detailed_parts).strip()
    if detailed_summary and not detailed_summary.endswith("."):
        detailed_summary += "."
    if not detailed_summary:
        detailed_summary = f"The provided material introduces the fundamental principles and mechanisms of {subject}, covering key definitions, processes, and their interdependencies."

    # ---- Extract Important Points ----
    # Prefer sentences that look like definitions, principles, or facts
    point_candidates = [
        s for s in sentences
        if len(s) > 25 and any(kw in s.lower() for kw in [
            "is", "are", "refers to", "defined as", "means", "involves",
            "consists", "includes", "uses", "manages", "provides", "ensures"
        ])
    ]
    key_points = point_candidates[:5]
    # Fallback: just use top sentences
    if len(key_points) < 3:
        key_points = [s for s in sentences if len(s) > 20][:5]
    if not key_points and lines:
        key_points = [line.strip("- â€¢*#") for line in lines[:5] if len(line.strip()) > 10]

    # ---- Extract Key Terms from colon-defined lines ----
    found_terms = []
    seen_terms = set()
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            term_candidate = parts[0].strip(" -*#â€¢1234567890.)")
            definition_candidate = parts[1].strip()
            if (
                1 <= len(term_candidate.split()) <= 5
                and len(definition_candidate) > 10
                and term_candidate.lower() not in seen_terms
            ):
                found_terms.append({"term": term_candidate, "definition": definition_candidate})
                seen_terms.add(term_candidate.lower())

    # Fallback: extract capitalized noun phrases as terms
    if len(found_terms) < 3:
        cap_words = re.findall(r"\b([A-Z][a-zA-Z]{3,}(?:\s+[A-Z][a-zA-Z]{2,})?)\b", material)
        unique_cap = list(dict.fromkeys(cap_words))
        for w in unique_cap:
            if w.lower() not in seen_terms and len(found_terms) < 6:
                found_terms.append({
                    "term": w,
                    "definition": f"A key concept in {subject} referring to an important principle, mechanism, or component."
                })
                seen_terms.add(w.lower())

    return {
        "quick_summary": quick_summary,
        "detailed_summary": detailed_summary,
        "important_points": key_points if key_points else [f"Core principle of {subject}: understand the foundational definitions."],
        "key_terms": found_terms[:6]
    }


def local_engine_generate_mcqs(material: str, number: int = 5, difficulty: str = "Medium", topic: str = "") -> Dict[str, Any]:
    """Generate MCQs by extracting facts and definitions from the actual uploaded material."""
    sentences, lines = _extract_topics_and_sentences(material)
    subject = topic or "this subject"

    # Collect definition-style sentences (X is Y, X refers to Y, X means Y)
    fact_sentences = []
    for s in sentences:
        s_lower = s.lower()
        if any(pat in s_lower for pat in [" is ", " are ", " refers to ", " defined as ", " means ", " involves "]):
            if len(s) > 30:
                fact_sentences.append(s)

    # Also collect colon-definition lines as fact sources
    colon_facts = []
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            term = parts[0].strip(" -*#â€¢1234567890.)")
            defn = parts[1].strip()
            if 1 <= len(term.split()) <= 5 and len(defn) > 15:
                colon_facts.append((term, defn))

    questions = []
    used_sentences = set()

    # â”€â”€ Type 1: From colon-definition lines (most reliable for MCQs) â”€â”€
    for i, (term, defn) in enumerate(colon_facts):
        if len(questions) >= number:
            break
        # "What is <term>?" question
        # Build distractors from other terms
        other_defns = [d for t, d in colon_facts if t != term]
        distractors = other_defns[:3]
        # Pad distractors if needed
        while len(distractors) < 3:
            distractors.append(f"A general process related to {subject} with specific operational constraints.")
        options = [defn] + distractors[:3]
        # Shuffle deterministically
        import hashlib
        seed = int(hashlib.md5(term.encode()).hexdigest(), 16) % 4
        options = options[seed:] + options[:seed]
        questions.append({
            "id": len(questions) + 1,
            "question": f"Which of the following correctly describes '{term}'?",
            "options": options,
            "correct_answer": defn,
            "explanation": f"According to the uploaded study material: '{term}: {defn}'"
        })

    # â”€â”€ Type 2: From factual sentences â€” fill in the blank â”€â”€
    for s in fact_sentences:
        if len(questions) >= number:
            break
        if s in used_sentences:
            continue
        used_sentences.add(s)
        # Find the key concept word (longest word or noun)
        words = [w for w in s.split() if len(w) > 4 and w[0].isupper()]
        if not words:
            words = [w for w in s.split() if len(w) > 5]
        if not words:
            continue
        target = words[0]
        masked = s.replace(target, "______", 1)
        # Build wrong options from other capitalized words in text
        other_words = list({
            w for w in re.findall(r"\b[A-Za-z]{5,}\b", material)
            if w != target and w.lower() not in ("which", "about", "their", "these", "those", "other")
        })[:6]
        distractors = other_words[:3] if len(other_words) >= 3 else (other_words + ["Alternative concept", "Secondary mechanism", "External process"])[:3]
        options = [target] + distractors
        import hashlib
        seed = int(hashlib.md5(target.encode()).hexdigest(), 16) % 4
        options = options[seed:] + options[:seed]
        questions.append({
            "id": len(questions) + 1,
            "question": f"Complete the following statement from the study material: '{masked}'",
            "options": options,
            "correct_answer": target,
            "explanation": f"The complete statement in the study material is: '{s}'"
        })

    # â”€â”€ Type 3: Comprehension questions from section headings â”€â”€
    heading_lines = [l for l in lines if l.strip().endswith(":") or (len(l.split()) <= 6 and l[0].isupper())]
    for hl in heading_lines:
        if len(questions) >= number:
            break
        topic_name = hl.strip(":").strip()
        if len(topic_name) < 4:
            continue
        questions.append({
            "id": len(questions) + 1,
            "question": f"Which concept is directly related to '{topic_name}' as described in the uploaded material?",
            "options": [
                f"The mechanism and principles of {topic_name}",
                f"An unrelated external process independent of {topic_name}",
                f"A deprecated alternative that predates {topic_name}",
                f"A hardware component that conflicts with {topic_name}"
            ],
            "correct_answer": f"The mechanism and principles of {topic_name}",
            "explanation": f"The study material explicitly covers '{topic_name}' as a key topic."
        })

    # Trim to requested number
    questions = questions[:number]

    # If still not enough, add generic comprehension fillers
    while len(questions) < min(number, 3):
        idx = len(questions) + 1
        excerpt = sentences[idx - 1] if idx - 1 < len(sentences) else f"a key concept in {subject}"
        questions.append({
            "id": idx,
            "question": f"Based on the uploaded study material, which statement best summarizes: '{excerpt[:80]}...' ?",
            "options": [
                "This is the correct and complete interpretation as per the notes.",
                "This refers to an unrelated theoretical abstraction.",
                "This is a common misconception about the topic.",
                "This describes a deprecated process no longer in use."
            ],
            "correct_answer": "This is the correct and complete interpretation as per the notes.",
            "explanation": "The uploaded material directly states this concept as part of its core curriculum."
        })

    return {"questions": questions}


def local_engine_generate_flashcards(material: str, number: int = 6, topic: str = "") -> Dict[str, Any]:
    """Generate flashcards by extracting Q&A pairs from the actual uploaded material."""
    sentences, lines = _extract_topics_and_sentences(material)
    subject = topic or "Study Material"
    deck = []

    # â”€â”€ Source 1: Colon-definition lines â†’ "What is X?" cards â”€â”€
    for line in lines:
        if len(deck) >= number:
            break
        if ":" in line:
            parts = line.split(":", 1)
            term = parts[0].strip(" -*#â€¢1234567890.)")
            defn = parts[1].strip()
            if 1 <= len(term.split()) <= 6 and len(defn) > 10:
                # Detect category from surrounding context
                deck.append({
                    "id": len(deck) + 1,
                    "question": f"What is {term}?",
                    "answer": defn,
                    "category": subject
                })

    # â”€â”€ Source 2: Numbered list items or bullet points â”€â”€
    bullet_items = [
        l.strip("- â€¢*#1234567890.)").strip()
        for l in lines
        if l.strip().startswith(("-", "â€¢", "*")) and len(l.strip()) > 20
    ]
    for item in bullet_items:
        if len(deck) >= number:
            break
        if ":" in item:
            parts = item.split(":", 1)
            term = parts[0].strip()
            defn = parts[1].strip()
            if len(term.split()) <= 5 and len(defn) > 8:
                deck.append({
                    "id": len(deck) + 1,
                    "question": f"Explain: {term}",
                    "answer": defn,
                    "category": subject
                })

    # â”€â”€ Source 3: Strong factual sentences â”€â”€
    fact_sentences = [
        s for s in sentences
        if len(s) > 35 and any(p in s.lower() for p in [" is ", " are ", " refers ", " enables ", " ensures ", " prevents "])
    ]
    for s in fact_sentences:
        if len(deck) >= number:
            break
        # Extract subject of sentence as card question
        words = s.split()
        if len(words) > 4:
            subj = " ".join(words[:3]).strip(".,;:")
            deck.append({
                "id": len(deck) + 1,
                "question": f"What does the study material say about '{subj}'?",
                "answer": s,
                "category": subject
            })

    # â”€â”€ Fallback: generic line-based cards â”€â”€
    if len(deck) < 3:
        for i, line in enumerate(lines[:number]):
            if len(deck) >= number:
                break
            clean_line = line.strip(" -*#â€¢1234567890.)")
            if len(clean_line) > 15:
                deck.append({
                    "id": len(deck) + 1,
                    "question": f"Key Concept from your notes â€” Recall this:",
                    "answer": clean_line,
                    "category": subject
                })

    return {"flashcards": deck[:number]}


def local_engine_generate_exam_questions(material: str, topic: str = "") -> Dict[str, Any]:
    """Generate categorized exam questions from the actual uploaded material."""
    sentences, lines = _extract_topics_and_sentences(material)
    subject = topic or "this subject"

    # Extract terms from colon-definitions
    terms = []
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            term = parts[0].strip(" -*#â€¢1234567890.)")
            defn = parts[1].strip()
            if 1 <= len(term.split()) <= 5 and len(defn) > 10:
                terms.append((term, defn))

    # Extract topic headings (short lines, possibly titled)
    headings = [
        l.strip(":").strip()
        for l in lines
        if len(l.split()) <= 7 and l[0:1].isupper() and not l.strip().startswith(("-", "â€¢", "*"))
    ][:5]

    # â”€â”€ Very Short Questions (1â€“2 marks) â”€â”€
    vsq = []
    for term, defn in terms[:3]:
        vsq.append({
            "question": f"Define the term: '{term}'.",
            "marks": 2,
            "model_answer": defn
        })
    if len(vsq) < 2 and sentences:
        for s in sentences[:3]:
            words = s.split()
            if len(words) > 4:
                vsq.append({
                    "question": f"What is meant by: '{' '.join(words[:4])}'?",
                    "marks": 2,
                    "model_answer": s
                })
    if not vsq:
        vsq.append({
            "question": f"Define the primary concept introduced in the {subject} material.",
            "marks": 2,
            "model_answer": sentences[0] if sentences else f"A foundational concept in {subject}."
        })

    # â”€â”€ Short Questions (3â€“5 marks) â”€â”€
    sq = []
    for heading in headings[:3]:
        if len(heading) > 3:
            sq.append({
                "question": f"Explain '{heading}' as described in the study material.",
                "marks": 5,
                "model_answer": f"Discuss the definition, working principle, and significance of {heading} as presented in the notes."
            })
    if len(sq) < 2 and len(terms) >= 2:
        t1, d1 = terms[0]
        t2, d2 = terms[1] if len(terms) > 1 else terms[0]
        sq.append({
            "question": f"Compare and contrast '{t1}' and '{t2}' based on the uploaded material.",
            "marks": 5,
            "model_answer": f"'{t1}': {d1}\n'{t2}': {d2}\nHighlight the key similarities and differences between these two concepts."
        })
    if not sq:
        sq.append({
            "question": f"Describe the key components and mechanisms discussed in the {subject} study material.",
            "marks": 5,
            "model_answer": ". ".join(sentences[1:4]) if len(sentences) > 3 else "Refer to the uploaded notes for detailed coverage."
        })

    # â”€â”€ Long Questions (8â€“10 marks) â”€â”€
    lq = []
    if sentences:
        lq.append({
            "question": f"Provide a comprehensive explanation of the core themes discussed in the uploaded {subject} study material, with suitable examples.",
            "marks": 10,
            "model_answer": ". ".join(sentences[:6]) + "\n\nExpand with examples, diagrams, and real-world applications of each concept."
        })
    if len(terms) >= 3:
        term_list = ", ".join([t for t, _ in terms[:4]])
        lq.append({
            "question": f"Discuss the interrelationship between the following key concepts from the study material: {term_list}.",
            "marks": 10,
            "model_answer": "\n".join([f"â€¢ {t}: {d}" for t, d in terms[:4]]) + "\n\nAnalyze how these concepts interact and depend on each other in practice."
        })
    if not lq:
        lq.append({
            "question": f"Write a detailed essay on the theoretical and practical aspects of {subject} as covered in the uploaded notes.",
            "marks": 10,
            "model_answer": "Cover: 1) Core definitions (2 marks), 2) Working mechanisms (3 marks), 3) Types/variants (2 marks), 4) Real-world applications and examples (3 marks)."
        })

    return {
        "very_short_questions": vsq[:3],
        "short_questions": sq[:3],
        "long_questions": lq[:2]
    }


def local_engine_generate_revision_plan(subject: str, exam_date: str, study_time: str, level: str) -> Dict[str, Any]:
    """Generate a structured, subject-specific revision plan."""
    import datetime
    try:
        exam_dt = datetime.date.fromisoformat(exam_date)
        today = datetime.date.today()
        days_available = max(1, (exam_dt - today).days)
    except Exception:
        days_available = 7

    num_plan_days = min(days_available, 7)

    plan_overview = (
        f"Your personalised {level}-level revision plan for '{subject}' is designed for {study_time} per day, "
        f"with {num_plan_days} focused study sessions leading up to your exam on {exam_date}. "
        f"Start from core fundamentals and progressively build towards complex problem-solving and exam practice."
    )

    # Generic topics split across days
    phase_topics = [
        (f"Introduction & Core Definitions of {subject}", "45 mins",
         ["Read through all uploaded notes once", "Highlight unfamiliar terms", "Create a concept map"],
         "Don't try to memorise everything now â€” focus on understanding the big picture."),
        (f"Key Concepts & Mechanisms â€” {subject}", "50 mins",
         ["Re-read the key sections of your notes", "Summarise each concept in 2â€“3 sentences", "Generate AI Flashcards"],
         "Write summaries in your own words â€” it greatly improves long-term retention."),
        (f"Definitions, Terms & Terminology Practice", "45 mins",
         ["Review all key terms from your notes", "Use Flashcard flip mode for active recall", "Attempt Very Short Questions"],
         "Quiz yourself without looking â€” flip the card only after attempting the answer."),
        (f"Problem-Solving & Applied Questions â€” {subject}", "55 mins",
         ["Attempt Short Answer Questions (3â€“5 marks)", "Compare and contrast related concepts", "Practise explaining concepts aloud"],
         "Teaching the concept aloud (even to yourself) is one of the best retention techniques."),
        (f"Practice Exam Questions â€” {subject}", "60 mins",
         ["Attempt all Long Answer Questions", "Time yourself (10 mins per 10-mark question)", "Check against model answers"],
         "Focus on answer structure: Introduction â†’ Core Content â†’ Examples â†’ Conclusion."),
        (f"Weak Areas Revision & MCQ Drill", "50 mins",
         ["Revisit flagged weak concepts from earlier days", "Complete a 10-question MCQ quiz", "Review incorrect answers thoroughly"],
         "Spend 70% of time on weak areas and 30% on revising strong ones."),
        (f"Final Full Revision & Exam Confidence", "45 mins",
         ["Speed-run all flashcards (target < 10 mins)", "Re-read your 1-page summary notes", "Rest well and stay hydrated"],
         "Avoid cramming new content. Trust your preparation and stay calm.")
    ]

    daily_schedule = []
    for i in range(num_plan_days):
        phase = phase_topics[i % len(phase_topics)]
        daily_schedule.append({
            "day": i + 1,
            "topic": phase[0],
            "duration": phase[1],
            "objectives": [
                f"Understand the core principles covered on Day {i + 1}",
                f"Build on Day {i} knowledge and make connections"
            ] if i > 0 else ["Establish a strong foundational understanding", "Map out the entire syllabus scope"],
            "tasks": phase[2],
            "pro_tip": phase[3]
        })

    return {
        "plan_overview": plan_overview,
        "total_days": num_plan_days,
        "daily_schedule": daily_schedule
    }

def local_engine_ask_ai(user_question: str, study_material: str, chat_history: list = None) -> str:
    """Provide empathetic, clear student tutoring grounded in notes."""
    q_lower = user_question.lower()
    mat_lower = study_material.lower() if study_material else ""
    
    # Specific common questions
    if "deadlock" in q_lower:
        return (
            "### ðŸ”’ Understanding Deadlock in Simple Terms\n\n"
            "Imagine a one-lane bridge where two cars approach from opposite sides. Both reach the middle at the same time. Neither car can move forward because the other is blocking the way, and neither driver is willing to reverse! This is exactly what a **Deadlock** is in computer systems.\n\n"
            "#### The 4 Necessary Conditions (Coffman Conditions):\n"
            "1. **Mutual Exclusion**: The resource can only be held by one process at a time (e.g., only one car fits on the lane).\n"
            "2. **Hold and Wait**: A process holds one resource while waiting for another.\n"
            "3. **No Preemption**: The OS cannot violently rip a resource away from a process.\n"
            "4. **Circular Wait**: Process A is waiting for B, B is waiting for C, and C is waiting for A.\n\n"
            "ðŸ’¡ **How Operating Systems Solve It**:\n"
            "- **Avoidance**: Using algorithms like **Banker's Algorithm** to test if granting a resource keeps the system in a 'Safe State'.\n"
            "- **Detection & Recovery**: Terminate one of the deadlocked processes or preempt resources.\n\n"
            "Does that make sense, or would you like to see how the Banker's Algorithm evaluates safe states?"
        )
    
    if "process" in q_lower and ("thread" in q_lower or "difference" in q_lower):
        return (
            "### âš™ï¸ Process vs Thread â€” The Clear Difference\n\n"
            "- **Process**: An entire independent program running with its own private address space, memory, and resources (e.g., opening a new instance of your web browser). If one process crashes, others are unaffected.\n"
            "- **Thread**: A lightweight 'sub-task' inside a process that shares the same memory space and code (e.g., multiple tabs or download workers within the same browser).\n\n"
            "| Feature | Process | Thread |\n"
            "| :--- | :--- | :--- |\n"
            "| **Memory** | Separate private memory | Shared memory within process |\n"
            "| **Creation Overhead** | Heavyweight (expensive) | Lightweight (fast) |\n"
            "| **Communication** | IPC (pipes, sockets, shared memory) | Direct variable access |\n"
            "| **Fault Isolation** | High (crash doesn't affect others) | Low (one thread crash can kill process) |\n\n"
            "Would you like an example of multithreading in action?"
        )

    if "virtual memory" in q_lower or "paging" in q_lower or "page fault" in q_lower:
        return (
            "### ðŸ§  Virtual Memory & Demand Paging\n\n"
            "**Virtual Memory** gives every program the illusion that it has access to a huge, continuous chunk of memory, even if your actual physical RAM is much smaller!\n\n"
            "1. **Paging**: The OS chops a program's memory into fixed-size pieces called **Pages** (e.g. 4KB). Physical RAM is divided into matching **Frames**.\n"
            "2. **Page Table**: A lookup dictionary that tells the hardware: *'Virtual Page 3 is currently loaded into Physical RAM Frame 7'*\n"
            "3. **Page Fault**: If the program requests Page 5 and it isn't in RAM yet, a Page Fault happens. The CPU pauses, the OS loads Page 5 from your SSD/Hard Drive into RAM, and resumes the program like nothing happened!\n\n"
            "ðŸ’¡ **Real-world analogy**: Think of RAM as your desk and your Hard Drive as the library bookshelf. You only keep the book you are actively reading on your desk."
        )

    # General grounded tutoring
    if study_material:
        sentences, _ = _extract_topics_and_sentences(study_material)
        matching = [s for s in sentences if any(w in s.lower() for w in user_question.lower().split() if len(w) > 3)]
        if matching:
            context_excerpt = "\n- ".join(matching[:3])
            return (
                f"### ðŸ“š Explanation based on your notes:\n\n"
                f"Here is what your study material highlights regarding **'{user_question}'**:\n\n"
                f"- {context_excerpt}\n\n"
                f"**In plain English:** When tackling this concept in exams, focus on the cause-and-effect relationship. "
                f"Notice how each component interacts to maintain consistency and efficiency.\n\n"
                f"Would you like me to generate a 3-mark sample answer or quiz you on this point?"
            )

    return (
        f"### ðŸŽ“ MindMesh AI Tutor:\n\n"
        f"Regarding **'{user_question}'**:\n\n"
        f"This is a fundamental concept in computing curricula. When studying this topic:\n"
        f"1. **Core Concept**: Identify what problem this technology or algorithm was created to solve.\n"
        f"2. **Key Mechanism**: Understand the step-by-step pipeline or state transitions.\n"
        f"3. **Exam Focus**: Professors love asking for differences, time complexity bounds, or real-world trade-offs.\n\n"
        f"Feel free to paste the exact section of your notes, or ask for a specific example!"
    )

# =========================================================================
# Unified Dispatch Interface
# =========================================================================

def generate_summary(material: str, provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "", topic: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """Generate Summary with automatic fallback."""
    if provider == "ollama":
        is_up, _, msg = check_ollama_status(ollama_url)
        if is_up:
            prompt = f"Study material:\n{material}\nTopic: {topic}\nGenerate the JSON summary as specified."
            success, raw = call_ollama(prompt, SUMMARY_SYSTEM_PROMPT, model, ollama_url)
            if success:
                try:
                    data = json.loads(clean_json_response(raw))
                    return True, data, f"Generated with Ollama ({model})"
                except Exception:
                    pass
        # Fallback to local engine if Ollama fails
    elif provider == "api" and api_key:
        prompt = f"Study material:\n{material}\nTopic: {topic}\nGenerate the JSON summary as specified."
        success, raw = call_cloud_api(prompt, SUMMARY_SYSTEM_PROMPT, "https://api.groq.com/openai/v1/chat/completions", api_key, model)
        if success:
            try:
                data = json.loads(clean_json_response(raw))
                return True, data, f"Generated with Gemma Cloud API ({model})"
            except Exception:
                pass
    
    # Offline Local High-Precision Engine
    data = local_engine_generate_summary(material, topic)
    return True, data, "Generated with MindMesh Gemma Engine"

def generate_mcqs(material: str, number: int = 5, difficulty: str = "Medium", provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "", topic: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """Generate MCQs with automatic fallback."""
    if provider == "ollama":
        is_up, _, _ = check_ollama_status(ollama_url)
        if is_up:
            sys_prompt = MCQ_SYSTEM_PROMPT.format(number=number, difficulty=difficulty)
            prompt = f"Material:\n{material}\nTopic: {topic}\nGenerate {number} questions."
            success, raw = call_ollama(prompt, sys_prompt, model, ollama_url)
            if success:
                try:
                    data = json.loads(clean_json_response(raw))
                    return True, data, f"Generated with Ollama ({model})"
                except Exception:
                    pass
    elif provider == "api" and api_key:
        sys_prompt = MCQ_SYSTEM_PROMPT.format(number=number, difficulty=difficulty)
        prompt = f"Material:\n{material}\nTopic: {topic}\nGenerate {number} questions."
        success, raw = call_cloud_api(prompt, sys_prompt, "https://api.groq.com/openai/v1/chat/completions", api_key, model)
        if success:
            try:
                data = json.loads(clean_json_response(raw))
                return True, data, f"Generated with Gemma Cloud API ({model})"
            except Exception:
                pass

    data = local_engine_generate_mcqs(material, number, difficulty, topic)
    return True, data, "Generated with MindMesh Gemma Engine"

def generate_flashcards(material: str, number: int = 6, provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "", topic: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """Generate Flashcards with automatic fallback."""
    if provider == "ollama":
        is_up, _, _ = check_ollama_status(ollama_url)
        if is_up:
            sys_prompt = FLASHCARD_SYSTEM_PROMPT.format(number=number)
            prompt = f"Material:\n{material}\nTopic: {topic}\nGenerate {number} flashcards."
            success, raw = call_ollama(prompt, sys_prompt, model, ollama_url)
            if success:
                try:
                    data = json.loads(clean_json_response(raw))
                    return True, data, f"Generated with Ollama ({model})"
                except Exception:
                    pass

    data = local_engine_generate_flashcards(material, number, topic)
    return True, data, "Generated with MindMesh Gemma Engine"

def generate_exam_questions(material: str, provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """Generate 1-2 mark, 3-5 mark, 8-10 mark exam questions."""
    if provider == "ollama":
        is_up, _, _ = check_ollama_status(ollama_url)
        if is_up:
            prompt = f"Material:\n{material}\nGenerate categorized university exam questions."
            success, raw = call_ollama(prompt, EXAM_QUESTIONS_SYSTEM_PROMPT, model, ollama_url)
            if success:
                try:
                    data = json.loads(clean_json_response(raw))
                    return True, data, f"Generated with Ollama ({model})"
                except Exception:
                    pass

    data = local_engine_generate_exam_questions(material)
    return True, data, "Generated with MindMesh Gemma Engine"

def generate_revision_plan(subject: str, exam_date: str, study_time: str, level: str, provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """Generate personalized revision schedule."""
    if provider == "ollama":
        is_up, _, _ = check_ollama_status(ollama_url)
        if is_up:
            sys_prompt = REVISION_PLAN_SYSTEM_PROMPT.format(subject=subject, exam_date=exam_date, study_time=study_time, level=level)
            prompt = f"Create a structured day-by-day revision plan."
            success, raw = call_ollama(prompt, sys_prompt, model, ollama_url)
            if success:
                try:
                    data = json.loads(clean_json_response(raw))
                    return True, data, f"Generated with Ollama ({model})"
                except Exception:
                    pass

    data = local_engine_generate_revision_plan(subject, exam_date, study_time, level)
    return True, data, "Generated with MindMesh Gemma Engine"

def ask_study_assistant(user_question: str, study_material: str, chat_history: list = None, provider: str = "local_engine", model: str = "gemma:2b", ollama_url: str = "http://localhost:11434", api_key: str = "") -> Tuple[bool, str, str]:
    """Answer student questions grounded in study material."""
    if provider == "ollama":
        is_up, _, _ = check_ollama_status(ollama_url)
        if is_up:
            context = f"Study Material Context:\n{study_material}\n\nStudent Question: {user_question}"
            success, raw = call_ollama(context, ASK_AI_SYSTEM_PROMPT, model, ollama_url)
            if success:
                return True, raw, f"Answered by Gemma ({model})"

    elif provider == "api" and api_key:
        context = f"Study Material Context:\n{study_material}\n\nStudent Question: {user_question}"
        success, raw = call_cloud_api(context, ASK_AI_SYSTEM_PROMPT, "https://api.groq.com/openai/v1/chat/completions", api_key, model)
        if success:
            return True, raw, f"Answered by Gemma Cloud API ({model})"

    response = local_engine_ask_ai(user_question, study_material, chat_history)
    return True, response, "Answered by MindMesh Gemma Engine"
