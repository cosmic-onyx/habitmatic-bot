import asyncio
from aiogram import Bot
from aiogram import Dispatcher

from main_handlers import main_router
from habits.handlers import habit_router
from settings.config import env_settings


bot = Bot(token=env_settings.TELEGRAM_BOT_TOKEN)


async def main():
    dp = Dispatcher(bot=bot)

    dp.include_router(main_router)
    dp.include_router(habit_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())