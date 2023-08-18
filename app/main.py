import asyncio
import logging
from aiogram import Bot, Dispatcher
from settings import API_TOKEN
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.handlers.jobs as JOB

from app.handlers import (
    start,
    addresses,
    additional,
)


logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler(timezone="Asia/Tbilisi")


async def main():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(start.router, addresses.router, additional.router)
    scheduler.add_job(
        JOB.notify,
        trigger='cron',
        hour=datetime.now().hour,
        minute=datetime.now().minute + 1,
        start_date=datetime.now(),
        kwargs={"bot": bot}
    )
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
