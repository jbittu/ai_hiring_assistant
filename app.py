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
<p style='text-align:center; color:#22577A; font-size:1.1rem;'>
Welcome! I'm your virtual hiring assistant. I'll guide you through a quick screening process.<br>
Type <b>'exit'</b> anytime to end the conversation.
</p>
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
        st.session_state.chat_history.append(("assistant", info_gathering_prompt(context.fields[field_index])))

# Display Chat History
for role, message in st.session_state.chat_history:
    css_class = 'assistant' if role == 'assistant' else 'user'
    st.markdown(f"<div class='{css_class}'>{message}</div>", unsafe_allow_html=True)

# User Input
user_input = st.chat_input("Type your response here...")

if user_input and not context.conversation_ended:
    st.session_state.chat_history.append(("user", user_input))

    if user_input.lower() == 'exit':
        context.conversation_ended = True
        st.rerun()

    if st.session_state.interview_phase == "info_gathering":
        reply = context.handle_input(user_input)
        st.session_state.chat_history.append(("assistant", reply))

        if context.ready_for_technical_questions():
            st.session_state.interview_phase = "generating_questions"
            st.session_state.chat_history.append(("assistant", "Please wait, I'm generating technical questions..."))
        st.rerun()

    elif st.session_state.interview_phase == "technical_questions":
        idx = st.session_state.current_question_index
        question = st.session_state.technical_questions[idx]
        st.session_state.interview_log.append(f"Q{idx+1}: {question}\nA{idx+1}: {user_input}")
        st.session_state.current_question_index += 1

        if st.session_state.current_question_index < len(st.session_state.technical_questions):
            next_q = st.session_state.technical_questions[st.session_state.current_question_index]
            st.session_state.chat_history.append(("assistant", f"{next_q}"))
        else:
            st.session_state.chat_history.append(("assistant", "Thank you! You've completed the technical interview."))
            st.session_state.interview_phase = "completed"
        st.rerun()

# Generate Questions
if st.session_state.interview_phase == "generating_questions":
    with st.spinner("Generating technical questions..."):
        tech_stack = context.get_tech_stack()
        questions = generate_technical_questions(tech_stack, num_questions=4)
        if questions:
            st.session_state.technical_questions = questions
            st.session_state.interview_phase = "technical_questions"
            st.session_state.current_question_index = 0
            first_q = questions[0]
            st.session_state.chat_history.append(("assistant", " Let's start the technical interview!"))
            st.session_state.chat_history.append(("assistant", f"{first_q}"))
        else:
            st.session_state.chat_history.append(("assistant", "❗ Failed to generate technical questions."))
            st.session_state.interview_phase = "completed"
    st.rerun()

# End message
if context.conversation_ended or st.session_state.interview_phase == "completed":
    st.markdown("<div class='assistant'> Conversation ended. Thank you for participating!</div>", unsafe_allow_html=True)


