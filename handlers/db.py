from datetime import datetime

import aiosqlite

DB_PATH = "lorianimebot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
                username TEXT
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def add_user(user_id: int, username: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
            (user_id, username, datetime.now().isoformat()),
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_is = ?", (user_id)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
