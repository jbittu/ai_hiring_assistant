import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from fpdf import FPDF


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_technical_questions(role_description, num_questions=5):
    """
    Generate technical questions based on role or skills.
    """
    prompt = f"""
    Generate {num_questions} technical interview questions for this role:
    {role_description}
    Only output the list of questions in plain text, one per line.
    """
    response = model.generate_content(prompt)
    return [q.strip("- ").strip() for q in response.text.strip().split("\n") if q.strip()]

def evaluate_all_answers(questions, answers):
    """
    Evaluate all answers at once using Gemini.
    Returns structured feedback with per-question scores and an overall summary.
    """
    qa_text = "\n".join(
        [f"Q{i+1}: {questions[i]}\nA{i+1}: {answers[i]}" for i in range(len(questions))]
    )

    prompt = f"""
    You are a senior technical interviewer evaluating a candidate's responses.
    Below are several technical questions and their answers.

    For each, provide:
      - "score" (integer 0–5)
      - "feedback" (short, constructive comment)

    Return *only valid JSON*, in this format:
    {{
      "results": [
        {{"question": "...", "answer": "...", "score": 5, "feedback": "..."}},
        ...
      ],
      "summary": {{
        "total_score": <int>,
        "average_score": <float>
      }}
    }}

    Evaluate this input:
    {qa_text}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 600,
                "response_mime_type": "application/json"
            }
        )

        import json, re
        text = response.text.strip()

        # Clean out any non-JSON wrapping (e.g., ```json ... ```)
        text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE)

        result = json.loads(text)
        return result

    except Exception as e:
        print("Evaluation error:", e)
        return {
            "results": [
                {"question": q, "answer": a, "score": 0, "feedback": "Evaluation failed."}
                for q, a in zip(questions, answers)
            ],
            "summary": {"total_score": 0, "average_score": 0.0}
        }
