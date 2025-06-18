import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_technical_questions(tech_stack, num_questions=4):
    prompt = (
        f"You are a technical interviewer. Given the candidate's tech stack: {tech_stack}, "
        f"generate {num_questions} distinct technical interview questions. Each question should be challenging, clear, and relevant to assess the candidate's skills. "
        "Present each question on a new line, numbered, and DO NOT provide answers."
    )
    try:
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 500, "temperature": 0.7})
        questions_text = response.text
        questions = [q.strip() for q in questions_text.split('\n') if q.strip() and q.strip()[0].isdigit()]
        return questions[:num_questions]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []


