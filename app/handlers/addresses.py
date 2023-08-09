from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.row import make_row_keyboard

# TODO: Create a db functions to insert addresses

AVAILIBLE_CITIES = {
    "Tbilisi | თბილისი": "Tbilisi",
}


router = Router()


class AddAddress(StatesGroup):
    choosing_city = State()
    entering_street = State()


@router.message(Command("add_address"))
async def cmd_add_address(message: Message, state: FSMContext):
    await message.answer(
        "<b>EN:</b> Choose city\n\n"
        "<b>KA:</b> აირჩიეთ ქალაქი:",
        reply_markup=make_row_keyboard(AVAILIBLE_CITIES.keys())
    )
    await state.set_state(AddAddress.choosing_city)


@router.message(AddAddress.choosing_city, F.text.in_(AVAILIBLE_CITIES.keys()))
async def city_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_city=AVAILIBLE_CITIES.get(message.text))
    await message.answer(
        "<b>EN:</b> Thank you, now enter a street (you can text in both English or Georgian):\n\n"
        "<b>KA:</b> გმადლობთ, ახლა შეიყვანეთ ქუჩა (შეგიძლიათ ტექსტი ინგლისურად ან ქართულად):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddAddress.entering_street)


@router.message(AddAddress.choosing_city)
async def city_chosen_incorrectly(message: Message):
    await message.answer(
        "<b>EN:</b> The city you entered is incorrect, please choose from the above:\n\n"
        "<b>KA:</b> თქვენ მიერ შეყვანილი ქალაქი არასწორია, გთხოვთ, აირჩიოთ ზემოთ ჩამოთვლილიდან:",
        reply_markup=make_row_keyboard(AVAILIBLE_CITIES.keys())
    )


@router.message(AddAddress.entering_street)
async def street_entered(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        f"<b>EN:</b> Your address <b>{message.text}, {user_data['chosen_city']}</b> is saved!\n\n"
        f"<b>KA:</b> თქვენი მისამართი <b>{message.text}, {user_data['chosen_city']}</b> შენახულია!",
    )
    await state.clear()
