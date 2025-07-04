# chat_engine.py
import requests
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Dummy token for testing (in real use, frontend should pass it securely)
DUMMY_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjUwMjkzLCJpYXQiOjE3NTE2NDY5OTMsImp0aSI6ImZjYWYwZTE1MDBiMjQzMTg5ZWIzZGM3MGZjZGM2NGVjIiwidXNlcl9pZCI6MX0.PFVGAlTNPgi47VJ8Mk6MzHQCfF_1B4C7lh6BivpLjuY"

API_BASE = "https://authenti-cation-system.vercel.app"
HEADERS = {"Authorization": f"JWT {DUMMY_TOKEN}"}

# Initialize LangChain model
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

# --- Helper: Get user about info ---
def get_user_about():
    res = requests.get(f"{API_BASE}/api/about/", headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    return {"sport_coach": "", "details": ""}

# --- Helper: Create chat session ---
def create_chat_detail():
    payload = {"topic_summary": "Personalized coaching chat", "participants": []}  # Backend uses token to infer user
    res = requests.post(f"{API_BASE}/api/chat-detail/", json=payload, headers=HEADERS)
    return res.json()["id"] if res.status_code == 201 else None

# --- Helper: Save message to backend ---
def save_message(chat_id, content):
    payload = {"chat": chat_id, "content": content}  # Sender inferred from token
    requests.post(f"{API_BASE}/api/chat-history/", json=payload, headers=HEADERS)

# --- Build prompt ---
def build_prompt(about_info, messages):
    system_msg = (
    f"You are a helpful assistant specialized in {about_info['sport_coach']}.\n"
    f"The user said about themselves: {about_info['details']}.\n"
    "Use this to guide your coaching responses."
)
    chat_template = ChatPromptTemplate.from_messages([
        ("system", system_msg)
    ] + [(m["role"], m["content"]) for m in messages])
    return chat_template | llm | StrOutputParser()

# --- Streamlit UI ---
st.title("🏅 Personalized Sports Chatbot")

if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_chat_detail()

if "messages" not in st.session_state:
    st.session_state.messages = []

about = get_user_about()

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new message
if prompt := st.chat_input("Ask your sports question..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.chat_id, prompt)

    # Generate assistant response
    with st.chat_message("assistant"), st.spinner("Thinking..."):
        response = build_prompt(about, st.session_state.messages).invoke({})
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    save_message(st.session_state.chat_id, response)
    