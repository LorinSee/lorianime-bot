import traceback

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from handlers.api import fetch_anime_by_id, fetch_anime_search
from handlers.keyboards import build_cancel_keyboard, build_search_button
from handlers.sender import send_anime

router = Router()


class SearchStates(StatesGroup):
    waiting_for_query = State()


@router.message(F.text == "Поиск")
async def search_start(message: Message, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_query)
    await message.answer(
        "Введите название аниме:", reply_markup=build_cancel_keyboard()
    )


@router.message(SearchStates.waiting_for_query)
async def search_process(message: Message, state: FSMContext):
    query = message.text
    await state.clear()

    if not query or len(query) < 3:
        await message.answer("Слишком короткий запрос, введи хотя бы 3 символа")
        return

    results = await fetch_anime_search(query)
    if not results:
        await message.answer(f"По запросу «{query}» ничего не найдено")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[build_search_button(a)] for a in results]
    )
    await message.answer(
        f"<b>Найдено {len(results)}:</b>", parse_mode="HTML", reply_markup=keyboard
    )


@router.callback_query(F.data == "cancel_search")
async def cancel_search_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Поиск отменён.")
    await callback.answer()


@router.callback_query(F.data.startswith("search:"))
async def search_result_callback(callback: CallbackQuery):
    try:
        anime_id = int(callback.data.split(":")[1])
        anime = await fetch_anime_by_id(anime_id)
        if anime is None:
            await callback.answer("Не удалось загрузить", show_alert=True)
            return

        chat_id = callback.message.chat.id
        try:
            await callback.message.delete()
        except Exception as e:
            print("Не удалось удалить сообщение:", e)

        await send_anime(callback.bot, anime, from_search=True, chat_id=chat_id)
        await callback.answer()
    except Exception as e:
        print("ОШИБКА:", type(e).__name__, e)
        traceback.print_exc()
