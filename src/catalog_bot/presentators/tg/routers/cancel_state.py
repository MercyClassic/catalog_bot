from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

router = Router()


@router.message(State('*'), Command('cancel'))
async def cancel_state(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    current_state = await state.get_state()
    if not current_state:
        return

    await state.clear()
    await bot.send_message(
        message.from_user.id,
        'Отменено',
    )
