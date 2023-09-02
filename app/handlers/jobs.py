from aiogram import Bot
from app.keyboards.main_kb import make_main_keyboard
import app.scrapers.gwp as GWP
import app.scrapers.telasi as TELASI
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.functions import (
    OutageAlreadySent,
    insert_sent_outage,
    select_addresses,
    delete_sent_outages
)

from settings import translator


# Job for sending outage notifications to chats

OUTAGE_MESSAGE = "{0}{1} <b>{2} {3}</b>\n\n{4}"

EMOJIS_MAP = {
    ":no_entry:": "\u26D4\uFE0F",
    ":bangbang:": "\u203C\uFE0F",
    ":droplet:": "\U0001F4A7",
    ":bulb:": "\U0001F4A1"
}


def format_info(info: str, street: str) -> str:
    """Highlight street with bold style"""

    if street in info:
        return info.replace(street, f"<b>{street}</b>")
    else:
        return info


async def notify(bot: Bot, session: AsyncSession):  # noqa: C901

    outages = []

    gwp_outages = await GWP.collect_outages()
    telasi_outages = await TELASI.collect_outages()

    outages.extend(gwp_outages)
    outages.extend(telasi_outages)

    addresses = await select_addresses(session)

    if not outages:
        pass

    for outage in outages:
        type = outage.get("type")
        emergency = outage.get("emergency")
        info = outage.get("info")
        en_info = translator.translate(info)

        for address in addresses:
            tg_chat_id = address.chat.tg_chat_id
            street = address.street
            date = outage.get("date").strftime("%Y-%m-%d")
            if street in info or street in en_info:
                title = outage.get("title")
                en_title = translator.translate(title)
                try:
                    await insert_sent_outage(tg_chat_id, outage, session)
                    await bot.send_message(
                        chat_id=tg_chat_id,
                        text=OUTAGE_MESSAGE.format(
                            EMOJIS_MAP[":bangbang:"] if emergency else EMOJIS_MAP[":no_entry:"],
                            EMOJIS_MAP[":droplet:"] if type == "water" else EMOJIS_MAP[":bulb:"],
                            date,
                            en_title,
                            format_info(en_info, street)
                        ),
                        reply_markup=make_main_keyboard()
                    )
                except OutageAlreadySent:
                    pass


# Job for cleaning db from outdated sent notifications

async def clean_sent_outages(session: AsyncSession):

    await delete_sent_outages(session)
