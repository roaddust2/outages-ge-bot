from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """Simple row keyboard with resize"""
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_col_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """Simple column keyboard with resize"""
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.row(
            KeyboardButton(text=str(item))
        )
    return builder.as_markup(resize_keyboard=True)
