"""
Text-to-speech using OpenAI's TTS API. Returns raw MP3 bytes so the
FastAPI route can stream them straight back to the browser without
touching disk.
"""

import os

from openai import OpenAI

client = OpenAI()

TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "onyx")


def text_to_speech(text: str) -> bytes:
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="mp3",
    )
    return response.content
