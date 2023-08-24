import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.handlers import (
    start,
    addresses,
    additional,
)
from app.handlers.jobs import clean_sent_outages, notify
from settings import API_TOKEN, TIMEZONE, jobstores


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE, jobstores=jobstores)
    scheduler.start()
    scheduler.add_job(notify, trigger="interval", minutes=15, kwargs={"bot": bot})
    scheduler.add_job(clean_sent_outages, jobstore='sqlalchemy', trigger="cron", day_of_week="sun", hour=0, minute=0)
    dp.include_routers(start.router, addresses.router, additional.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
