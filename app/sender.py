from aiogram.types import LinkPreviewOptions

from app.keyboards import build_main_keyboard
from app.utils import build_caption, get_image_url


async def send_anime(target, anime, from_search=False, chat_id=None):
    caption = build_caption(anime)
    image_url = get_image_url(anime)
    keyboard = build_main_keyboard(anime.get("id"), from_search=from_search)

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
