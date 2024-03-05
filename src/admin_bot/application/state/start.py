from aiogram.fsm.state import State, StatesGroup


class StartState(StatesGroup):
    main = State()

    catalog_bot_list = State()
    catalog_bot_detail = State()

    create_bot_set_title = State()
    create_bot_set_token = State()
