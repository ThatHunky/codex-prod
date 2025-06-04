import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pathlib import Path

import pytest

from bot import memory


@pytest.mark.asyncio
async def test_memory_round_trip(tmp_path: Path):
    memory.DB_PATH = tmp_path / "test.db"
    await memory.init_db()
    await memory.add_message(1, "user", "hi")
    await memory.add_message(1, "model", "ok")
    history = await memory.get_history(1)
    assert history == [("user", "hi"), ("model", "ok")]
    await memory.clear_history(1)
    assert await memory.get_history(1) == []
