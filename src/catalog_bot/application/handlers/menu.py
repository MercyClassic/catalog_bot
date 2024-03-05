from typing import Any

from aiogram import types
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput

from catalog_bot.application.interactors.menu.change_media import ChangeMedia
from catalog_bot.application.interactors.menu.change_text import ChangeText
from catalog_bot.application.interactors.menu.get_menu import GetMenu
from catalog_bot.application.services.welcome_message import WelcomeMessageService
from catalog_bot.application.tg.states.menu import MenuState
from catalog_bot.domain.entities.welcome_message import ButtonEntity
from catalog_bot.domain.exceptions.welcome_message import WelcomeMessageLimit


async def handle_text_change(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_text = manager.middleware_data['container'].resolve(ChangeText)

    await change_text.execute(
        text=message.text,
        bot_id=bot.id,
    )
    await bot.send_message(
        message.from_user.id,
        '✅',
    )
    await bot.send_message(
        message.from_user.id,
        'Текст успешно изменён',
    )
    await manager.switch_to(MenuState.start)


async def handle_media_change(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_media = manager.middleware_data['container'].resolve(ChangeMedia)
    if message.video:
        media_id = message.video.file_id
    else:
        media_id = message.photo[-1].file_id

    await change_media.execute(
        file_id=media_id,
        bot_id=bot.id,
    )
    await bot.send_message(
        message.from_user.id,
        '✅',
    )
    await bot.send_message(
        message.from_user.id,
        'Медиа успешно изменено',
    )
    await manager.switch_to(MenuState.start)


async def set_bot_uuid(
    _: Any,
    dialog_manager: DialogManager,
) -> None:
    get_menu = dialog_manager.middleware_data['container'].resolve(GetMenu)
    menu = await get_menu.execute(dialog_manager.middleware_data['bot'].id)
    dialog_manager.dialog_data['bot_uuid'] = menu.bot_uuid


async def change_state_to_get_welcome_message_detail(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_data: str,
) -> None:
    welcome_message_uuid, welcome_message_order = item_data.split(':')
    manager.dialog_data['welcome_message_uuid'] = welcome_message_uuid
    manager.dialog_data['welcome_message_order'] = welcome_message_order
    await manager.switch_to(MenuState.welcome_message_detail)


async def get_welcome_messages(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    channel_uuid = dialog_manager.dialog_data['bot_uuid']
    wm_service = middleware_data['container'].resolve(WelcomeMessageService)
    messages = await wm_service.get_welcome_messages(object_uuid=channel_uuid)
    for index, message in enumerate(messages):
        message.order = index + 1
        message.button_data = '%s:%s' % (message.uuid, message.order)
    return {'welcome_messages': messages}


async def get_welcome_message_detail(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    welcome_message_uuid = dialog_manager.dialog_data['welcome_message_uuid']
    message_order = dialog_manager.dialog_data.get('welcome_message_order') or 'последним'
    wm_service = middleware_data['container'].resolve(WelcomeMessageService)
    message = await wm_service.get_welcome_message(welcome_message_uuid=welcome_message_uuid)
    text = (
        f'Текст сообщения: {message.text}\n\n'
        f'*Это сообщение будет отправлено {message_order} по счёту\n\n'
    )
    if message.buttons:
        text += 'Кнопки, которые прикреплены к этому сообщению:\n'
        for button in message.buttons:
            text += f'{button.text}\n'
    data = {'message': text, 'message_media': None}
    if message.media:
        media = MediaAttachment(ContentType.PHOTO, file_id=MediaId(message.media))
        data.update({'message_media': media})
    return data


async def handle_welcome_message_delete(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    wm_service = manager.middleware_data['container'].resolve(WelcomeMessageService)
    welcome_message_uuid = manager.dialog_data['welcome_message_uuid']

    await wm_service.delete_welcome_message(welcome_message_uuid)

    await manager.switch_to(MenuState.get_welcome_messages)


async def handle_welcome_message_create_set_title(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['welcome_message_text'] = message.text
    await manager.switch_to(MenuState.welcome_message_create_set_media)


async def handle_welcome_message_create_set_media(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['welcome_message_media'] = message.photo[-1].file_id
    await manager.switch_to(MenuState.welcome_message_choose_button_or_create)


async def handle_welcome_message_create_set_button_type(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_type: str,
) -> None:
    manager.dialog_data['welcome_message_button_type'] = item_type
    await manager.switch_to(MenuState.welcome_message_create_set_buttons)


async def handle_welcome_message_create_set_button(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    buttons = manager.dialog_data.get('welcome_message_buttons', [])
    button_type = manager.dialog_data['welcome_message_button_type']
    button = ButtonEntity(uuid=None, message_uuid=None, type=button_type, text=message.text)
    buttons.append(button)
    manager.dialog_data['welcome_message_buttons'] = buttons

    await bot.send_message(
        message.from_user.id,
        '✅ Кнопка успешно создана! Добавьте ещё, если это требуется, или нажмите продолжить',
    )


async def handle_welcome_message_create(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    wm_service = manager.middleware_data['container'].resolve(WelcomeMessageService)

    try:
        welcome_message = await wm_service.create_welcome_message(
            object_uuid=manager.dialog_data['bot_uuid'],
            owner_type='bot',
            text=manager.dialog_data['welcome_message_text'],
            media=manager.dialog_data.get('welcome_message_media'),
            buttons=manager.dialog_data.get('welcome_message_buttons', []),
        )
    except WelcomeMessageLimit:
        bot = manager.middleware_data['bot']
        await bot.send_message(
            callback.from_user.id,
            'Лимит приветственных сообщений - 5 штук\nНовое сообщение не было создано',
        )
        await manager.switch_to(MenuState.start)
    else:
        await bot.send_message(
            callback.from_user.id,
            '✅ Сообщение успешно создано!',
        )
        manager.dialog_data['welcome_message_uuid'] = welcome_message.uuid
        await manager.switch_to(MenuState.welcome_message_detail)
    finally:
        manager.dialog_data.update({'welcome_message_order': None})
        manager.dialog_data.update({'welcome_message_text': None})
        manager.dialog_data.update({'welcome_message_media': None})
        manager.dialog_data.update({'welcome_message_button_type': None})
        manager.dialog_data.update({'welcome_message_buttons': []})


async def handle_welcome_message_change_text(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    wm_service = manager.middleware_data['container'].resolve(WelcomeMessageService)
    welcome_message_uuid = manager.dialog_data['welcome_message_uuid']

    await wm_service.change_welcome_message_text(welcome_message_uuid, message.text)
    await bot.send_message(
        message.from_user.id,
        '✅ Текст успешно изменён!',
    )
    await manager.switch_to(MenuState.welcome_message_detail)


async def handle_welcome_message_change_media(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    wm_service = manager.middleware_data['container'].resolve(WelcomeMessageService)
    welcome_message_uuid = manager.dialog_data['welcome_message_uuid']
    if message.video:
        media_id = message.video.file_id
    else:
        media_id = message.photo[-1].file_id

    await wm_service.change_welcome_message_media(welcome_message_uuid, media_id)
    await bot.send_message(
        message.from_user.id,
        '✅ Медиа успешно изменено!',
    )
    await manager.switch_to(MenuState.welcome_message_detail)
