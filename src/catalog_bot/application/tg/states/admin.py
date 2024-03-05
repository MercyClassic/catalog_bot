from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    start = State()
    create = State()
    delete = State()


class AdminCatalogState(StatesGroup):
    start = State()

    category_detail = State()
    channel_detail = State()

    category_create = State()
    category_change_title = State()
    category_change_description = State()
    category_change_image = State()
    category_delete = State()

    channel_create = State()
    channel_change_title = State()
    channel_change_link = State()
    channel_change_autocommit = State()
    channel_delete = State()

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
