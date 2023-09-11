from aiogram import Bot
from app.keyboards.main_kb import make_main_keyboard
from app.scrapers.gwp import GWP
from app.scrapers.telasi import Telasi
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.translator import translate
from app.db.functions import (
    select_chats,
    insert_sent_outages,
    delete_sent_outages,
    select_chat_outages
)


# Job for sending outage notifications to chats

async def send_notification(
    bot: Bot,
    tg_chat_id: int,
    emergency: bool,
    type: str,
    date: str,
    en_title: str,
    en_info: str,
    street: str
) -> None:
    """Send message async function"""

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


async def notify(bot: Bot, session: AsyncSession):  # noqa: C901
    """Notify job"""

    # Retrieve actual outages

    gwp_provider = GWP()
    telasi_privider = Telasi()
    outages = []
    gwp_outages = await gwp_provider.collect_outages()
    telasi_outages = await telasi_privider.collect_outages()
    outages.extend(gwp_outages)
    outages.extend(telasi_outages)

    if not outages:
        return None

    # Select chats with their addresses from database

    chats = await select_chats(session)

    for chat in chats:

        outages_to_insert = []

        tg_chat_id = chat.tg_chat_id
        addresses = chat.addresses
        sent_outages = await select_chat_outages(tg_chat_id, session)

        for address in addresses:
            street = address.street

            for outage in outages:

                if outage in sent_outages:
                    continue

                date = outage.get("date")
                type = outage.get("type")
                emergency = outage.get("emergency")
                title = outage.get("title")
                info = outage.get("info")
                en_info = await translate(info)

                if street in info or street in en_info:
                    en_title = await translate(title)
                    await send_notification(bot, tg_chat_id, emergency, type, date, en_title, en_info, street)
                    outages_to_insert.append(outage)

        await insert_sent_outages(tg_chat_id, outages_to_insert, session)


# Job for cleaning db from outdated sent notifications

async def clean_sent_outages(session: AsyncSession):

    await delete_sent_outages(session)
