import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import os
import httpx
from types import SimpleNamespace
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


class FakeImageClient:
    class Aio:
        class Models:
            async def generate_images(self, *, model: str, prompt: str):
                img = SimpleNamespace(image_bytes=b"img")
                return SimpleNamespace(generated_images=[SimpleNamespace(image=img)])

        def __init__(self) -> None:
            self.models = self.Models()

    def __init__(self, *args, **kwargs) -> None:
        self.aio = self.Aio()


class FakeImageClientError(FakeImageClient):
    class Aio(FakeImageClient.Aio):
        class Models(FakeImageClient.Aio.Models):
            async def generate_images(self, *, model: str, prompt: str):
                raise httpx.HTTPStatusError("Bad Request", request=None, response=None)


@pytest.mark.asyncio
async def test_generate_response(monkeypatch):
    monkeypatch.setattr(gemini.httpx, "AsyncClient", FakeAsyncClient)
    os.environ["GEMINI_API_KEY"] = "x"
    result = await gemini.generate_response("hello")
    assert result == "hi"


@pytest.mark.asyncio
async def test_generate_image(monkeypatch):
    monkeypatch.setattr(gemini.genai, "Client", FakeImageClient)
    os.environ["GEMINI_API_KEY"] = "x"
    result = await gemini.generate_image("cat")
    assert result == b"img"


@pytest.mark.asyncio
async def test_generate_image_error(monkeypatch):
    monkeypatch.setattr(gemini.genai, "Client", FakeImageClientError)
    os.environ["GEMINI_API_KEY"] = "x"
    with pytest.raises(RuntimeError):
        await gemini.generate_image("cat")
