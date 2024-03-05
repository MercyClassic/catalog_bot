from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from catalog_bot.application.interactors.admin.create_admin import CreateAdmin
from catalog_bot.application.interactors.admin.delete_admin import DeleteAdmin
from catalog_bot.application.interactors.admin.get_admins import GetAdmins
from catalog_bot.application.tg.states.admin import AdminState
from catalog_bot.domain.exceptions.bot import (
    AdminAlreadyExist,
    AdminNotFound,
    CantDeleteBotOwner,
    CantDeleteItself,
)
from catalog_bot.domain.exceptions.tap_client import TapClientNotFound


async def handle_get_admins(**middleware_data) -> dict[str, str]:
    bot = middleware_data['bot']
    get_admins = middleware_data['container'].resolve(GetAdmins)

    admins = await get_admins.execute(bot.id)

    message = ''
    for admin in admins:
        admin_info = await bot.get_chat(admin.telegram_id)
        if admin_info.username:
            message += f'@{admin_info.username}, '
        message += f'{admin_info.first_name}\nID: {admin.telegram_id}\n\n'

    return {'message': message}


async def handle_admin_create(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    create_admin = manager.middleware_data['container'].resolve(CreateAdmin)

    try:
        await create_admin.execute(
            telegram_field=message.text.lstrip('@'),
            bot_id=bot.id,
        )
    except AdminAlreadyExist:
        text = 'Такой админ уже существует'
    except TapClientNotFound:
        text = 'Пользователь не найден! Убедитесь что он есть в боте (нажал /start)'
    else:
        text = '✅ Админ успешно создан'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminState.start)


async def handle_admin_delete(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    delete_admin = manager.middleware_data['container'].resolve(DeleteAdmin)

    try:
        await delete_admin.execute(
            executor_id=message.from_user.id,
            telegram_field=message.text.lstrip('@'),
            bot_id=bot.id,
        )
    except AdminNotFound:
        text = 'Админ не найден'
    except TapClientNotFound:
        text = (
            'Пользователь не найден, '
            'вероятно он сменил @username, используйте телеграм id для удаления'
        )
    except CantDeleteItself:
        text = 'Вы не можете удалить себя из админов'
    except CantDeleteBotOwner:
        text = 'Вы не можете удалить главного админа'
    else:
        text = '✅ Админ успешно удалён'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminState.start)
