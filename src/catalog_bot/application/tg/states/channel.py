from aiogram.fsm.state import State, StatesGroup


class JoinChannelState(StatesGroup):
    start = State()
