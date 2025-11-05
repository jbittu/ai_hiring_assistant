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
