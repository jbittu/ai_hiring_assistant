import json
import streamlit as st
from context_manager import ConversationContext
from gemini_client import generate_technical_questions, evaluate_all_answers
from prompts import info_gathering_prompt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --------------------------
# Helper: Apply Local CSS
# --------------------------
def local_css(styles):
    with open(styles) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------
# Helper: Generate PDF from Evaluation JSON
# --------------------------
def generate_pdf(evaluation_data, file_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    elements.append(Paragraph("<b>TalentScout Interview Summary</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    candidate_info = evaluation_data.get("candidate_info", {})
    elements.append(Paragraph("<b>Candidate Information:</b>", styles['Heading2']))
    for key, value in candidate_info.items():
        elements.append(Paragraph(f"{key}: {value}", styles['Normal']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Technical Interview Results:</b>", styles['Heading2']))
    if "evaluation" in evaluation_data and evaluation_data["evaluation"]:
        eval_results = evaluation_data["evaluation"]["results"]
        total_score = evaluation_data["evaluation"]["summary"]["total_score"]
        avg_score = evaluation_data["evaluation"]["summary"]["average_score"]

        for item in eval_results:
            elements.append(Paragraph(f"Q: {item['question']}", styles['Normal']))
            elements.append(Paragraph(f"Your Answer: {item['answer']}", styles['Normal']))
            elements.append(Paragraph(f"Feedback: {item['feedback']}", styles['Normal']))
            elements.append(Paragraph(f"Score: {item['score']}/5", styles['Normal']))
            elements.append(Spacer(1, 10))

        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"<b>Final Technical Score:</b> {total_score}", styles['Heading3']))
        elements.append(Paragraph(f"<b>Average Score:</b> {avg_score} / 5", styles['Heading3']))

    doc.build(elements)
    return file_path

# --------------------------
# Page Configuration
# --------------------------
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

# --------------------------
# Session State Initialization
# --------------------------
if 'context' not in st.session_state:
    st.session_state.context = ConversationContext()
    st.session_state.chat_history = []
    st.session_state.current_question_index = 0
    st.session_state.technical_questions = []
    st.session_state.interview_log = []
    st.session_state.interview_phase = "info_gathering"
    st.session_state.evaluation = None

context = st.session_state.context

# --------------------------
# Initial Greeting
# --------------------------
if not st.session_state.chat_history:
    st.session_state.chat_history.append(("assistant", "👋 Hello! I'm your virtual hiring assistant for TalentScout."))
    field_index = context.current_field
    if field_index < len(context.fields):
        next_prompt = info_gathering_prompt(context.fields[field_index])
        st.session_state.chat_history.append(("assistant", next_prompt))
    else:
        st.session_state.chat_history.append(("assistant", "Let's start with your basic information."))

# --------------------------
# Display Chat History
# --------------------------
for role, message in st.session_state.chat_history:
    css_class = 'assistant' if role == 'assistant' else 'user'
    st.markdown(f"<div class='{css_class}'>{message}</div>", unsafe_allow_html=True)

# --------------------------
# User Input
# --------------------------
user_input = st.chat_input("Type your response here...")

if user_input:
    if user_input.lower() == "restart":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.session_state.chat_history.append(("user", user_input))

    if user_input.lower() in ["exit", "quit"]:
        context.conversation_ended = True
        st.session_state.chat_history.append(("assistant", "Understood. Ending the conversation."))
        st.rerun()

    # --------------------------
    # Info Gathering Phase
    # --------------------------
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

    # --------------------------
    # Technical Q&A Phase
    # --------------------------
    elif st.session_state.interview_phase == "technical_questions":
        idx = st.session_state.current_question_index
        question = st.session_state.technical_questions[idx]
        st.session_state.interview_log.append({"question": question, "answer": user_input})
        st.session_state.current_question_index += 1

        if st.session_state.current_question_index == len(st.session_state.technical_questions):
            with st.spinner("Evaluating all your answers..."):
                questions = [q["question"] for q in st.session_state.interview_log]
                answers = [q["answer"] for q in st.session_state.interview_log]
                evaluation = evaluate_all_answers(questions, answers)
                st.session_state.evaluation = evaluation

            summary = evaluation["summary"]
            total_score = summary["total_score"]
            avg_score = summary["average_score"]

            #  Only show final result
            st.session_state.chat_history.append((
                "assistant",
                f" All questions answered!<br><br>"
                f" <b>Final Technical Score:</b> {total_score}<br>"
                f" <b>Average Score:</b> {avg_score} / 5<br><br>"
                f"Thank you for completing the technical interview!"
            ))

            st.session_state.interview_phase = "completed"
            st.rerun()
        else:
            next_q = st.session_state.technical_questions[st.session_state.current_question_index]
            st.session_state.chat_history.append(("assistant", f"{next_q}"))
            st.rerun()

# --------------------------
# Generate Technical Questions
# --------------------------
if st.session_state.interview_phase == "generating_questions":
    with st.spinner("Generating technical questions..."):
        tech_stack = context.get_tech_stack()
        questions = generate_technical_questions(tech_stack, num_questions=5)

        if questions:
            st.session_state.technical_questions = questions
            st.session_state.interview_phase = "technical_questions"
            st.session_state.chat_history.append(("assistant", "Let's start the technical interview!"))
            st.session_state.chat_history.append(("assistant", f"{questions[0]}"))
        else:
            st.session_state.chat_history.append(("assistant", "❗ Failed to generate technical questions."))
            st.session_state.interview_phase = "completed"

    st.rerun()

# --------------------------
# End Message + PDF Download
# --------------------------
if context.conversation_ended or st.session_state.interview_phase == "completed":
    eval_data = st.session_state.evaluation
    total_score = eval_data["summary"]["total_score"] if eval_data else 0
    avg_score = eval_data["summary"]["average_score"] if eval_data else 0.0

    st.markdown(f"""
    <div class='assistant'>
     <b>Final Technical Score:</b> {total_score} <br>
     <b>Average Score:</b> {avg_score} / 5
    </div>
    """, unsafe_allow_html=True)

    interview_summary = {
        "candidate_info": context.candidate,
        "tech_stack": context.get_tech_stack(),
        "interview_log": st.session_state.interview_log,
        "evaluation": eval_data
    }

    json_path = "candidate_data/interview_summary.json"
    pdf_path = "candidate_data/interview_summary.pdf"

    with open(json_path, "w") as f:
        json.dump(interview_summary, f, indent=2)

    generate_pdf(interview_summary, pdf_path)

    st.download_button("Download Full Report (JSON)", open(json_path, "rb"), file_name="interview_summary.json")
    st.download_button("Download Interview Report (PDF)", open(pdf_path, "rb"), file_name="interview_summary.pdf")
