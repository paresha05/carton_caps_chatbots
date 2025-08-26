"""
LLM integration for Capper chatbot.
Formats prompt and queries Ollama LLM for responses.
Handles different output types from LangChain.
"""

from langchain_ollama import ChatOllama
from typer import prompt
from prompt import format_referral_prompt
from langchain.schema import AIMessage

llm = ChatOllama(model="llama3", temperature=0, max_tokens=512, top_k=3)


def get_llm_response(state: dict) -> str:
    """
    Formats prompt using user, PDF, and chat context, then queries LLM.
    Returns response as string.
    """
    prompt = format_referral_prompt(
        user_ctx=state["user_context"],
        pdf_ctx=state["pdf_context"],
        chat_history=state["chat_history"],
        user_input=state["input"],
    )   
    result = llm.invoke(prompt)
    # Unwrap any messaging object into a string
    if isinstance(result, AIMessage):
        return result.content
    # If it’s a LangChain ChatResult
    if hasattr(result, "generations"):
        # take the first generation’s message
        gen = result.generations[0]
        return getattr(gen, "message", gen).content if hasattr(gen, "message") else gen.text

    # Fallback
    return str(result)

