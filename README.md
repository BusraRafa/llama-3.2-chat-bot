# 🦙 LLaMA 3.2 Chatbot (Streamlit + LangChain)

An interactive chatbot UI powered by **LLaMA 3.2**, built using **Streamlit** and **LangChain**. This project runs a local LLaMA model via **Ollama**, enabling fast and private chat interactions directly in your browser.

## 🚀 Features

- Chat UI built with **Streamlit**
- Uses **LangChain** for prompt formatting and parsing
- Local inference using **Ollama** (`llama3.2:3b`)
- Session-based conversation history
- Ready for Codespaces or local Docker/Devcontainer environments

---

## 📦 Requirements

- Python 3.11+
- [Ollama](https://ollama.com/) running locally with `llama3.2:3b` model installed

## Python Dependencies

### 1. Clone the Repository
```bash
git clone https://github.com/BusraRafa/llama-3.2-chat-bot.git
cd llama-3.2-chat-bot
```
### 2. Create a Virtual Environment (optional but recommended)
```bash
python -m venv myenv
myenv\Scripts\activate.bat
```
**Install dependencies in the project folder with:**
   ```bash
   pip install -r requirements.txt
```
**Contents of requirements.txt:**
```nginx
streamlit
langchain
langchain_openai
langchain_core
langchain_ollama
langchain_community
python-dotenv
```
### ⚙️ Dev Container Support

This repo includes a `.devcontainer/devcontainer.json` for seamless development in GitHub Codespaces or locally using VS Code Dev Containers.

**Features:**

- Preconfigured Python 3.11 image  
- Auto-installs packages from `requirements.txt`  
- Automatically starts the chatbot on port `8501`

---

## 🧠 How It Works

The chatbot interface is defined in `chatbot.py`:

- Loads the `llama3.2:3b` model via LangChain's `ChatOllama`
- Maintains user and assistant messages in Streamlit session state
- Displays chat messages in a conversational format

---

## 🛠️ Running the App

Make sure [Ollama](https://ollama.com/) is running and the model is pulled:

```bash
ollama pull llama3.2:3b
```
**Then run the chatbot:**
```bash
streamlit run lama/chatbot.py
```
The app will be available at: http://localhost:8501
