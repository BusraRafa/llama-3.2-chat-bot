import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

st.title("llama-3.2 Chat-bot")

model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

# Function to generate response using full history
def generate_response(messages):
    chat_template = ChatPromptTemplate.from_messages(messages)
    chain = chat_template | model | StrOutputParser()
    return chain.invoke({})

# Initialize chat history (no system prompt)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history in UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response using full chat history
    with st.chat_message("assistant"), st.spinner("Generating response..."):
        response = generate_response(st.session_state.messages)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
