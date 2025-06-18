EXIT_KEYWORDS = ["exit", "quit", "bye", "goodbye", "end", "stop"]

class ConversationContext:
    def __init__(self):
        self.fields = [
            "name", "email", "phone", "experience", "position", "location", "tech_stack"
        ]
        self.candidate = {}
        self.current_field = 0
        self.conversation_ended = False

    def handle_input(self, user_input):
        if any(word in user_input.lower() for word in EXIT_KEYWORDS):
            self.conversation_ended = True
            return "Thank you for your time! We will contact you with next steps."
        
        if self.current_field < len(self.fields):
            field = self.fields[self.current_field]
            self.candidate[field] = user_input
            self.current_field += 1

            if self.current_field < len(self.fields):
                from prompts import info_gathering_prompt
                next_field = self.fields[self.current_field]
                return info_gathering_prompt(next_field)
            else:
                return "Thank you for providing your information."
        else:
            return "All information has been collected. Type 'exit' to end the conversation."

    def ready_for_technical_questions(self):
        return self.current_field == len(self.fields)

    def get_tech_stack(self):
        return self.candidate.get("tech_stack", "")

    def set_questions(self, questions):
        self.candidate['questions'] = questions
