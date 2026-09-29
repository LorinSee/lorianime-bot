from aiogram import F, Router
from aiogram.types import Message

from app.db import get_user, get_user_stats


router = Router()


@router.message(F.text == "Профиль")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("Профиль не найден. Напишите /start")
        return
    
    stats = await get_user_stats(message.from_user.id)

    username = user.get("username") or "не указан"
    created = user.get("created_at", "")[:10]

    text = (
        f"<b>Профиль</b>\n\n"
        f"<b>ID:</b> <code>{user['user_id']}</code>\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>Дата регистрации:</b> {created}\n\n"
        f"<b>Аниме в списках:</b> {stats['anime_count']}\n"
        f"<b>В избранном:</b> {stats['fav_count']}"
    )
    await message.answer(text, parse_mode="HTML")