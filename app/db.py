from datetime import datetime

import aiosqlite

DB_PATH = "lorianimebot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                anime_id INTEGER,
                title TEXT,
                PRIMARY KEY (user_id, anime_id)
            )
        """)
        for col in ("display_name", "bio"):
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
            except Exception:
                pass
        await db.commit()


async def add_user(user_id: int, username: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
            (user_id, username, datetime.now().isoformat()),
        )
        await db.commit()


async def add_favorite(user_id: int, anime_id: int, title: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO favorites (user_id, anime_id, title) VALUES (?, ?, ?)",
            (user_id, anime_id, title),
        )
        await db.commit()


async def remove_favorite(user_id: int, anime_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND anime_id = ?",
            (user_id, anime_id),
        )
        await db.commit()


async def is_favorite(user_id: int, anime_id: int) -> bool:
    async with (
        aiosqlite.connect(DB_PATH) as db,
        db.execute(
            "SELECT 1 FROM favorites WHERE user_id = ? AND anime_id = ?",
            (user_id, anime_id),
        ) as cursor,
    ):
        return await cursor.fetchone() is not None


async def get_favorites(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT anime_id, title FROM favorites WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_user_stats(user_id: int):
    async with (
        aiosqlite.connect(DB_PATH) as db,
        db.execute(
            "SELECT COUNT(*) FROM favorites WHERE user_id = ?", (user_id,)
        ) as cursor,
    ):
        row = await cursor.fetchone()
        fav_count = row[0] if row else 0
    return {"anime_count": 0, "fav_count": fav_count}


async def update_display_name(user_id: int, name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET display_name = ? WHERE user_id = ?", (name, user_id)
        )
        await db.commit()


async def update_bio(user_id: int, bio: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET bio = ? WHERE user_id = ?", (bio, user_id))
        await db.commit()
