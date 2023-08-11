from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.basic_kbs import make_row_keyboard
from app.keyboards.main_kb import make_main_keyboard

from app.db.db import (
    is_address_num_exceeded,
    insert_address,
)


AVAILIBLE_CITIES = ["Tbilisi",]


router = Router()


class AddAddress(StatesGroup):
    choosing_city = State()
    entering_street = State()


@router.message(Command("add_address"))
@router.message(F.text.lower() == "add new address")
async def cmd_add_address(message: Message, state: FSMContext):
    if is_address_num_exceeded(message.chat.id):
        await message.answer(
            "Number of addresses exceeded. To add new address remove at least one. "
            "Use <b>\"Remove address\"</b> button.",
            reply_markup=make_main_keyboard()
        )
    else:
        await message.answer(
            "You can add up to 2 addresses.\n\n"
            "1. Choose city:",
            reply_markup=make_row_keyboard(AVAILIBLE_CITIES)
        )
        await state.set_state(AddAddress.choosing_city)


@router.message(AddAddress.choosing_city, F.text.in_(AVAILIBLE_CITIES))
async def city_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_city=message.text)
    await message.answer(
        "2. Enter a street (you can text in both English or Georgian):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddAddress.entering_street)


@router.message(AddAddress.choosing_city)
async def city_chosen_incorrectly(message: Message):
    await message.answer(
        "The city you entered is incorrect, please choose from the above:",
        reply_markup=make_row_keyboard(AVAILIBLE_CITIES)
    )


@router.message(AddAddress.entering_street)
async def street_entered(message: Message, state: FSMContext):
    user_data = await state.get_data()
    insert_address(message.chat.id, {"city": user_data['chosen_city'], "street": message.text})
    await message.answer(
        f"Your address <b>{message.text}, {user_data['chosen_city']}</b> is saved!",
        reply_markup=make_main_keyboard()
    )
    await state.clear()
