import traceback

from aiogram import F, Router
from aiogram.types import CallbackQuery, LinkPreviewOptions

from app.api import fetch_anime_by_id
from app.keyboards import build_back_keyboard, build_main_keyboard
from app.utils import build_caption, clean_description

router = Router()


@router.callback_query(F.data.startswith("desc:"))
async def send_description_callback(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")
        source = parts[1]
        anime_id = int(parts[2])
        anime = await fetch_anime_by_id(anime_id)
        if anime is None:
            await callback.answer("Не удалось загрузить", show_alert=True)
            return

        description = anime.get("description") or "Нет описания"
        description = clean_description(description)
        if len(description) > 900:
            description = description[:900] + "..."

        text = f"<b>Описание:</b>\n\n{description}"
        keyboard = build_back_keyboard(anime_id, source)

        if callback.message.photo:
            await callback.message.edit_caption(
                caption=text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await callback.message.edit_text(
                text=text,
                parse_mode="HTML",
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()


@router.callback_query(F.data.startswith("back:"))
async def back_callback(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")
        source = parts[1]
        anime_id = int(parts[2])
        anime = await fetch_anime_by_id(anime_id)
        if anime is None:
            await callback.answer("Не удалось загрузить", show_alert=True)
            return

        from_search = source == "search"
        caption = build_caption(anime)
        keyboard = build_main_keyboard(anime_id, from_search=from_search)

        if callback.message.photo:
            await callback.message.edit_caption(
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await callback.message.edit_text(
                text=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()
