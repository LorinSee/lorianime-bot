from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Случайное аниме")],
        [KeyboardButton(text="Поиск")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


def build_main_keyboard(anime_id, from_search=False):
    buttons = []
    if from_search:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Описание", callback_data=f"desc:search:{anime_id}"
                )
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Описание", callback_data=f"desc:random:{anime_id}"
                )
            ]
        )
        buttons.append(
            [InlineKeyboardButton(text="Ещё аниме", callback_data="more_anime")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_back_keyboard(anime_id, source):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад", callback_data=f"back:{source}:{anime_id}"
                )
            ]
        ]
    )


def build_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить", callback_data="cancel_search")]
        ]
    )


def build_search_button(anime):
    label = anime.get("russian") or anime.get("name", "Без названия")
    year = (anime.get("aired_on") or "")[:4]
    if year:
        label = f"{label} ({year})"
    return InlineKeyboardButton(
        text=label[:60], callback_data=f"search:{anime.get('id')}"
    )
