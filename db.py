from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
DB_PATH = "data/Carton_Caps_Data.sqlite"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    return SessionLocal()

def get_user_context(user_id):
    session = get_db_session()
    user_row = (
        session
        .execute(text("SELECT * FROM Users WHERE id = :user_id"), {"user_id": user_id})
        .mappings()
        .fetchone()
    )
    if not user_row:
        session.close()
        return {}
    school_row = (
        session
        .execute(text("SELECT name FROM Schools WHERE id = :school_id"),
                 {"school_id": user_row["school_id"]})
        .mappings()
        .fetchone()
    )
    session.close()
    return {
        "user_id":     user_row["id"],
        "name":        user_row["name"],
        "email":       user_row["email"],
        "school":      school_row["name"] if school_row else None,
        "created_at":  user_row["created_at"],
    }

def get_chat_history(user_id):
    session = get_db_session()
    results = session.execute(
        text("SELECT message, sender FROM Conversation_History WHERE user_id = :uid ORDER BY timestamp"),
        {"uid": user_id}
    ).mappings().fetchall()
    session.close()
    history = []
    temp = None
    for row in results:
        if row["sender"] == "user":
            temp = row["message"]
        elif row["sender"] == "bot" and temp:
            history.append((temp, row["message"]))
            temp = None
    return history

def save_chat(state):
    session = get_db_session()
    now = datetime.utcnow().isoformat()
    session.execute(
        text("INSERT INTO Conversation_History (user_id, message, sender, timestamp) VALUES (:uid, :msg, 'user', :ts)"),
        {"uid": state["user_id"], "msg": state["input"], "ts": now}
    )
    session.execute(
        text("INSERT INTO Conversation_History (user_id, message, sender, timestamp) VALUES (:uid, :msg, 'bot', :ts)"),
        {"uid": state["user_id"], "msg": state["response"], "ts": now}
    )
    session.commit()
    session.close()