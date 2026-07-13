import base64
import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse  # <-- FileResponse yahan add kiya
from fastapi.staticfiles import StaticFiles

from asr_handler import speech_to_text
from tts_handler import text_to_speech
from agent import get_agent_response, reset_history

app = FastAPI(title="Mahesh Voice Bot")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")


# --- Updated Root Endpoint ---
@app.get("/")
async def root():
    # static/index.html ka absolute path use karna safer hota hai
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)
# ------------------------------


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat/text")
async def chat_text(message: str = Form(...)):
    """Text-in, voice+text-out — used for the preset question buttons."""
    if not message.strip():
        return JSONResponse({"error": "Empty message"}, status_code=400)

    reply_text = get_agent_response(message.strip())
    audio_bytes = text_to_speech(reply_text)
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "transcript": message.strip(),
        "response_text": reply_text,
        "audio_base64": audio_b64,
    }


@app.post("/chat/voice")
async def chat_voice(audio: UploadFile = File(...)):
    """Voice-in, voice+text-out — the main mic pipeline."""
    audio_bytes = await audio.read()

    transcript = speech_to_text(audio_bytes, filename=audio.filename or "audio.webm")

    if transcript.startswith("__ERROR__"):
        return JSONResponse({"error": transcript}, status_code=500)

    if not transcript:
        return JSONResponse({"transcript": "", "response_text": "", "audio_base64": ""})

    reply_text = get_agent_response(transcript)
    audio_out = text_to_speech(reply_text)
    audio_b64 = base64.b64encode(audio_out).decode("utf-8")

    return {
        "transcript": transcript,
        "response_text": reply_text,
        "audio_base64": audio_b64,
    }


@app.post("/chat/reset")
async def chat_reset():
    reset_history()
    return {"status": "reset"}
