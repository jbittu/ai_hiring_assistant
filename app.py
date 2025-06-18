# app.py

import streamlit as st
from context_manager import ConversationContext
from llm_utils import generate_technical_questions
from prompts import info_gathering_prompt

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
st.title("TalentScout Hiring Assistant 🤖")

if 'context' not in st.session_state:
    st.session_state.context = ConversationContext()
    st.session_state.chat_history = []
    st.session_state.asked_questions = False

context = st.session_state.context

# Initial greeting
if not st.session_state.chat_history:
    greeting = (
        "Hello! I'm your virtual hiring assistant for TalentScout. "
        "I'll ask you a few questions to get started with your application. "
        "You can type 'exit' anytime to end the conversation."
    )
    st.session_state.chat_history.append(("assistant", greeting))
    st.session_state.chat_history.append(("assistant", info_gathering_prompt(context.fields[0])))

for role, message in st.session_state.chat_history:
    if role == "assistant":
        st.chat_message("assistant").write(message)
    else:
        st.chat_message("user").write(message)

user_input = st.chat_input("Type your response here...")

if user_input and not context.conversation_ended:
    st.session_state.chat_history.append(("user", user_input))
    response = context.handle_input(user_input)
    st.session_state.chat_history.append(("assistant", response))

    if context.ready_for_technical_questions() and not st.session_state.asked_questions:
        tech_stack = context.get_tech_stack()
        questions = generate_technical_questions(tech_stack)
        context.set_questions(questions)
        st.session_state.chat_history.append(("assistant", "Here are your technical questions:"))
        st.session_state.chat_history.append(("assistant", questions))
        st.session_state.asked_questions = True

    st.experimental_rerun()
elif context.conversation_ended:
    st.chat_message("assistant").write("Thank you for your time! The conversation has ended.")

