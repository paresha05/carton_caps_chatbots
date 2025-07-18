****Capper – Carton Caps AI Chatbot Prototype****

Welcome to Capper, the AI‑powered conversational assistant proof‑of‑concept for Carton Caps. 
Capper helps users get personalized product recommendations and understand the referral program via natural, in-app chat.

---

Python 3.10 or 3.11
 [Ollama CLI](https://ollama.com/) installed and running
 `snowflake-arctic-embed` and `llama3` models pulled:

  ```bash
  ollama pull snowflake-arctic-embed
  ollama pull llama3
  ```

Clone & Install

```bash
git clone https://github.com/pareshau/capper-chatbot.git
cd capper-chatbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Data

Place the provided assets under `data/`:
data/
```
├── Carton_Caps_Data.sqlite
├── “Carton Caps Referral FAQs.pdf”
└── “Carton Caps Referral Program Rules.pdf”
```
Run the code

1. Start Ollama LLM

   ```bash
   ollama run llama3
   ```
2. Launch FastAPI

   ```bash
   uvicorn app:app --reload
   ```
3. Test via CURL

   ```bash
   curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"user_id":1,"message":"How do referrals work?"}'
   ```

Project Directory Structure
```
├── app.py            # FastAPI entrypoint
├── graph.py          # LangGraph workflow definition
├── db.py             # SQLAlchemy data access (SQLite)
├── embeddings.py     # PDF ingestion & Chroma vector store
├── llm.py            # ChatOllama integration & prompt formatting
├── prompt.py         # Reusable PromptTemplate for “Capper”
├── requirements.txt  # Dependency list
└── tests/            # Pytest suite (unit & integration)
```
API Endpoints
```
POST /chat
Request: `{ user_id: int, conversation_id?: str, message: str }`
Response: `{ conversation_id: str, turn: int, response: str, suggested_actions?: [] }`
GET /history/{user_id}
Fetch past chat turns for UI replay.
```
LangGraph orchestrates:
  1. Load user context & history
  2. Retrieve PDF snippets via Chroma
  3. Format “Capper” system + history prompt
  4. Call ChatOllama LLM
  5. Persist conversation turns

PromptTemplate - centralizes system intro, user info, PDF context, history, and user query.
Chroma vectorstore for fast semantic search over FAQs & rules.
SQLite backend for demo; easily swap to Postgres/MySQL for production.


Testing
```bash
pytest --maxfail=1 -q
```

Covers:

 DB layer (context & history)
 Embeddings retrieval
 Prompt formatting & LLM stubbing
 Workflow execution
 FastAPI endpoint validation

