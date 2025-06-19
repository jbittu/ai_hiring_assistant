import json
import streamlit as st
from context_manager import ConversationContext
from gemini_client import generate_technical_questions
from prompts import info_gathering_prompt

def local_css(styles):
    with open(styles) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page Config
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="assets/icon.png", layout="wide")
local_css("styles.css")

st.markdown("<div class='title'> TalentScout Hiring Assistant</div>", unsafe_allow_html=True)
st.markdown("""
<span class='titledis'>
Welcome! I'm your virtual hiring assistant. I'll guide you through a quick screening process.
Type 'exit' anytime to end the conversation.
</span>
""", unsafe_allow_html=True)
st.markdown("""
<div class='privacy-notice'>
<b>Data Privacy Notice:</b>
Your information is stored temporarily and used solely for this hiring process.
We do not store or share any personal data externally.

</div>
""", unsafe_allow_html=True)
# Session State Init
if 'context' not in st.session_state:
    st.session_state.context = ConversationContext()
    st.session_state.chat_history = []
    st.session_state.current_question_index = 0
    st.session_state.technical_questions = []
    st.session_state.interview_log = []
    st.session_state.interview_phase = "info_gathering"

context = st.session_state.context

# Initial Greeting 
if not st.session_state.chat_history:
    st.session_state.chat_history.append(("assistant", " Hello! I'm your virtual hiring assistant for TalentScout."))
    field_index = context.current_field
    if field_index < len(context.fields):
        next_prompt = info_gathering_prompt(context.fields[field_index])
        if next_prompt:
            st.session_state.chat_history.append(("assistant", next_prompt))
        else:
            st.session_state.chat_history.append(("assistant", "Let's start with your basic information."))

# Display Chat History
for role, message in st.session_state.chat_history:
    css_class = 'assistant' if role == 'assistant' else 'user'
    st.markdown(f"<div class='{css_class}'>{message}</div>", unsafe_allow_html=True)

# User Input
user_input = st.chat_input("Type your response here...")

if user_input:
    # Restart if user requests it
    if user_input.lower() == "restart":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    st.session_state.chat_history.append(("user", user_input))

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        context.conversation_ended = True
        st.session_state.chat_history.append(("assistant", "Understood. Ending the conversation."))
        st.rerun()

    # Info Gathering Phase with Fallback
    if st.session_state.interview_phase == "info_gathering":
        try:
            reply = context.handle_input(user_input)
        except Exception:
            reply = "❗ Sorry, I couldn't understand that. Could you please rephrase?"

        st.session_state.chat_history.append(("assistant", reply))

        if context.ready_for_technical_questions():
            st.session_state.interview_phase = "generating_questions"
            st.session_state.chat_history.append(("assistant", "Generating technical questions..."))

        st.rerun()

    # Technical Q&A Phase with Fallback
    elif st.session_state.interview_phase == "technical_questions":
        if not user_input.strip():
            st.session_state.chat_history.append(("assistant", "Please enter a meaningful answer so we can continue."))
            st.rerun()

        idx = st.session_state.current_question_index
        question = st.session_state.technical_questions[idx]
        st.session_state.interview_log.append(f"Q{idx+1}: {question}\nA{idx+1}: {user_input}")
        st.session_state.current_question_index += 1

        if st.session_state.current_question_index < len(st.session_state.technical_questions):
            next_q = st.session_state.technical_questions[st.session_state.current_question_index]
            st.session_state.chat_history.append(("assistant", f"{next_q}"))
        else:
            st.session_state.chat_history.append(("assistant", " Thank you! You've completed the technical interview."))

            # Save candidate data
            saved_path = context.save_candidate_data()
            st.session_state.chat_history.append(("assistant", f" Your data has been saved securely for evaluation (simulation only)."))
            st.session_state.interview_phase = "completed"

            

        st.rerun()

# Generate Technical Questions
if st.session_state.interview_phase == "generating_questions":
    with st.spinner("Generating technical questions..."):
        tech_stack = context.get_tech_stack()
        questions = generate_technical_questions(tech_stack, num_questions=4)

        if questions:
            st.session_state.technical_questions = questions
            st.session_state.interview_phase = "technical_questions"
            st.session_state.current_question_index = 0
            st.session_state.chat_history.append(("assistant", "Let's start the technical interview!"))
            st.session_state.chat_history.append(("assistant", f"{questions[0]}"))
        else:
            st.session_state.chat_history.append(("assistant", "❗ Failed to generate technical questions."))
            st.session_state.interview_phase = "completed"

    st.rerun()

#  End Message
if context.conversation_ended or st.session_state.interview_phase == "completed":
    st.markdown("""
    <div class='assistant'>
     Thank you for completing the interview!<br>
    We’ll review your responses and contact you with next steps.<br><br>
    You can now close this window or type <b>'restart'</b> to begin again.
    </div>
    """, unsafe_allow_html=True)

    interview_summary = {
        "candidate_info": context.candidate,
        "tech_stack": context.get_tech_stack(),
        "interview_log": [
            {
                "question": st.session_state.technical_questions[i],
                "answer": st.session_state.interview_log[i].split('\nA')[1] if '\nA' in st.session_state.interview_log[i] else ""
            }
            for i in range(len(st.session_state.interview_log))
        ]
    }

    saved_path = "candidate_data/interview_summary.json"
    with open(saved_path, "w") as f:
        json.dump(interview_summary, f, indent=2)

    with open(saved_path, "rb") as f:
        st.download_button(" Download My Interview Summary (JSON)", f, file_name="interview_summary.json")
