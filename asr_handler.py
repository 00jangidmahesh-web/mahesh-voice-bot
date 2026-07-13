"""
Speech-to-text using OpenAI's Whisper API, with filtering for Whisper's
known tendency to hallucinate stock phrases when given near-silent audio
(short recordings, background noise only, etc.).
"""

import io

from openai import OpenAI

client = OpenAI()

# Phrases Whisper commonly emits when fed silence or pure noise. Matched
# case-insensitively against the *whole* transcript after stripping
# punctuation, so a real sentence that merely contains one of these words
# is not falsely dropped.
_HALLUCINATION_PHRASES = {
    "thank you for watching",
    "thanks for watching",
    "thank you for watching!",
    "please subscribe",
    "subscribe to my channel",
    "like and subscribe",
    "thanks for listening",
    "you",
    ".",
    "bye",
    "bye bye",
    "goodbye",
    "amara.org",
    "www.amara.org",
}

_MIN_AUDIO_BYTES = 4000  # ~ under half a second at typical webm/opus bitrates


def _looks_like_hallucination(text: str) -> bool:
    cleaned = text.strip().strip(".").strip().lower()
    return cleaned in _HALLUCINATION_PHRASES or len(cleaned) == 0


def speech_to_text(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    if len(audio_bytes) < _MIN_AUDIO_BYTES:
        return ""

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename  # OpenAI SDK reads the extension from this

    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    except Exception as e:
        return f"__ERROR__: {str(e)}"

    text = (transcription.text or "").strip()

    if _looks_like_hallucination(text):
        return ""

    return text
