from aiogram.fsm.state import State, StatesGroup


class NewsletterState(StatesGroup):
    start = State()
    default = State()
    periodic_list = State()

    set_periodic_title = State()
    set_periodic_entity = State()

    periodic_detail = State()

    periodic_change_date = State()

    approve = State()
    periodic_create_approve = State()
