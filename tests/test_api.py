"""
Test FastAPI chat endpoint for Capper chatbot.
Validates response structure and error handling for missing fields.
"""

import pytest

def test_chat_endpoint(client, sample_user):
    payload = {"user_id": sample_user, "message": "I need help with my referral program."}
    resp = client.post("/chat", json=payload)
    assert resp.status_code == 200
    json_body = resp.json()
    assert "response" in json_body
    assert isinstance(json_body["response"], str)

def test_missing_fields(client):
    resp = client.post("/chat", json={"user_id": 1})
    assert resp.status_code == 422
