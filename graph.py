"""
Defines the workflow graph for Capper chatbot using LangGraph.
Each node loads context, generates response, or saves chat.
"""
from typing import TypedDict, List, Tuple
from langgraph.graph import StateGraph, END
from db import get_user_context, get_chat_history, save_chat
from embeddings import load_pdf_context
from llm import get_llm_response

class ChatState(TypedDict):
    user_id: str
    input: str
    user_context: dict
    pdf_context: str
    chat_history: List[Tuple[str, str]]
    response: str

# Node: Loads user context from DB
def load_user_context_node(state: ChatState) -> ChatState:
    state["user_context"] = get_user_context(state["user_id"])
    return state

# Node: Loads relevant PDF context
def load_pdf_context_node(state: ChatState) -> ChatState:
    state["pdf_context"] = load_pdf_context(state["input"])
    return state

# Node: Loads chat history for user
def load_chat_history_node(state: ChatState) -> ChatState:
    state["chat_history"] = get_chat_history(state["user_id"])
    return state

# Node: Generates LLM response
def generate_response_node(state: ChatState) -> ChatState:
    state["response"] = get_llm_response(state)
    return state

# Node: Saves chat turn to DB
def save_chat_node(state: ChatState) -> ChatState:
    save_chat(state)
    return state

# Build workflow graph
def build_graph():
    workflow = StateGraph(ChatState)
    workflow.add_node("load_user_context", load_user_context_node)
    workflow.add_node("load_pdf_context", load_pdf_context_node)
    workflow.add_node("load_chat_history", load_chat_history_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("save_chat", save_chat_node)

    workflow.set_entry_point("load_user_context")
    workflow.add_edge("load_user_context", "load_pdf_context")
    workflow.add_edge("load_pdf_context", "load_chat_history")
    workflow.add_edge("load_chat_history", "generate_response")
    workflow.add_edge("generate_response", "save_chat")
    workflow.add_edge("save_chat", END)
    
    return workflow.compile()