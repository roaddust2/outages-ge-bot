import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.handlers import (
    start,
    addresses,
    additional,
)
from app.handlers.jobs import notify
from settings import API_TOKEN, TIMEZONE


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.start()
    scheduler.add_job(notify, trigger="interval", minutes=1, kwargs={"bot": bot})
    dp.include_routers(start.router, addresses.router, additional.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
