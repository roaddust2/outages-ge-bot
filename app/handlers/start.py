from aiogram import F, Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ChatMemberUpdated
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


@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer(
        f"""*EN:* Hello *{message.from_user.first_name}*, this bot can alert you to upcoming outages\\.
The next step is to add an address\\.

*KA:* გამარჯობა *{message.from_user.first_name}*, ამ ბოტს შეუძლია გაფრთხილება მოახლოებული გათიშვის შესახებ\\.
შემდეგი ნაბიჯი არის მისამართის დამატება\\.""",
        parse_mode="MarkdownV2"
    )
    insert_chat(message.chat.id)
