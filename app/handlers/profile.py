from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.db import get_user, get_user_stats, update_bio, update_display_name
from app.keyboards import (
    build_cancel_keyboard_simple,
    build_profile_keyboard,
    build_settings_keyboard,
)

router = Router()


class SettingsStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_bio = State()


def build_profile_text(user, stats):
    username = user.get("username") or "не указан"
    created = (user.get("created_at") or "")[:10]
    display_name = user.get("display_name") or "не задано"
    bio = user.get("bio") or "не задано"

    return (
        f"<b>Профиль</b>\n\n"
        f"<b>ID:</b> <code>{user['user_id']}</code>\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>Имя:</b> {display_name}\n"
        f"<b>О себе:</b> {bio}\n"
        f"<b>Дата регистрации:</b> {created}\n\n"
        f"<b>Аниме в списках:</b> {stats['anime_count']}\n"
        f"<b>В избранном:</b> {stats['fav_count']}"
    )


@router.message(F.text == "Профиль")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("Профиль не найден. Напиши /start")
        return

    stats = await get_user_stats(message.from_user.id)
    text = build_profile_text(user, stats)
    await message.answer(text, parse_mode="HTML", reply_markup=build_profile_keyboard())


@router.callback_query(F.data == "profile:settings")
async def open_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Настройки профиля</b>\n\nЧто хочешь изменить?",
        parse_mode="HTML",
        reply_markup=build_settings_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:back")
async def settings_back(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    stats = await get_user_stats(callback.from_user.id)
    await callback.message.edit_text(
        build_profile_text(user, stats),
        parse_mode="HTML",
        reply_markup=build_profile_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:name")
async def settings_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_for_name)
    await callback.message.edit_text(
        "Введи новое имя (до 32 символов):",
        reply_markup=build_cancel_keyboard_simple(),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:bio")
async def settings_bio(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.waiting_for_bio)
    await callback.message.edit_text(
        "Введи описание (до 200 символов):",
        reply_markup=build_cancel_keyboard_simple(),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:cancel")
async def settings_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "<b>Настройки профиля</b>\n\nЧто хочешь изменить?",
        parse_mode="HTML",
        reply_markup=build_settings_keyboard(),
    )
    await callback.answer()


@router.message(SettingsStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if not name:
        await message.answer("Имя не может быть пустым. Попробуй ещё раз.")
        return
    if len(name) > 32:
        await message.answer("Слишком длинное имя. Максимум 32 символа.")
        return

    await update_display_name(message.from_user.id, name)
    await state.clear()

    user = await get_user(message.from_user.id)
    stats = await get_user_stats(message.from_user.id)
    await message.answer(
        f"Имя сохранено: <b>{name}</b>",
        parse_mode="HTML",
    )
    await message.answer(
        build_profile_text(user, stats),
        parse_mode="HTML",
        reply_markup=build_profile_keyboard(),
    )


@router.message(SettingsStates.waiting_for_bio)
async def process_bio(message: Message, state: FSMContext):
    bio = (message.text or "").strip()
    if not bio:
        await message.answer("Описание не может быть пустым. Попробуй ещё раз.")
        return
    if len(bio) > 200:
        await message.answer("Слишком длинное описание. Максимум 200 символов.")
        return

    await update_bio(message.from_user.id, bio)
    await state.clear()

    user = await get_user(message.from_user.id)
    stats = await get_user_stats(message.from_user.id)
    await message.answer(
        "Описание сохранено.",
    )
    await message.answer(
        build_profile_text(user, stats),
        parse_mode="HTML",
        reply_markup=build_profile_keyboard(),
    )
