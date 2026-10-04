import traceback

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
)

from app.api import (
    fetch_anime_by_id,
    fetch_genres,
    fetch_random_anime,
    fetch_random_by_genre,
)
from app.db import add_user, get_user
from app.keyboards import MAIN_KEYBOARD, GenrePagination, build_genres_keyboard
from app.sender import send_anime

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    existing = await get_user(message.from_user.id)
    await add_user(message.from_user.id, message.from_user.username)

    if existing is None:
        greeting = "Привет! Я аниме бот.\n\nВыбери действие:"
    else:
        greeting = "С возвращением!\n\nВыбери действие:"

    await message.answer(greeting, reply_markup=MAIN_KEYBOARD)


@router.message(F.text == "Случайное аниме")
@router.message(Command("random"))
async def random_anime(message: Message):
    try:
        anime = await fetch_random_anime()
        if anime is None:
            await message.answer("Сервер не доступен или вернул пустой ответ...")
            return
        await send_anime(message, anime)
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()


@router.callback_query(F.data == "more_anime")
async def more_anime_callback(callback: CallbackQuery):
    try:
        anime = await fetch_random_anime()
        if anime is None:
            await callback.answer("Сервер не доступен, попробуй позже")
            return
        await send_anime(callback.message, anime, user_id=callback.from_user.id)
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()


@router.message(F.text == "Рандом по жанру")
async def random_by_genre_start(message: Message):
    genres = await fetch_genres()
    if not genres:
        await message.answer("Не удалось загрузить список жанров")
        return

    await message.answer(
        "Выбери жанр:", reply_markup=build_genres_keyboard(genres, page=0)
    )


@router.callback_query(GenrePagination.filter())
async def genre_pagination(callback: CallbackQuery, callback_data: GenrePagination):
    genres = await fetch_genres()
    await callback.message.edit_reply_markup(
        reply_markup=build_genres_keyboard(genres, page=callback_data.page)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("genre_pick"))
async def genre_pick(callback: CallbackQuery):
    genre_id = int(callback.data.split(":")[1])
    print("GENRE_ID:", genre_id)

    anime = await fetch_random_by_genre(genre_id)
    print("ANIME:", anime)

    if anime is None:
        await callback.answer("Не удалось найти аниме по этому жанру", show_alert=True)
        return

    anime = await fetch_anime_by_id(anime.get("id"))

    await send_anime(
        callback.message,
        anime,
        source="genre",
        genre_id=genre_id,
        user_id=callback.from_user.id,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("more_genre"))
async def more_genre_callback(callback: CallbackQuery):
    try:
        genre_id = int(callback.data.split(":")[1])

        anime = await fetch_random_by_genre(genre_id)
        if anime is None:
            await callback.answer("Не нашлось аниме по этому жанру", show_alert=True)
            return

        anime = await fetch_anime_by_id(anime.get("id"))

        await send_anime(
            callback.message,
            anime,
            source="genre",
            genre_id=genre_id,
            user_id=callback.from_user.id,
        )
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()
