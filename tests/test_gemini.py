import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import os
import pytest

from bot import gemini


class FakeResponse:
    def __init__(self, data: dict[str, str]):
        self._data = data

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict[str, str]:
        return self._data


class FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, *args, **kwargs):
        return FakeResponse({"candidates": [{"content": {"parts": [{"text": "hi"}]}}]})


@pytest.mark.asyncio
async def test_generate_response(monkeypatch):
    monkeypatch.setattr(gemini.httpx, "AsyncClient", FakeAsyncClient)
    os.environ["GEMINI_API_KEY"] = "x"
    result = await gemini.generate_response("hello")
    assert result == "hi"
