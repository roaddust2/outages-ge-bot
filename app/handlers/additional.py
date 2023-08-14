from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.main_kb import make_main_keyboard


router = Router()


@router.message(Command("help"))
@router.message(F.text.lower() == "help")
async def cmd_help(message: Message):
    await message.answer(
        "<b>All commands availible for this bot:</b>\n\n"
        "/help - Display the list of available commands\n"
        "/about - Dispay information about this bot\n"
        "/add_address - Add an address that will be checked for outages. "
        "<i>You can add up to 2 addresses.</i>\n"
        "/list_addresses - Show all added addresses\n"
        "/remove_address - Remove an address",
        reply_markup=make_main_keyboard()
    )


@router.message(Command("about"))
@router.message(F.text.lower() == "about")
async def cmd_about(message: Message):
    await message.answer(
        "<b>About:</b>\n\n"
        "It is an app written in Python with the aiogram framework. "
        "This bot will assist you with information about the latest outages in Georgia (the country).\n\n"
        "<a href=\"https://github.com/roaddust2/outages-ge-bot\">Source code on GitHub</a>",
        disable_web_page_preview=True,
        reply_markup=make_main_keyboard()
    )
