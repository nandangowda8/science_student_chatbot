from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from . import crud, models, database, chat_service

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Science Tutor Chatbot")

# CORS to allow Streamlit to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateSessionRequest(BaseModel):
    student_class: str

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    message: str
    student_class: Optional[str] = "General" # Optional, used if creating new session implicitly

class ChatResponse(BaseModel):
    session_id: int
    message: str
    role: str
    student_class: str

class SessionInfo(BaseModel):
    id: int
    created_at: str
    student_class: str

@app.post("/sessions", response_model=SessionInfo)
def create_session_endpoint(request: CreateSessionRequest, db: Session = Depends(get_db)):
    session = crud.create_session(db, student_class=request.student_class)
    return SessionInfo(id=session.id, created_at=session.created_at.isoformat(), student_class=session.student_class)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Get or Create Session
    if request.session_id:
        session = crud.get_session(db, request.session_id)
        if not session:
             # Fallback: Create new if not found
             session = crud.create_session(db, student_class=request.student_class or "General")
    else:
        session = crud.create_session(db, student_class=request.student_class or "General")
    
    session_id = session.id
    student_class = session.student_class
    
    # 2. Save User Message
    crud.create_message(db, session_id, "user", request.message)
    
    # 3. Get History for Context
    # We fetch all messages to pass context to the LLM
    # In a real app, you might limit this to the last N messages
    db_messages = crud.get_session_messages(db, session_id)
    history = [{"role": m.role, "content": m.content} for m in db_messages if m.role != "system"] # Exclude current msg which we just added? 
    # Actually, chat_service.get_chat_response takes history excluding the *current* user input usually, 
    # or we let the chat object handle it. 
    # Let's align with chat_service: it takes history + new_input.
    # So history should NOT include the latest user message we just saved, strictly speaking, 
    # OR we pass the full history to start_chat (if it continues) and then send nothing? No, send_message needs input.
    # We will pass history excluding the *latest* user message.
    
    history_for_llm = [{"role": m.role, "content": m.content} for m in db_messages[:-1]]

    # 4. Get LLM Response
    response_text = chat_service.get_chat_response(history_for_llm, request.message, student_class=student_class)
    
    # 5. Save Model Response
    crud.create_message(db, session_id, "model", response_text)
    
    return ChatResponse(session_id=session_id, message=response_text, role="model", student_class=student_class)

@app.get("/history/{session_id}")
def get_history(session_id: int, db: Session = Depends(get_db)):
    messages = crud.get_session_messages(db, session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found")
    return [{"role": m.role, "content": m.content} for m in messages]

@app.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    sessions = crud.get_recent_sessions(db)
    return [{"id": s.id, "created_at": s.created_at.isoformat(), "student_class": s.student_class} for s in sessions]

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    success = crud.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "message": "Session deleted"}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Science Tutor API is running"}
