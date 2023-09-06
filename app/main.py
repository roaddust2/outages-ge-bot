import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.handlers import (
    start,
    addresses,
    additional,
)
from app.handlers.jobs import clean_sent_outages, notify
from app.middlewares.db import DbSessionMiddleware
from settings import API_TOKEN, DATABASE_URL_ASYNC, TIMEZONE, jobstores
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


logging.basicConfig(level=logging.INFO)


async def main():

    # Init SQLAlchemy async engine, make AsyncSession
    engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Init bot
    bot = Bot(token=API_TOKEN, parse_mode="HTML")

    # Init dispatcher
    dp = Dispatcher()

    # Bind middlewares to dispatcher
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    # Bind routers to dispatcher
    dp.include_router(start.router)
    dp.include_router(addresses.router)
    dp.include_router(additional.router)

    # Init scheduler and add jobs
    scheduler = AsyncIOScheduler(timezone=TIMEZONE, jobstores=jobstores)
    notify_trigger = CronTrigger.from_crontab("0,30 8-17 * * *")  # Every 30 minutes from 08:00 - 18:00
    clean_trigger = CronTrigger.from_crontab("0 0 * * fri")  # Every Friday at 00:00 Midnight
    scheduler.start()
    scheduler.add_job(
        notify,
        jobstore='default',
        trigger=notify_trigger,
        kwargs={"bot": bot, "session": sessionmaker}
    )
    scheduler.add_job(
        clean_sent_outages,
        jobstore='default',
        trigger=clean_trigger,
        kwargs={"session": sessionmaker}
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
