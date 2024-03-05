from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_i_am_not_a_bot_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.button(
        text='Я не бот',
        callback_data='verification',
    )
    markup.adjust(1)
    markup = markup.as_markup()
    return markup


def get_admin_menu_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    markup.button(text='Админ меню')
    markup.adjust(1)
    markup = markup.as_markup(resize_keyboard=True)
    return markup
