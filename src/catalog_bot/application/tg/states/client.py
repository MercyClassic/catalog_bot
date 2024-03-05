from aiogram.fsm.state import State, StatesGroup


class ClientCatalogState(StatesGroup):
    start = State()
    category_detail = State()
