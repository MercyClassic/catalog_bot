from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    start = State()
    text = State()
    media = State()

    get_welcome_messages = State()
    welcome_message_create_set_title = State()
    welcome_message_create_set_media = State()
    welcome_message_choose_button_or_create = State()
    welcome_message_create_set_button_type = State()
    welcome_message_create_set_buttons = State()
    welcome_message_create = State()
    welcome_message_detail = State()
    welcome_message_delete = State()

    welcome_message_change = State()
    welcome_message_change_text = State()
    welcome_message_change_media = State()
