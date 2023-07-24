import asyncio
import logging
from aiogram import Bot, Dispatcher
from settings import API_TOKEN

from app.handlers import greeting


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_routers(greeting.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
