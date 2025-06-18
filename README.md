# TalentScout Hiring Assistant Chatbot

## Overview
A Streamlit-based intelligent chatbot for candidate screening, powered by GPT-3.5/4.

## Features
- Gathers candidate info step-by-step
- Generates technical questions based on tech stack
- Graceful fallback and exit handling

## Installation
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenAI API key to a `.env` file
4. Run: `streamlit run app.py`

## Usage
- Follow on-screen prompts
- Type 'exit' to end conversation

## Technical Details
- Python, Streamlit, OpenAI GPT-3.5/4
- Modular code structure

## Prompt Design
- See `prompts.py` for prompt templates

## Challenges & Solutions
- Context management
- Prompt engineering for relevant question generation

## License
MIT
