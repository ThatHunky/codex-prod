"""Simple user-specific conversation history stored in SQLite."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import aiosqlite


DB_PATH = Path(__file__).with_name("history.db")

_INIT_SQL = (
    "CREATE TABLE IF NOT EXISTS messages ("
    "user_id INTEGER NOT NULL,"
    "role TEXT NOT NULL,"
    "text TEXT NOT NULL,"
    "ts DATETIME DEFAULT CURRENT_TIMESTAMP"
    ")"
)


async def init_db() -> None:
    """Create database and tables if they do not exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(_INIT_SQL)
        await db.commit()


async def add_message(user_id: int, role: str, text: str) -> None:
    """Persist a single message for the given user."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO messages (user_id, role, text) VALUES (?, ?, ?)",
            (user_id, role, text),
        )
        await db.commit()


async def get_history(user_id: int, limit: int = 20) -> list[tuple[str, str]]:
    """Return the most recent conversation history for a user."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT role, text FROM messages WHERE user_id = ? ORDER BY ts ASC LIMIT ?",
            (user_id, limit),
        ) as cursor:
            rows: Iterable[tuple[str, str]] = await cursor.fetchall()
    return list(rows)


async def clear_history(user_id: int) -> None:
    """Remove stored conversation for the user."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        await db.commit()
