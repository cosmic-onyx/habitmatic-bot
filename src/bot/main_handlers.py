from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from main_keyboard import main_kb
from services.AsyncHttpService import AsyncHttpService
from services.RedisService import RedisService


main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    text = """<strong>Habitmatic Bot</strong> - бот помогающий превратить дело в привычку ✨
    
💫 <strong>Бот позволяет</strong>:

    ✏️ Создавать собственные привычки
        
    🗒 Отслеживать свои привычки
        
    📊 Просматривать статистику по каждой привычке
    
А так же получение напоминаний о своих привычках
"""

    await message.answer(
        text,
        reply_markup=main_kb,
        parse_mode='HTML'
    )
    tg_id = message.from_user.id
    is_exists_user = await AsyncHttpService().get_user(
        tg_id
    )
    if not is_exists_user:
        pwd = await AsyncHttpService.create_user(
            message.from_user
        )
        data = await AsyncHttpService().get_jwt_token(
            tg_id, pwd
        )
        await RedisService.set_token(tg_id, data)

        await message.answer(
            f"""Вы были зарегистрированы ботом\n\nВаш пароль от API: {pwd}"""
        )