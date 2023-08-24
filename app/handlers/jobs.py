from aiogram import Bot
from app.keyboards.main_kb import make_main_keyboard
import app.scrapers.gwp as GWP
import app.scrapers.telasi as TELASI

from app.db.functions import (
    OutageAlreadySent,
    insert_sent_outage,
    select_addresses,
    delete_sent_outages
)


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


async def notify(bot: Bot):  # noqa: C901

    outages = []

    gwp_outages = GWP.collect_outages()
    telasi_outages = TELASI.collect_outages()

    outages.extend(gwp_outages)
    outages.extend(telasi_outages)

    addresses = select_addresses()

    if not outages:
        pass

    for outage in outages:
        type = outage.get("type")
        emergency = outage.get("emergency")
        geo_info = outage.get("geo_info")
        en_info = outage.get("en_info")

        for address in addresses:
            tg_chat_id = address.chat.tg_chat_id
            street = address.street
            if street in geo_info or street in en_info:
                try:
                    insert_sent_outage(tg_chat_id, outage)
                    await bot.send_message(
                        chat_id=tg_chat_id,
                        text=OUTAGE_MESSAGE.format(
                            EMOJIS_MAP[":bangbang:"] if emergency else EMOJIS_MAP[":no_entry:"],
                            EMOJIS_MAP[":droplet:"] if type == "water" else EMOJIS_MAP[":bulb:"],
                            outage.get("date"),
                            outage.get("en_title"),
                            format_info(en_info)
                        ),
                        reply_markup=make_main_keyboard()
                    )
                except OutageAlreadySent:
                    pass


# Job for cleaning db from outdated sent notifications

async def clean_sent_outages():

    await delete_sent_outages()
