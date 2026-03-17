# app.py
import gradio as gr
import requests
import time
import datetime

# The URL of our new FastAPI backend
API_URL = "http://localhost:8000/chat"

def chat_response(message, history):

    greeting_msg = "Global Intelligence Liaison (GIL) active. Secure connection established. I am ready to provide SITREPs on the Russia-Ukraine or Middle East sectors using my verified sources intelligence network. What is your request?"

    if message.lower() in ["exit", "quit", "bye"]:
        yield "Goodbye! Stay secure! (Refresh to restart)"
        return
    # 1. Start searching immediately
    yield "⏳ Searching trusted networks, analyzing intelligence, and synthesizing data... Please wait."

    try:
        history_str = ""
        for item in history:

            if isinstance(item, dict):
                role = item.get('role', 'user')
                content = item.get('content', '')
            else:
                role = 'user' if item[0] else 'assistant'
                content = item[0] if item[0] else item[1]
            
            if isinstance(content, str) and content.startswith("⏳ Searching"): 
                continue
            
            history_str += f"{role.capitalize()}: {content}\n"

        # 2. Data Requesting from API
        response = requests.post(
            API_URL, 
            json={"message": message, "history": history_str},
            timeout=300
        )
        response.raise_for_status()
        final_answer = response.json().get("response", "Error: No response from API.")

    except Exception as e:
        yield f"⚠️ Error: {str(e)}"
        return

    # 3. Streaming response letter by letter
    output = ""
    for char in final_answer:
        output += char
        time.sleep(0.005) 
        yield output

# ===========================
# GRADIO INTERFACE SETUP
# ===========================
greeting_msg = "Global Intelligence Liaison (GIL) active. Secure connection established. I am ready to provide SITREPs on the Russia-Ukraine or Middle East sectors using my verified sources intelligence network. What is your request?"

initial_chatbot = gr.Chatbot(value=[{"role": "assistant", "content": greeting_msg}], height=600)

demo = gr.ChatInterface(
    fn=chat_response,
    chatbot=initial_chatbot,
    title="🛡️ GIL: Multi-Agent Intelligence Swarm",
    description="Strategic Geopolitical Intelligence Desk. Powered by a 6-Agent Swarm, Ephemeral RAG, and Semantic Caching.",
    examples=[
        "SITREP: Current status of the Donbas front.",
        "Summarize the intelligence from this URL: https://www.understandingwar.org"
    ]
)

if __name__ == "__main__":
    # Gradio runs on port 7860 by default 
    demo.launch(share=True, debug=True, theme="soft")

