from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.basic_kbs import make_row_keyboard
from app.keyboards.main_kb import make_main_keyboard

from app.db.db import (
    AddressesNumExceeded,
    AddressAlreadyExists,
    is_address_num_exceeded,
    insert_address,
    select_addresses,
)


AVAILIBLE_CITIES = ["Tbilisi",]


router = Router()


class AddAddress(StatesGroup):
    choosing_city = State()
    entering_street = State()


@router.message(Command("add_address"))
@router.message(F.text.lower() == "add new address")
async def cmd_add_address(message: Message, state: FSMContext):
    try:
        is_address_num_exceeded(message.chat.id)
        await message.answer(
            "<b>1. Choose city:</b>\n\n"
            "<i>You can add up to 2 addresses.</i>",
            reply_markup=make_row_keyboard(AVAILIBLE_CITIES)
        )
        await state.set_state(AddAddress.choosing_city)
    except AddressesNumExceeded:
        await message.answer(
            "Number of addresses exceeded. To add new address remove at least one. "
            "Use <b>\"Remove address\"</b> button.",
            reply_markup=make_main_keyboard()
        )


@router.message(AddAddress.choosing_city, F.text.in_(AVAILIBLE_CITIES))
async def city_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_city=message.text)
    await message.answer(
        "<b>2. Enter a street:</b>\n\n"
        "<i>You can text in both English or Georgian.</i>"
        ,
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
    try:
        insert_address(message.chat.id, {"city": user_data['chosen_city'], "street": message.text})
        await message.answer(
            f"Your address <b>{message.text}, {user_data['chosen_city']}</b> is saved!\n"
            "Now this bot will notify you as soon as possible if the outage appears, stay tuned!",
            reply_markup=make_main_keyboard()
        )
        await state.clear()
    except AddressAlreadyExists:
        await message.answer(
            f"Address <b>{message.text}, {user_data['chosen_city']}</b> already exists.",
            reply_markup=make_main_keyboard()
        )
        await state.clear()


@router.message(Command("list_addresses"))
@router.message(F.text.lower() == "my addresses")
async def cmd_list_addresses(message: Message):
    addresses = select_addresses(message.chat.id)
    if len(addresses) < 1:
        await message.answer(
            "You do not have any saved addresses.\n"
            "To add address use <b>\"Add new address\"</b> button "
            "or (/add_address) command.",
            reply_markup=make_main_keyboard()
        )
    else:
        result = ''
        for i, address in enumerate(addresses):
            result += f"<b>{i+1}.</b> {address}\n"
        await message.answer(
            "<b>Your saved addresses:</b>\n\n"
            f"{result.strip()}",
            reply_markup=make_main_keyboard()
        )
