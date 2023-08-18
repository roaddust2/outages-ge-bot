from aiogram import Bot

from app.keyboards.main_kb import make_main_keyboard

from app.db.functions import OutageAlreadySent, insert_sent_outage
from app.scheduler.tasks import collect_addresses_with_outages


async def notify(bot: Bot):

    outage_message = "{0} <b>{1}</b>\n\n{2}"
    mapping = {"water": "💧", "electricity": "⚡️"}

    addresses_outages = collect_addresses_with_outages("GWP")
    print(addresses_outages)
    for _ in addresses_outages:
        for address, outage in _.items():
            try:
                insert_sent_outage(address.chat.tg_chat_id, outage)
                print(outage)
                await bot.send_message(
                    chat_id=address.chat.tg_chat_id,
                    text=outage_message.format(
                        mapping[outage.get("type")],
                        outage.get("en_title"),
                        outage.get("en_info")
                    ),
                    reply_markup=make_main_keyboard()
                )
            except OutageAlreadySent:
                pass
