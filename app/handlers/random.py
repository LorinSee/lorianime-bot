import traceback

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.api import fetch_random_anime
from app.db import add_user, get_user
from app.keyboards import MAIN_KEYBOARD
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
        await send_anime(callback.message, anime)
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()
