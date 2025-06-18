import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads OPENAI_API_KEY from .env

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_technical_questions(tech_stack):
    prompt = (
        f"You are a technical interviewer. "
        f"Given the candidate's tech stack: {tech_stack}, "
        "generate 3-5 technical interview questions for each technology."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']
