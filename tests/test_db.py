"""
Test database functions for Capper chatbot.
Validates user context retrieval, chat history, and saving chat turns.
"""

from db import get_user_context, get_chat_history, save_chat
from datetime import datetime

def test_get_user_context(sample_user):
    ctx = get_user_context(sample_user)
    assert isinstance(ctx, dict)
    assert ctx["user_id"] == sample_user
    assert "name" in ctx and "email" in ctx

def test_chat_history_empty(sample_user):
    history = get_chat_history(sample_user)
    assert history == []

def test_save_and_get_chat(sample_user):
    state = {
        "user_id": sample_user,
        "input": "Hello",
        "response": "Hi there!"
    }
    # insert
    save_chat(state)
    # fetch
    history = get_chat_history(sample_user)
    assert history[-1] == ("Hello", "Hi there!")
