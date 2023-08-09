from aiogram import F, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatMemberUpdated, ReplyKeyboardRemove
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    MEMBER, KICKED
)

from app.db.db import insert_chat, delete_chat


router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def blocked(event: ChatMemberUpdated):
    delete_chat(event.chat.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def started(event: ChatMemberUpdated):
    insert_chat(event.chat.id)


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"<b>EN:</b> Hello <b>{message.from_user.first_name}</b>, this bot can alert you to upcoming outages."
        "The next step is to add an address using command (/add_address) \n\n"
        f"<b>KA:</b> გამარჯობა <b>{message.from_user.first_name}</b>,"
        " ამ ბოტს შეუძლია გაფრთხილება მოახლოებული გათიშვის შესახებ."
        "შემდეგი ნაბიჯი არის მისამართის დამატება ბრძანების (/add_address) გამოყენებით.",
        reply_markup=ReplyKeyboardRemove()
    )
    insert_chat(message.chat.id)


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="cancel", ignore_case=True))
@router.message(Text(text="გააუქმოს"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>EN:</b> process is canceled.\n\n"
        "<b>KA:</b> პროცესი გაუქმებულია.\n\n",
        reply_markup=ReplyKeyboardRemove()
    )
