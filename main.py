import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.db import init_db
from app.routes import router

load_dotenv()
TOKEN = str(getenv("BOT_TOKEN"))

dp = Dispatcher()
dp.include_router(router)


async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    print("Start...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
