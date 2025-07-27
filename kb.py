from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_kb(
    *,
    btns: dict,
    sizes: tuple[int]):

    kb = InlineKeyboardBuilder()
    for text, query in btns.items():
        kb.add(InlineKeyboardButton(text=text,callback_data=query))

    return kb.adjust(*sizes).as_markup()
