"""
Gradio UI for Capper chatbot.
Sends user messages to FastAPI backend and displays responses.
"""
import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat"

# System prompt for the chatbot
SYSTEM_PROMPT = """
Hi! I'm Capper, your personal Carton Caps assistant.
Ask me a question, and I'll do my best to help you.
If there's anything I can't help you with, I'll direct you to someone who can.
"""

def chat_with_bot(user_id, user_message):
    """
    Sends user message to backend API and returns bot reply.
    """
    payload = {"user_id": user_id, "message": user_message}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        bot_reply = response.json().get("response", "")
    else:
        bot_reply = "Error: " + str(response.status_code)
    return bot_reply

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Carton Caps: AI-Powered Chat Agent")
    user_id_input = gr.Number(value=1, label="User ID")
    chat_interface = gr.Chatbot()
    user_input = gr.Textbox(placeholder="Send a message...", label="Message")
    send_button = gr.Button("Send")

    def respond(user_id, message, chat_history):
        """
        Handles user input, updates chat history with bot response.
        """
        bot_response = chat_with_bot(user_id, message)
        chat_history = chat_history + [(message, bot_response)]
        return "", chat_history

    send_button.click(respond, inputs=[user_id_input, user_input, chat_interface], outputs=[user_input, chat_interface])

if __name__ == "__main__":
    demo.launch()
