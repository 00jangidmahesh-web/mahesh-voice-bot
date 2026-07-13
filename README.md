---
title: Mahesh Voice Bot
emoji: 🎙️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🎙️ Digital Twin Voice Agent — Mahesh Kumar Jangid

A voice-to-voice AI agent that answers interview and background questions as me,
grounded in a RAG knowledge base and built as a LangGraph agent.

## How It Works

```
Mic Input (browser, RMS silence detection)
        │
        ▼
  Groq/OpenAI Whisper (STT)            ← hallucination filtering on near-silence
        │
        ▼
  LangGraph ReAct Agent
        │
        ├─ search_mahesh_profile tool ──► Chroma vectorstore (RAG over profile)
        │
        ▼
  gpt-4o-mini generates grounded, first-person response
        │
        ▼
  OpenAI TTS → MP3 → auto-plays in browser (barge-in enabled)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Agent framework | LangGraph (`create_react_agent`) |
| RAG | LangChain + Chroma + OpenAI embeddings (`text-embedding-3-small`) |
| LLM | OpenAI `gpt-4o-mini` |
| Speech-to-Text | OpenAI Whisper (`whisper-1`) |
| Text-to-Speech | OpenAI TTS (`gpt-4o-mini-tts`) |
| Frontend | HTML5 + CSS3 + Vanilla JS (Web Audio API, MediaRecorder) |
| Deployment | Hugging Face Spaces (Docker) |

## Key Engineering Features

- **RAG-grounded persona** — answers are retrieved from `app/data/mahesh_profile.txt`
  via a Chroma vectorstore, not hardcoded in the prompt. Add a new project or
  achievement by editing that file; the vectorstore rebuilds automatically on
  next startup (it compares file vs. DB modified time).
- **Barge-in** — clicking the orb while the bot is speaking instantly stops
  playback and starts a new recording.
- **RMS silence detection** — the browser computes RMS volume via the Web
  Audio API `AnalyserNode` and auto-stops recording after ~1.1s of
  sustained silence, so you don't have to click stop manually.
- **Whisper hallucination filtering** — short/near-silent clips are dropped
  before hitting the LLM, and common Whisper silence-hallucinations
  ("thank you for watching", etc.) are filtered out server-side.
- **Extensible for MCP tools** — `app/agent.py` builds the LangGraph agent's
  tool list explicitly; adding an MCP-backed tool (e.g. live web search)
  later is a matter of appending to that list, no architecture change needed.

## Project Structure

```text
mahesh-voice-bot/
├── app/
│   ├── main.py           # FastAPI routes (/chat/voice, /chat/text, /chat/reset)
│   ├── agent.py           # LangGraph ReAct agent + system prompt
│   ├── rag.py              # Chroma vectorstore build/load
│   ├── asr_handler.py     # OpenAI Whisper STT + hallucination filter
│   ├── tts_handler.py     # OpenAI TTS
│   ├── data/
│   │   └── mahesh_profile.txt   # Source knowledge base for RAG
│   └── static/
│       └── index.html    # Orb UI, RMS silence detection, barge-in
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Run Locally

```bash
git clone <your-repo-url> mahesh-voice-bot
cd mahesh-voice-bot

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# edit .env and add your OPENAI_API_KEY

cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000/static/index.html` in Chrome or Edge.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Used for Whisper, gpt-4o-mini, embeddings, and TTS |
| `OPENAI_CHAT_MODEL` | No | Default `gpt-4o-mini` |
| `OPENAI_TTS_MODEL` | No | Default `gpt-4o-mini-tts` |
| `OPENAI_TTS_VOICE` | No | Default `onyx` |
| `OPENAI_EMBEDDING_MODEL` | No | Default `text-embedding-3-small` |

## Deploy to Hugging Face Spaces

1. Create a new Space → SDK: **Docker**.
2. Push this repo to the Space's git remote.
3. In Space **Settings → Repository secrets**, add `OPENAI_API_KEY`.
4. The Space builds from the `Dockerfile` and serves on port `7860`
   automatically — no extra config needed.

## Updating the Persona

Everything the agent knows about Mahesh lives in one place:
`app/data/mahesh_profile.txt`. To add a new project, achievement, or answer,
just edit that file — the RAG index rebuilds itself the next time the app
starts (it checks whether the file is newer than the persisted vectorstore).

## Security & Privacy

- API key is read from environment variables only, never exposed to the frontend.
- Audio is processed in-memory and not persisted to disk.
- Conversation history is kept in-memory per server process and resets on
  restart (or via `POST /chat/reset`).
