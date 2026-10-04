from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards import build_main_keyboard

from app.api import fetch_anime_by_id
from app.db import add_favorite, is_favorite, remove_favorite

router = Router()


@router.callback_query(F.data.startswith("fav:"))
async def toggle_favorite(callback: CallbackQuery):
    parts = callback.data.split(":")
    action = parts[1]  # add / remove
    source = parts[2]  # random / search / genre
    anime_id = int(parts[3])
    user_id = callback.from_user.id

    anime = await fetch_anime_by_id(anime_id)
    if anime is None:
        await callback.answer("Не удалось загрузить", show_alert=True)
        return

    title = anime.get("russian") or anime.get("name") or "Без названия"

    if action == "add":
        await add_favorite(user_id, anime_id, title)
        await callback.answer("Добавлено в избранное ⭐")
    else:
        await remove_favorite(user_id, anime_id)
        await callback.answer("Убрано из избранного ❌")

    fav_now = await is_favorite(user_id, anime_id)

    new_keyboard = build_main_keyboard(
        anime_id,
        source=source,
        is_fav=fav_now,
    )
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
