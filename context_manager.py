import re
from prompts import info_gathering_prompt

EXIT_KEYWORDS = ["exit", "quit", "bye", "goodbye", "end", "stop"]

def validate_name(name): 
    return bool(re.match(r"^[A-Za-z][A-Za-z\s'\-]{1,}[A-Za-z]$", name.strip()))

def validate_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))

def validate_phone(phone):
    return bool(re.match(r"^\+?[\d\s\-]{10,15}$", phone.strip()))

class ConversationContext:
    def __init__(self):
        self.fields = [
            "name", "email", "phone", "experience", "position", "location", "tech_stack"
        ]
        self.candidate = {}
        self.current_field = 0
        self.conversation_ended = False

    def handle_input(self, user_input):
        user_input = user_input.strip()

        if any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS):
            self.conversation_ended = True
            return "Thank you for your time! We will contact you with next steps."

        if self.current_field < len(self.fields):
            field = self.fields[self.current_field]

            # Validation
            if field == "name" and not validate_name(user_input):
                return "❗ Invalid name. Please enter your full name using letters only (spaces and hyphens allowed)."

            if field == "email" and not validate_email(user_input):
                return "❗ Invalid email format. Please enter a valid email like example@domain.com."

            if field == "phone" and not validate_phone(user_input):
                return "❗ Invalid phone number. Please enter 10–15 digits, optionally with +, -, or spaces."

            
            self.candidate[field] = user_input
            self.current_field += 1

            if self.current_field < len(self.fields):
                return info_gathering_prompt(self.fields[self.current_field])
            else:
                return " Thank you! All required information has been collected."

        else:
            return " All information has already been collected. Type 'exit' to end the conversation."

    def ready_for_technical_questions(self):
        return self.current_field == len(self.fields)

    def get_tech_stack(self):
        return self.candidate.get("tech_stack", "")

    def set_questions(self, questions):
        self.candidate['questions'] = questions
