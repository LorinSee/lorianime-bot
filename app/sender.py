from aiogram.types import LinkPreviewOptions

from app.db import is_favorite
from app.keyboards import build_main_keyboard
from app.utils import build_caption, get_image_url


async def send_anime(
    target, anime, source="random", chat_id=None, genre_id=None, user_id=None
):
    caption = build_caption(anime)
    image_url = get_image_url(anime)
    anime_id = anime.get("id")

    if user_id is not None:
        fav = await is_favorite(user_id, anime_id)
    else:
        fav = False

    keyboard = build_main_keyboard(
        anime_id, source=source, genre_id=genre_id, is_fav=fav
    )

    print("ОТПРАВЛЯЮ:", anime.get("russian") or anime.get("name"), anime.get("score"))

    if chat_id is not None:
        if image_url:
            await target.send_photo(
                chat_id=chat_id,
                photo=image_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await target.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    else:
        if image_url:
            await target.answer_photo(
                photo=image_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        else:
            await target.answer(
                caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
