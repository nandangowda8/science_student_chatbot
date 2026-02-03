from sqlalchemy.orm import Session
from . import models

def get_session(db: Session, session_id: int):
    return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()

def create_session(db: Session, user_id: str = "default_user", student_class: str = "General"):
    db_session = models.ChatSession(user_id=user_id, student_class=student_class)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session_messages(db: Session, session_id: int):
    return db.query(models.Message).filter(models.Message.session_id == session_id).all()

def create_message(db: Session, session_id: int, role: str, content: str):
    db_message = models.Message(session_id=session_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_recent_sessions(db: Session, limit: int = 10):
    return db.query(models.ChatSession).order_by(models.ChatSession.created_at.desc()).limit(limit).all()

def delete_session(db: Session, session_id: int):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False
