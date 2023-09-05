import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from app.keyboards.basic_kbs import make_row_keyboard, make_col_keyboard
from app.keyboards.main_kb import make_main_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.functions import (
    AddressesNumExceeded,
    AddressAlreadyExists,
    is_address_num_exceeded,
    insert_address,
    select_full_addresses,
    delete_address,
)


router = Router()


# Add address handlers

AVAILIBLE_CITIES = ["Tbilisi",]


class AddAddress(StatesGroup):
    choosing_city = State()
    entering_street = State()


@router.message(Command("add_address"))
@router.message(F.text.lower() == "add new address")
async def cmd_add_address(message: Message, state: FSMContext, session: AsyncSession):
    try:
        await is_address_num_exceeded(message.chat.id, session)
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
        "<i>You can text in both English or Georgian.</i>",
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
async def street_entered(message: Message, state: FSMContext, session: AsyncSession):

    user_data = await state.get_data()
    try:
        await insert_address(
            message.chat.id,
            {"city": user_data['chosen_city'], "street": message.text},
            session,
        )
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


# Remove address handlers

class RemoveAddress(StatesGroup):
    choosing_address = State()


@router.message(Command("remove_address"))
@router.message(F.text.lower() == "remove address")
async def cmd_remove_address(message: Message, state: FSMContext, session: AsyncSession):
    addresses = await select_full_addresses(message.chat.id, session)
    if not addresses:
        await message.answer(
            "You do not have any saved addresses.\n"
            "To add address use <b>\"Add new address\"</b> button "
            "or (/add_address) command.",
            reply_markup=make_main_keyboard()
        )
    else:
        await message.answer(
            "<b>Choose address that you want to remove from the above:</b>",
            reply_markup=make_col_keyboard(addresses)
        )
        await state.set_state(RemoveAddress.choosing_address)


@router.message(RemoveAddress.choosing_address)
async def address_chosen(message: Message, state: FSMContext, session: AsyncSession):
    addresses = await select_full_addresses(message.chat.id, session)
    if message.text in addresses:
        await delete_address(message.chat.id, message.text, session)
        await message.answer(
            "Address has been successfully deleted!",
            reply_markup=make_main_keyboard()
        )
        await state.clear()
    else:
        logging.info(f"{message.text}, {addresses}")
        await message.answer(
            "The address you entered is incorrect, please choose from the above:",
            reply_markup=make_col_keyboard(addresses)
        )


# Display list of addresses for specific chat handler

@router.message(Command("list_addresses"))
@router.message(F.text.lower() == "my addresses")
async def cmd_list_addresses(message: Message, session: AsyncSession):
    addresses = await select_full_addresses(message.chat.id, session)
    if not addresses:
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
