from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram import types


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        """*EN:* Hi, please enter a street so the bot can alert you to upcoming outages\\.
The street name can be entered in both English and Georgian

*KA:* გამარჯობა, გთხოვთ, შეიყვანოთ ქუჩა, რათა ბოტმა შეგატყობინოთ მომავალი გათიშვის შესახებ\\.
ქუჩის სახელი შეიძლება შეიყვანოთ როგორც ინგლისურად, ასევე ქართულად""",
        parse_mode="MarkdownV2"
    )


@router.message(F.text)
async def handle_street_name(message: types.Message):
    await message.answer(
        f"""*EN:* Your street now is *{message.text}*\\.
Now, if a message about outage is published, the bot will immediately notify you, stay tuned\\!

*KA:* ახლა შენი ქუჩაა *{message.text}*\\.
ახლა, თუ გამოქვეყნდება შეტყობინება გათიშვის შესახებ, ბოტი მაშინვე შეგატყობინებთ, თვალი ადევნეთ\\!""",
        parse_mode="MarkdownV2"
    )
