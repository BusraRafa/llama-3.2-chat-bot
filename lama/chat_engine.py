import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import user profiles from separate file
from mock_users import USER_PROFILES

st.set_page_config(page_title="Sports ChatBot", layout="centered")
st.title("🏟️ Personalized Sports ChatBot")

# Select user (simulate login)
selected_user = st.selectbox("Select user", list(USER_PROFILES.keys()), format_func=lambda x: USER_PROFILES[x]["username"])

user_profile = USER_PROFILES[selected_user]
about_text = user_profile["details"]

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {}
if selected_user not in st.session_state.user_memory:
    st.session_state.user_memory[selected_user] = []

model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
output_parser = StrOutputParser()

def generate_response(user_history):
    messages = [
        ("system", f"You are a sports coaching assistant specializing in {user_profile['sport']}. Personalize your replies based on the user's details: {about_text}")
    ] + [(msg["role"], msg["content"]) for msg in user_history]
    
    chain = ChatPromptTemplate.from_messages(messages) | model | output_parser
    return chain.invoke({})

for msg in st.session_state.user_memory[selected_user]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about coaching, tactics, or your favorite team..."):
    st.session_state.user_memory[selected_user].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"), st.spinner("Thinking..."):
        response = generate_response(st.session_state.user_memory[selected_user])
        st.markdown(response)

    st.session_state.user_memory[selected_user].append({"role": "assistant", "content": response})
