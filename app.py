"""
FastAPI application for Capper chatbot.
Defines API endpoints for chat and history retrieval.
Initializes workflow and database.
"""

from fastapi import FastAPI, Request
from graph import build_graph
from db import init_db
from pydantic import BaseModel

app = FastAPI()
workflow = build_graph()
init_db()

class ChatRequest(BaseModel):
    user_id: int
    message: str 


@app.post("/chat")
async def chat(request: ChatRequest):
    # Receives chat request, invokes workflow, returns response
    state = {"user_id": request.user_id, "input": request.message}
    final_state = workflow.invoke(state)
    return {"response": final_state.get("response", "")}

@app.get("/history/{user_id}")
def history(user_id: int):
    # Returns chat history for a user
    from db import get_chat_history
    return {"history": get_chat_history(user_id)}