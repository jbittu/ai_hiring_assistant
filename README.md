## TalentScout Hiring Assistant

TalentScout Hiring Assistant is a Streamlit-based web application designed to automate and streamline the initial technical screening process for hiring. It interacts with candidates in a conversational format, collects their information, and dynamically generates relevant technical interview questions using Google Gemini AI.

---

## **Features**

- **Conversational UI:** Guides candidates through information collection using a chat interface.
- **Input Validation:** Ensures all candidate data (name, email, phone, etc.) is validated for correctness.
- **Technical Q&A:** Automatically generates technical interview questions based on the candidate’s tech stack.
- **Session Management:** Maintains chat history and conversation context for a seamless user experience.
- **Data Privacy:** Candidate information is stored temporarily and used solely for the hiring process.
- **Export:** Candidates can download a summary of their interview session.

---

## **Project Structure**

```
.
├── app.py
├── context_manager.py
├── gemini_client.py
├── prompts.py
├── requirements.txt
├── styles.css
├── assets/
│   └── icon.png
└── candidate_data/
```

---

## **Installation**

1. **Clone the repository:**
   ```bash
   git clone 
   cd 
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_google_gemini_api_key
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## **Usage**

- Open the provided local URL in your browser.
- The assistant will greet you and sequentially ask for your:
  - Full name
  - Email address
  - Phone number
  - Years of professional experience
  - Desired position(s)
  - Current location
  - Tech stack (languages, frameworks, tools)
- After collecting your information, the assistant generates technical questions based on your tech stack.
- Answer the questions in the chat.
- At the end, you can download a summary of your interview session as a JSON file.

---

## **File Descriptions**

| File                | Purpose                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------|
| `app.py`            | Main Streamlit app. Handles UI, session state, and conversation flow.                   |
| `context_manager.py`| Manages conversation context, validates user input, and saves candidate data.           |
| `gemini_client.py`  | Connects to Google Gemini API to generate technical questions.                          |
| `prompts.py`        | Contains prompts for information gathering.                                             |
| `requirements.txt`  | Lists Python dependencies.                                                              |
| `styles.css`        | Custom CSS for UI styling.                                                              |
| `assets/icon.png`   | Application icon.                                                                       |
| `candidate_data/`   | Stores candidate data and interview summaries.                                          |

---

## **Environment Variables**

- `GOOGLE_API_KEY`: Your Google Gemini API key (required for technical question generation).

---

## **Customization**

- **Prompts:** Modify `prompts.py` to change or add information-gathering questions.
- **Styling:** Edit `styles.css` for UI customization.
- **Question Generation:** Adjust the prompt logic in `gemini_client.py` to tailor the technical questions.

---

## **Security & Privacy**

- Candidate data is stored locally in the `candidate_data/` directory and is not shared externally.
- All data collection is simulated for demonstration; adapt as needed for production use.

---

## **Dependencies**

- `streamlit`: For the web interface.
- `openai`: (Listed, but not used by default; can be adapted for OpenAI models.)
- `python-dotenv`: For loading environment variables.
- `google-generativeai`: For accessing the Gemini API.

---

## **Troubleshooting**

- **API Key Error:** Ensure `GOOGLE_API_KEY` is set in your `.env` file.
- **Dependency Issues:** Double-check that all required packages are installed.
- **File Permissions:** Ensure the app has write access to the `candidate_data/` directory.

---

## **License**

This project is for demonstration and educational use. Adapt and extend as needed for your organization.

---

## **Contact**

For questions, feature requests, or issues, please open an issue or contact the maintainer.



