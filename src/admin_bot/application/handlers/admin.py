import re
from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from admin_bot.application.services.catalog_bot import CatalogService
from admin_bot.application.state.start import StartState
from admin_bot.application.tasks.catalog_bot import start_catalog_bot, stop_catalog_bot
from admin_bot.application.tasks.catalog_bot.base import get_catalog_bot_status


async def handle_catalog_bot_set_title(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['catalog_bot_text'] = message.text
    await manager.switch_to(StartState.create_bot_set_token)


async def handle_catalog_bot_set_token(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    catalog_bot_title = manager.dialog_data['catalog_bot_text']
    catalog_bot_token = message.text
    if not re.fullmatch(r'\d+:\w+-\w+', catalog_bot_token):
        await bot.send_message(
            message.from_user.id,
            '❌ Введён несуществующий токен',
        )
        return
    catalog_bot_id = message.text.split(':')[0]
    catalog_bot_service = manager.middleware_data['container'].resolve(CatalogService)
    catalog_bot_uuid = await catalog_bot_service.create_catalog_bot(
        title=catalog_bot_title,
        bot_token=catalog_bot_token,
        telegram_owner_id=message.from_user.id,
        telegram_bot_id=catalog_bot_id,
    )
    manager.dialog_data.update({'catalog_bot_text': None})
    manager.dialog_data.update({'catalog_bot_uuid': catalog_bot_uuid})
    await manager.switch_to(StartState.catalog_bot_detail)


async def get_catalog_bots_by_telegram_owner_id(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    catalog_bot_service = middleware_data['container'].resolve(CatalogService)

    bots = await catalog_bot_service.get_bots_by_telegram_owner_id(
        telegram_owner_id=dialog_manager.event.from_user.id,
    )
    return {'catalog_bots': bots}


async def change_state_to_catalog_bot_detail(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data['catalog_bot_uuid'] = item_id
    await manager.switch_to(StartState.catalog_bot_detail)


async def get_catalog_bot(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    catalog_bot_service = middleware_data['container'].resolve(CatalogService)
    catalog_bot_uuid = dialog_manager.dialog_data['catalog_bot_uuid']

    catalog_bot = await catalog_bot_service.get_bot_by_uuid(catalog_bot_uuid)
    status = await get_catalog_bot_status(catalog_bot.token)
    status_text = '🟢 Включить' if not status else '🔴 Выключить'

    dialog_manager.dialog_data['telegram_bot_token'] = catalog_bot.token
    dialog_manager.dialog_data['catalog_bot_status'] = status

    return {'catalog_bot': catalog_bot, 'status_text': status_text}


async def switch_container_status(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    telegram_bot_token = manager.dialog_data['telegram_bot_token']
    status = manager.dialog_data['catalog_bot_status']
    if status:
        await stop_catalog_bot(telegram_bot_token)
    else:
        await start_catalog_bot(telegram_bot_token)
    await manager.switch_to(StartState.catalog_bot_detail)
