from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Поиск")],
        [
            KeyboardButton(text="Случайное аниме"),
            KeyboardButton(text="Рандом по жанру"),
        ],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


class GenrePagination(CallbackData, prefix="genre_page"):
    page: int


class SearchPagination(CallbackData, prefix="search_page"):
    query: str
    page: int


def build_main_keyboard(anime_id, source="random", genre_id=None):
    buttons = []

    if source == "search":
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Описание", callback_data=f"desc:search:{anime_id}"
                )
            ]
        )
    elif source == "genre":
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Описание", callback_data=f"desc:genre:{anime_id}"
                )
            ]
        )

        if genre_id is not None:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Ещё аниме", callback_data=f"more_genre:{genre_id}"
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


def build_profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Настройки", callback_data="profile:settings")],
        ]
    )


def build_settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить имя", callback_data="settings:name")],
            [
                InlineKeyboardButton(
                    text="Изменить описание", callback_data="settings:bio"
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="settings:back")],
        ]
    )


def build_cancel_keyboard_simple():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить", callback_data="settings:cancel")]
        ]
    )


def build_genres_keyboard(genres: list, page: int, per_page=8):
    builder = InlineKeyboardBuilder()

    start = page * per_page
    end = start + per_page
    chunk = genres[start:end]

    for g in chunk:
        builder.button(
            text=g.get("russian") or g.get("name", "Unknown"),
            callback_data=f"genre_pick:{g['id']}",
        )

    builder.adjust(2)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️", callback_data=GenrePagination(page=page - 1).pack()
            )
        )

    total_pages = (len(genres) + per_page - 1) // per_page
    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}", callback_data="genre_page:ignore"
        )
    )

    if end < len(genres):
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️", callback_data=GenrePagination(page=page + 1).pack()
            )
        )

    if nav_buttons:
        builder.row(*nav_buttons)

    return builder.as_markup()


def build_search_results_keyboard(results, query, page, per_page=8):
    builder = InlineKeyboardBuilder()

    start = page * per_page
    end = start + per_page
    chunk = results[start:end]

    for a in chunk:
        builder.row(build_search_button(a))

    total_pages = (len(results) + per_page - 1) // per_page

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=SearchPagination(query=query, page=page - 1).pack(),
            )
        )
    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}", callback_data="search_page:ignore"
        )
    )
    if end < len(results):
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=SearchPagination(query=query, page=page + 1).pack(),
            )
        )

    if nav_buttons:
        builder.row(*nav_buttons)

    return builder.as_markup()
