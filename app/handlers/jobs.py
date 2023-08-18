from aiogram import Bot

from app.keyboards.main_kb import make_main_keyboard
from app.scrapers.gwp import scrap_notifications, parse_notifications_info
from app.db.functions import (
    OutageAlreadySent,
    insert_sent_outage,
    select_addresses
)


OUTAGE_MESSAGE = "{0}{1} <b>{2}</b>\n\n{3}"

EMOJIS_MAP = {
    ":no_entry:": "\u26D4\uFE0F",
    ":bangbang:": "\u203C\uFE0F",
    ":droplet:": "\U0001F4A7",
    ":bulb:": "\U0001F4A1"
}


async def notify(bot: Bot, tg_chat_id: str):

    addresses = select_addresses(tg_chat_id)
    outages = parse_notifications_info(scrap_notifications())

    for outage in outages:
        type = outage.get("type")
        emergency = outage.get("emergency")
        geo_info = outage.get("geo_info")
        en_info = outage.get("en_info")
        for address in addresses:
            street = address.street
            if street in geo_info or street in en_info:
                try:
                    insert_sent_outage(tg_chat_id, outage)
                    await bot.send_message(
                        chat_id=tg_chat_id,
                        text=OUTAGE_MESSAGE.format(
                            EMOJIS_MAP[":bangbang:"] if emergency else EMOJIS_MAP[":no_entry:"],
                            EMOJIS_MAP[":droplet:"] if type == "water" else EMOJIS_MAP[":bulb:"],
                            outage.get("en_title"),
                            en_info
                        ),
                        reply_markup=make_main_keyboard()
                    )
                except OutageAlreadySent:
                    pass
