from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    MEMBER, KICKED
)

from app.db.functions import insert_chat, delete_chat

from app.keyboards.main_kb import make_main_keyboard


router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def blocked(event: ChatMemberUpdated):
    delete_chat(event.chat.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def started(event: ChatMemberUpdated):
    insert_chat(event.chat.id)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Hello <b>{message.from_user.first_name}</b>, this bot can alert you to upcoming outages.\n\n"
        "In order for the bot to be able to send notifications, use <b>\"Add new address\"</b> button "
        "or (/add_address) command.",
        reply_markup=make_main_keyboard()
    )
    insert_chat(message.chat.id)


@router.message(Command("cancel"))
@router.message(F.text.lower() == "cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Process has been canceled.\n\n",
        reply_markup=make_main_keyboard()
    )
