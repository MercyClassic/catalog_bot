from aiogram.fsm.state import State, StatesGroup


class WelcomeMessageState(StatesGroup):
    main = State()
