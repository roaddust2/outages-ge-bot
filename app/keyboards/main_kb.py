from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_main_keyboard() -> ReplyKeyboardMarkup:
    """Main keyboard with most usable menu buttons"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Add new address")
    )
    builder.row(
        KeyboardButton(text="My addresses"),
        KeyboardButton(text="Remove address")
    )
    # builder.row(
    #     KeyboardButton(text="Help"),
    #     KeyboardButton(text="About")
    # )
    return builder.as_markup(resize_keyboard=True)
