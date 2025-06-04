import os
from typing import Any, Iterable

import httpx


# Endpoint for the Gemini API

# Use the Gemini 2.0 Flash model
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"


async def generate_response(
    prompt: str, history: Iterable[tuple[str, str]] | None = None
) -> str:
    """Call Gemini API to generate a response including prior history."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    params = {"key": api_key}
    contents = [
        {"role": role, "parts": [{"text": text}]} for role, text in (history or [])
    ]
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    payload: dict[str, Any] = {"contents": contents}

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(GEMINI_API_URL, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text")
            )
            if not text:
                raise ValueError("Empty response from Gemini")
            return text
        except Exception as e:  # broad exception to simplify example
            # In production, log exception details
            return f"Error contacting Gemini API: {e}"
