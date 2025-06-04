import os
from typing import Any

import httpx


# Endpoint for the Gemini API

# Use the Gemini Flash 2.5 preview model
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-preview-05-20:generateContent"



async def generate_response(prompt: str) -> str:
    """Call Gemini API to generate a response for the given prompt."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    params = {"key": api_key}
    # fmt: off
    payload: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    # fmt: on

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
