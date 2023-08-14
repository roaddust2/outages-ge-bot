import asyncio
import logging
from aiogram import Bot, Dispatcher
from settings import API_TOKEN

from app.handlers import (
    start,
    addresses,
    additional,
)


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(start.router, addresses.router, additional.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
