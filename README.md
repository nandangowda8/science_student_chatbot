# science_student_chatbot
# 🤖 SCIBUDDY – AI Science Learning Chatbot

SCIBUDDY is an AI-powered science chatbot designed for students across different grade levels.  
It provides interactive, rank-based learning experiences with a modern **Vibrant Glass UI** and an intelligent backend powered by **Gemini 1.5 Flash**.

---

## ✨ Project Overview

SCIBUDDY helps students:
- Explore science concepts interactively
- Learn according to their grade level
- Save chat history and sessions
- Discover topics using Quick Discoveries

The app is built with a full-stack Python architecture:
- Streamlit frontend for UI, animations, and state handling
- FastAPI backend for session management and routing
- Chat Service module for rank-based prompting
- SQLite database for storing chat history and sessions

---

## 🚀 Features

- 🎨 Vibrant Glass UI with smooth animations
- 🤖 AI-powered chatbot using Gemini 1.5 Flash
- 🧭 Grade-based learning modes:
  - Junior Explorer (5th–6th)
  - Science Cadet (7th–8th)
  - Research Associate (9th–10th)
  - Innovation Fellow (11th–12th)
- ⚡ Quick Discoveries topic suggestions
- 🔄 Session management (Mission Log)
- 💬 Chat history storage using SQLite
- 📡 REST API backend with FastAPI
- 🔐 Secure API key handling using environment variables
- 🖥️ Local deployment with Streamlit

---

## 🛠️ Tech Stack

### Frontend
- Streamlit (Vibrant Glass UI)
- State management and animations
- User input handling

### Backend
- FastAPI (REST API)
- Session management and routing

### AI Engine
- Gemini 1.5 Flash (LLM API)
- Rank-specific prompt engineering

### Database
- SQLite (local database)
- Stores chat history and active sessions

### Language & Tools
- Python
- Git & GitHub

---

## 📂 Project Structure

SCIBUDDY/
│
├── frontend/
│ └── app.py # Streamlit frontend (UI & animations)
│
├── backend/
│ ├── main.py # FastAPI backend
│ ├── chat_service.py # Gemini prompt handling
│ ├── database.py # SQLite database logic
│ └── requirements.txt
│
├── screenshots/
│ └── ui.png
│
├── README.md
├── .gitignore
└── .env (not uploaded)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
git clone https://github.com/nandangowda8/SCIBUDDY.git
cd SCIBUDDY

### 2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install dependencies
pip install -r backend/requirements.txt

### 🔐 Environment Variables
Create a .env file in the backend folder and add:
GEMINI_API_KEY=your_api_key_here

### ▶️ Run the Backend (FastAPI)
uvicorn backend.main:app --reload

### ▶️ Run the Frontend (Streamlit)
Open another terminal and run:
streamlit run frontend/app.py

---

## 🧠 How It Works

1. User selects a learning grade (Junior Explorer, Science Cadet, Research Associate, or Innovation Fellow).
2. Streamlit frontend captures user input and manages UI state and animations.
3. User queries are sent to the FastAPI backend through REST API endpoints.
4. Backend routes the request to the Chat Service module.
5. Chat Service prompts Gemini 1.5 Flash with grade-specific instructions.
6. The AI generates a response based on the selected learning level.
7. Chat history and session data are stored in a local SQLite database.
8. The response is returned to the Streamlit frontend and displayed to the user in real time.
9. Previous sessions are listed in the Mission Log for easy access.

---

## 📸 Screenshots

### 🏠 Home Screen – Grade Selection
This screen allows students to select their learning level (Junior Explorer, Science Cadet, Research Associate, Innovation Fellow).

![Home Screen](https://github.com/nandangowda8/science_student_chatbot/blob/ba4874d7076664bdc8cb344dbb7bd3a19b9f98b3/2026-02-04.png)

---

### 🌱 Junior Explorer Mode
Chat interface for Junior Explorer level with simple explanations and friendly responses.

![Junior Explorer](https://github.com/nandangowda8/science_student_chatbot/blob/a416be7ba620676048a55f2b6828642843ab4476/Screenshot%20(33)%20-%20Copy.png)

---

### 🔬 Research Associate Mode
Advanced learning mode with deeper scientific explanations and Quick Discoveries feature.

![Research Associate]()

---

### 🚀 Innovation Fellow Mode
Highest learning level designed for senior students with advanced science topics and structured responses.

![Innovation Fellow]()

---

### 📜 Mission Log (Session History)
Displays previous chat sessions and allows users to revisit or delete past missions.

![Mission Log](https://github.com/nandangowda8/science_student_chatbot/blob/0dbeb08677902461c9a0bc361e1879c30c391501/Screenshot%20(37).png)

---

### ⚡ Quick Discoveries
Predefined topic buttons that help users quickly explore popular science topics.

![Quick Discoveries]()


---

## 🎯 Future Enhancements

- User authentication and profiles
- Voice input and text-to-speech support
- Support for additional subjects (Math, Physics, Chemistry)
- Cloud database integration
- Mobile-friendly responsive UI
- Deployment to cloud platforms (Streamlit Cloud / AWS / Azure)
- Analytics dashboard for learning progress
- Multi-language support

---

## 👨‍🎓 Author

**Nandan Gowda**  
Student Developer – SCIBUDDY AI Science Chatbot  
Built using FastAPI, Streamlit, Python, and Gemini LLM API


