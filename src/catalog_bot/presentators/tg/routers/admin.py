from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from catalog_bot.application.handlers.admin import (
    handle_admin_create,
    handle_admin_delete,
    handle_get_admins,
)
from catalog_bot.application.tg.states.admin import AdminState

router = Router()


dialog = Dialog(
    Window(
        Const('Список действуюших админов\n'),
        Format('{message}'),
        SwitchTo(
            Const('Добавить админа'),
            id='create_admin',
            state=AdminState.create,
        ),
        SwitchTo(
            Const('Удалить админа'),
            id='delete_admin',
            state=AdminState.delete,
        ),
        state=AdminState.start,
        getter=handle_get_admins,
    ),
    Window(
        Const(
            'Отправьте telegram_id или @username пользователя, '
            'которого хотите добавить в администраторы',
        ),
        MessageInput(handle_admin_create),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_admin',
            state=AdminState.start,
        ),
        state=AdminState.create,
    ),
    Window(
        Const(
            'Отправьте telegram_id или @username пользователя, '
            'которого хотите удалить из администраторов',
        ),
        MessageInput(handle_admin_delete),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_delete_admin',
            state=AdminState.start,
        ),
        state=AdminState.delete,
    ),
)

router.include_router(dialog)
