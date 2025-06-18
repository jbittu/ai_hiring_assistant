
def info_gathering_prompt(field):
    prompts = {
        "name": "Please provide your full name.",
        "email": "What is your email address?",
        "phone": "What is your phone number?",
        "experience": "How many years of professional experience do you have?",
        "position": "What position(s) are you interested in?",
        "location": "Where are you currently located?",
        "tech_stack": "Please list the programming languages, frameworks, databases, and tools you are proficient in."
    }
    return prompts.get(field, "Please provide the requested information.")

def tech_questions_prompt(tech_stack):
    return (
        f"You are an expert technical interviewer. "
        f"Given a candidate with the following tech stack: {tech_stack}, "
        "generate 3-5 interview questions for each technology to assess their proficiency. "
        "Questions should be clear, relevant, and vary in difficulty."
    )
