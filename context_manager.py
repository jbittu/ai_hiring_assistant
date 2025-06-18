import re
from prompts import info_gathering_prompt

EXIT_KEYWORDS = ["exit", "quit", "bye", "goodbye", "end", "stop"]

# Validation functions
def validate_name(name): 
    return bool(re.match(r"^[A-Za-z][A-Za-z\s'\-]{1,}[A-Za-z]$", name.strip()))

def validate_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))

def validate_phone(phone):
    return bool(re.match(r"^\+?[\d\s\-]{10,15}$", phone.strip()))

def validate_experience(exp):
    try:
        value = float(exp)
        return 0 <= value <= 50
    except ValueError:
        return False

def validate_position(pos):
    return bool(re.match(r"^[A-Za-z][A-Za-z\s'\-]{1,}[A-Za-z]$", pos.strip()))

def validate_location(loc):
    return bool(re.match(r"^[A-Za-z][A-Za-z\s'\-]{1,}[A-Za-z]$", loc.strip()))

def validate_tech_stack(stack):
    return len(stack.strip()) >= 3  

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

            # Field-specific validation
            if field == "name" and not validate_name(user_input):
                return "❗ Invalid name. Use letters only; spaces, hyphens, and apostrophes are allowed."

            if field == "email" and not validate_email(user_input):
                return "❗ Invalid email format. Please enter a valid email like example@domain.com."

            if field == "phone" and not validate_phone(user_input):
                return "❗ Invalid phone number. Use 10–15 digits with optional +, -, or spaces."

            if field == "experience" and not validate_experience(user_input):
                return "❗ Please enter your years of experience as a number between 0 and 50."

            if field == "position" and not validate_position(user_input):
                return "❗ Invalid position title. Please enter a proper job title (letters, spaces, hyphens)."

            if field == "location" and not validate_location(user_input):
                return "❗ Invalid location. Please enter a city or region using letters only."

            if field == "tech_stack" and not validate_tech_stack(user_input):
                return "❗ Please mention at least one technology or tool you're familiar with."

            # Store validated input
            self.candidate[field] = user_input
            self.current_field += 1

            # Move to next question
            if self.current_field < len(self.fields):
                return info_gathering_prompt(self.fields[self.current_field])
            else:
                return " Thank you! All required information has been collected."

        else:
            return "ℹ All information has already been collected. Type 'exit' to end the conversation."

    def ready_for_technical_questions(self):
        return self.current_field == len(self.fields)

    def get_tech_stack(self):
        return self.candidate.get("tech_stack", "")

    def set_questions(self, questions):
        self.candidate['questions'] = questions
