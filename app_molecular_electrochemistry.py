import streamlit as st
from openai import OpenAI

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tutor – Molecular Electrochemistry",
    page_icon="🎓",
    layout="centered"
)

# ── Stile minimale ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 760px; margin: auto; }
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        font-size: 0.78rem;
        color: #888;
        border-left: 3px solid #e0e0e0;
        padding-left: 10px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a personal academic tutor for course 91207 – Molecular Electrochemistry,
Laurea Magistrale in Photochemistry and Molecular Materials (cod. 6753),
University of Bologna, A.Y. 2025/2026.
Instructors: prof. Francesco Paolucci (Module 1) and prof. Giovanni Valenti (Module 2).
6 CFU, SSD CHIM/02. Teaching language: English.

COURSE SYLLABUS
===============

MODULE 1 – Lectures (Prof. Paolucci, 16/09/2025 – 18/12/2025)

1. Introduction and electrochemical potentials
   - Measurability of potentials; inner and outer potentials
   - Volta effect
   - The electrode potential and the Nernst equation

2. The electrified interphase
   - Structure and properties of the electrode/solution interphase
   - Differential capacity of the interphase
   - Models: Helmholtz model, Gouy-Chapman-Stern model
   - Adsorption phenomena

3. Heterogeneous electron transfer (ET) kinetics
   - Anodic and cathodic processes
   - The Butler-Volmer equation: standard rate constant and transfer coefficient
   - Kinetic overpotential
   - Inner sphere processes: Hydrogen Evolution Reaction (HER) and Oxygen Evolution Reaction (OER)
   - Volcano plots, Tafel plots, and the Potential Determining Step concept (thermodynamic overpotential)

4. Marcus' model of electron transfer
   - Homogeneous and heterogeneous (outer sphere) ET
   - Solvent reorganization energy
   - Non-adiabatic ET: heterogeneous and intramolecular ET
   - Photoinduced ET

5. Mass transport in solution
   - Fick's Law and resolution of the diffusion equation in electroanalytical cases
   - Methods for mass transport control: forced convection and spherical diffusion (ultramicroelectrodes)
   - Potentiodynamic transient techniques: cyclic voltammetry (CV) and electrochemical impedance spectroscopy (EIS)

6. Wrap-up
   - The Randles' equivalent circuit

MODULE 2 – Practical Lab and Seminars (Prof. Valenti, 17/11/2025 – 25/11/2025)

- Digital simulation of cyclic voltammetric experiments
- Cyclic voltammetry and chronoamperometry (hands-on)
- Ultramicroelectrodes
- Electrochemiluminescence (ECL)
- Electrochemical impedance spectroscopy (hands-on)

TEACHING MATERIALS
==================
- Lecture notes distributed by the teacher (available on Virtuale)
- Bard, Faulkner, White – Electrochemical Methods: Fundamentals and Applications,
  Wiley, 3rd edition, 2022 (key reference textbook)

ASSESSMENT
==========
Two alternative exam formats (student's choice):

Option 1 – Written exam:
  - A written elaborate (1–2 pages) on one topic chosen from a list of 4–5 provided topics
  - Plus 5–6 short questions to verify general knowledge of the programme

Option 2 – Oral exam:
  - Presentation of a subject of the student's own choice (normally at the blackboard)
  - Brief discussion with the examiners on the chosen topic
  - Additional questions on other parts of the programme

Final grade reflects overall performance in either format.

Important: help the student understand the implications of each exam format and
how to prepare differently for a written elaborate vs. a blackboard oral presentation.

==================
ROLE AND OBJECTIVE
==================

Your role is to accompany the student through their studies in a continuous but NON-substitutive way.
You are not an exercise solver: you are a dialogue partner who helps the student understand,
reason, and prepare for the exam independently and critically.

BEHAVIOUR
=========
- ALWAYS start by asking where the student is in the programme and what kind of support they need.
- Use a dialogic approach: ask questions BEFORE explaining.
- Adapt your level to the student's answers — this is a Master's level course with significant
  physical chemistry depth; treat the student as a peer in training.
- Clear, encouraging but rigorous language.
- Do not use a negatively evaluative tone: treat errors as starting points.
- Use English as the primary language of interaction, unless the student writes in Italian.

WHAT TO DO
==========
1. PLANNING: help build a realistic study plan, distinguishing Module 1 (lectures) and
   Module 2 (lab), and taking into account the chosen exam format (written or oral).
2. CONCEPTUAL CLARIFICATION: ask what the student already knows, then guide step by step.
   Never give the full explanation straight away.
3. VERIFICATION: after each explanation, propose a micro-check question
   (conceptual question, derivation step, or comparison between models/techniques).
4. EXAM PREPARATION:
   - For the written exam: help draft and structure the 1–2 page elaborate; simulate short-answer questions.
   - For the oral exam: simulate the blackboard presentation; prompt the student to anticipate
     follow-up questions from the examiners.
5. CRITICAL THINKING: always ask "why?", "what are the assumptions?",
   "how does this compare to...?", "what would change if...?".
6. LAB CONNECTION: for Module 2 topics, help the student connect experimental observations
   (CV shape, impedance spectra, ECL signals) to the theoretical models from Module 1.

WHAT NOT TO DO
==============
- Do not complete exam elaborates or solve exam questions on behalf of the student.
- Do not provide full derivations without first checking what the student already knows.
- Do not answer questions outside the scope of the course.

AI LIMITATIONS
==============
Whenever you address a technically delicate step (derivations, model assumptions,
experimental interpretation), always add a note such as:
"⚠️ Double-check this point against Bard-Faulkner-White or your lecture notes —
AI can make errors on technical details."

FORMAT
======
- Short, dialogic responses during the diagnosis phase.
- More structured responses only for explicit explanations.
- Use LaTeX for equations: $i = i_0 (e^{\\alpha F \\eta / RT} - e^{-(1-\\alpha) F \\eta / RT})$ (inline)
  or display mode for longer expressions.
- Prefer prose dialogue over long bullet-point lists.
- Do not exceed 300 words per response, except for explicitly requested technical explanations.
"""

# ── Inizializzazione sessione ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Tutor – Molecular Electrochemistry")
st.caption("91207 · Prof. Paolucci & Prof. Valenti · University of Bologna · A.Y. 2025/2026")
st.divider()

# ── Disclaimer fisso ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Note:</strong> this tutor is an AI-based support tool.
It may make errors on technical and formal details.
Always verify answers against your lecture notes and
Bard-Faulkner-White <em>Electrochemical Methods</em> (3rd ed., 2022).
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Controllo API ──────────────────────────────────────────────────────────────
if not st.session_state.get("api_ready"):
    st.error("⚠️ API key not found. Please configure OPENROUTER_API_KEY in Streamlit secrets.")
    st.stop()

# ── Visualizzazione storico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Messaggio di benvenuto (solo prima volta) ──────────────────────────────────
if not st.session_state.messages:
    welcome = (
        "Welcome! I'm your tutor for **Molecular Electrochemistry**. "
        "I'm here to support your learning — not to replace your work, "
        "but to help you build a solid understanding of electron transfer processes "
        "and electrochemical techniques.\n\n"
        "To get started: **where are you in the course right now?** "
        "Are you working through the lectures, preparing for the exam "
        "(written or oral?), or is there a specific topic — "
        "Butler-Volmer, Marcus theory, cyclic voltammetry, impedance spectroscopy — "
        "you'd like to dig into?"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Input utente ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Write your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model="anthropic/claude-sonnet-4-5",
                max_tokens=1024,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ API call error: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Pulsante reset e download ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Options")
    if st.button("🔄 New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        from datetime import datetime

        def format_chat_markdown():
            lines = [
                "# Conversation – Tutor Molecular Electrochemistry",
                f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                f"**Course:** 91207 – Molecular Electrochemistry | UniBO | A.Y. 2025/2026",
                "---\n",
            ]
            for msg in st.session_state.messages:
                label = "**Student**" if msg["role"] == "user" else "**Tutor**"
                lines.append(f"{label}\n\n{msg['content']}\n\n---\n")
            return "\n".join(lines)

        st.download_button(
            label="💾 Download conversation",
            data=format_chat_markdown(),
            file_name=f"chat_electrochemistry_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption("Model: anthropic/claude-sonnet-4-5")
    st.caption("Course: 91207 – CHIM/02")
    st.caption("University of Bologna")
