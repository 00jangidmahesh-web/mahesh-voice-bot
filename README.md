# 🎙️ Mahesh Voice Bot

An AI-powered voice and text conversational agent that acts as my digital twin, answering interview, career, project, and background questions in natural language.

The assistant is powered by Retrieval-Augmented Generation (RAG), LangGraph, OpenAI models, and a modern voice-enabled web interface.

---

## 🌐 Live Demo

**Website:** https://mahesh-voice-bot.onrender.com

---

# Features

- 🎤 Voice-to-Voice Conversation
- 💬 Text Chat Support
- 🧠 RAG-powered Knowledge Base
- 🤖 LangGraph ReAct Agent
- 🔍 Semantic Search using ChromaDB
- 🗣️ OpenAI Whisper Speech-to-Text
- 🔊 OpenAI Text-to-Speech
- ⚡ Barge-in Support (Interrupt while speaking)
- 🎯 Automatic Silence Detection
- 📱 Responsive Web UI

---

# Architecture

```
                 User

        🎤 Voice / 💬 Text
                 │
                 ▼
         FastAPI Backend
                 │
     ┌───────────┴───────────┐
     │                       │
 Speech-to-Text          Text Input
(OpenAI Whisper)             │
     │                       │
     └───────────┬───────────┘
                 ▼
        LangGraph ReAct Agent
                 │
                 ▼
      Chroma Vector Database
          (RAG Search)
                 │
                 ▼
          GPT-4o Mini LLM
                 │
                 ▼
       Response Generation
                 │
      ┌──────────┴─────────┐
      │                    │
  Text Response       OpenAI TTS
      │                    │
      └──────────┬─────────┘
                 ▼
          Browser UI
```

---

# Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Language | Python |
| AI Agent | LangGraph |
| LLM | GPT-4o Mini |
| RAG | LangChain + ChromaDB |
| Embeddings | text-embedding-3-small |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | OpenAI TTS |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |
| Version Control | Git & GitHub |

---

# Key Engineering Features

### Voice Interaction

- Browser microphone recording
- Automatic silence detection
- No manual stop required
- Continuous listening until user finishes speaking

---

### Barge-in Support

Users can interrupt the assistant while it is speaking and immediately ask another question.

---

### Retrieval-Augmented Generation (RAG)

Instead of hardcoding responses, the assistant retrieves relevant information from a personal knowledge base using semantic search.

Knowledge Source:

```
data/mahesh_profile.txt
```

---

### Semantic Search

Uses:

- LangChain
- ChromaDB
- OpenAI Embeddings

to retrieve only the most relevant context before generating answers.

---

### Text + Voice Modes

Users can either

- Talk using microphone
- Type questions manually

Both use the same LangGraph backend.

---

### Modern UI

- Animated Voice Orb
- Conversation History
- Quick Question Buttons
- Voice Playback
- Responsive Layout

---

# Project Structure

```text
mahesh-voice-bot/

│
├── main.py
├── agent.py
├── rag.py
├── asr_handler.py
├── tts_handler.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── data/
│     └── mahesh_profile.txt
│
└── static/
      └── index.html
```

---

# Running Locally

```bash
git clone https://github.com/00jangidmahesh-web/mahesh-voice-bot.git

cd mahesh-voice-bot

python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```
OPENAI_API_KEY=your_api_key
```

Run

```bash
uvicorn main:app --reload
```

Open

```
http://localhost:8000
```

---

# Environment Variables

| Variable | Description |
|-----------|-------------|
| OPENAI_API_KEY | OpenAI API Key |
| OPENAI_CHAT_MODEL | GPT model (default: gpt-4o-mini) |
| OPENAI_EMBEDDING_MODEL | Embedding model |
| OPENAI_TTS_MODEL | TTS model |
| OPENAI_TTS_VOICE | Voice name |

---

# Deployment

The application is deployed on **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Add the following environment variable in Render:

```
OPENAI_API_KEY
```

---

# Updating the Knowledge Base

All interview answers, projects, achievements, skills, and personal information are stored in:

```
data/mahesh_profile.txt
```

Simply edit this file and restart the application.

The assistant automatically uses the updated information through the RAG pipeline.

---

# Future Improvements

- Memory across conversations
- Resume Upload
- LinkedIn Integration
- GitHub Project Search
- Live Web Search
- MCP Tool Support
- Multi-language Conversations
- Streaming Responses
- Authentication

---

# License

This project is intended for educational and portfolio purposes.

---

# Author

**Mahesh Kumar Jangid**

Master's in Mathematics and Computing  
Indian Institute of Technology (ISM) Dhanbad

LinkedIn

https://www.linkedin.com/in/mahesh-kumar-jangid-22b375306/

GitHub

https://github.com/00jangidmahesh-web

Email

00jangidmahesh@gmail.com
