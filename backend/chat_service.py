import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the project root (parent of backend)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

# System instruction to guide the persona
BASE_SYSTEM_INSTRUCTION = """
You are a helpful and knowledgeable science tutor specialized in Chemistry, Physics, and Biology. 
Your goal is to help students understand scientific concepts, solve problems, and explore these fields.
While you can engage in general conversation, always try to bring the context back to science when relevant.
Be encouraging, clear, and accurate. 
If a user asks a question that is clearly outside the scope of a general tutor (e.g. advice on illegal acts, medical diagnosis), politely decline.
"""

def get_chat_response(history_messages, user_input, student_class="General"):
    """
    Generates a response using Google Gemini.
    history_messages: List of dicts, e.g. [{"role": "user", "content": "hi"}, {"role": "model", "content": "hello"}]
    user_input: The current user message.
    student_class: The grade level of the student (e.g., "5th", "12th").
    """
    
    # Customize instruction based on class
    custom_instruction = BASE_SYSTEM_INSTRUCTION + f"""
    
    IMPORTANT: The student is in {student_class}. Adjust your language, complexity, and examples to be appropriate for a {student_class} student.
    
    AT THE END OF YOUR RESPONSE:
    Provide 3 "Curiosity Follow-up Questions" that are related to the topic but slightly more advanced, to encourage further learning. 
    Format them clearly as a list.
    """

    try:
        if not API_KEY or API_KEY == "your_api_key_here":
            # Mock mode for testing UI
            import time
            time.sleep(1) # Simulate network delay
            return f"**[MOCK MODE]** This is a simulated response because the API key is missing.\n\nYou asked: '{user_input}'.\n\nI am acting as a {student_class} tutor."

        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=custom_instruction)
        
        # Convert history to Gemini format if needed (list of Content objects or dicts)
        # Gemini python lib expects history as a list of dicts with 'role' and 'parts' usually, 
        # or simplified 'role' and 'parts'.
        # 'role': 'user' or 'model'
        
        formatted_history = []
        for msg in history_messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})
            
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "I'm sorry, I'm having trouble connecting to the science lab right now. Please check my API key or try again later."
