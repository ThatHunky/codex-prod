import base64
import os
from typing import Any, Iterable

import httpx


# Endpoints for the Gemini API

# Use the Gemini 2.5 Flash Preview model for text responses
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# Image generation model
GEMINI_IMAGE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"


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


async def generate_image(prompt: str) -> bytes:
    """Generate an image from a text prompt using Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    params = {"key": api_key}
    payload: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(GEMINI_IMAGE_URL, params=params, json=payload)
            response.raise_for_status()
        except Exception as e:  # broad exception to simplify example
            raise RuntimeError(f"Error contacting Gemini API: {e}") from e

        data = response.json()
        b64 = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("inlineData", {})
            .get("data")
        )
        if not b64:
            raise RuntimeError("Empty image response from Gemini")
        return base64.b64decode(b64)
