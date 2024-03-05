from typing import Any

from aiogram.enums import ContentType
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput

from catalog_bot.application.interactors.catalog.channel.change_auto_commit import (
    ChangeChannelAutoCommit,
)
from catalog_bot.application.interactors.catalog.channel.change_link import (
    ChangeChannelLink,
)
from catalog_bot.application.interactors.catalog.channel.change_title import (
    ChangeChannelTitle,
)
from catalog_bot.application.interactors.catalog.channel.delete_channel import (
    DeleteChannel,
)
from catalog_bot.application.interactors.catalog.channel.get_channel_by_uuid import (
    GetChannelByUUID,
)
from catalog_bot.application.interactors.catalog.channel.register_channel import (
    RegisterChannel,
)
from catalog_bot.application.services.welcome_message import WelcomeMessageService
from catalog_bot.application.tg.states.admin import AdminCatalogState
from catalog_bot.domain.entities.welcome_message import ButtonEntity
from catalog_bot.domain.exceptions.catalog import (
    CategoryNotFound,
    ChannelAlreadyExists,
    ChannelNotFound,
)
from catalog_bot.domain.exceptions.welcome_message import WelcomeMessageLimit


async def change_state_to_get_channel_detail(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data['channel_uuid'] = item_id
    await manager.switch_to(AdminCatalogState.channel_detail)


async def handle_get_channel(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, Any]:
    channel_uuid = dialog_manager.dialog_data['channel_uuid']
    get_channel = middleware_data['container'].resolve(GetChannelByUUID)

    channel = await get_channel.execute(channel_uuid=channel_uuid)
    dialog_manager.dialog_data['channel_autocommit_status'] = channel.auto_commit

    message = f'Название канала: {channel.title}\n'
    if channel.link:
        message += f'Своя ссылка: {channel.link}'

    return {'message': message}


async def handle_channel_create(  # noqa CCR001
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    register_channel = manager.middleware_data['container'].resolve(RegisterChannel)
    category_uuid = manager.dialog_data.get('category_uuid')

    chat = message.forward_from_chat
    if not chat:
        await bot.send_message(
            message.from_user.id,
            'Перешлите сообщение из канала!',
        )
        return

    try:
        membership = await bot.get_chat_member(chat.id, bot.id)
    except TelegramForbiddenError as exc:
        if exc.message == 'Forbidden: bot is not a member of the channel chat':
            await bot.send_message(
                message.from_user.id,
                'Сделайте бота администратором и дайте права на добавление пользователей!',
            )
            return
        else:
            raise exc
    if membership.status != 'administrator' or not membership.can_manage_chat:
        await bot.send_message(
            message.from_user.id,
            'Сделайте бота администратором и дайте права на добавление пользователей!',
        )
        return

    try:
        await register_channel.execute(
            chat_id=chat.id,
            title=chat.title,
            bot_id=bot.id,
            category_uuid=category_uuid,
        )
    except ChannelAlreadyExists:
        text = 'Канал уже существует'
    except CategoryNotFound:
        text = 'Выбранная категория не найдена'
    else:
        text = 'Канал успешно создан!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.start)


async def handle_channel_change_title(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_title = manager.middleware_data['container'].resolve(ChangeChannelTitle)
    channel_uuid = manager.dialog_data['channel_uuid']

    try:
        await change_title.execute(
            channel_uuid=channel_uuid,
            title=message.text,
        )
    except ChannelNotFound:
        text = 'Канал не найден'
    else:
        text = 'Название успешно изменено!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.channel_detail)


async def handle_channel_change_link(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_link = manager.middleware_data['container'].resolve(ChangeChannelLink)
    channel_uuid = manager.dialog_data['channel_uuid']

    try:
        await change_link.execute(
            channel_uuid=channel_uuid,
            link=message.text,
        )
    except ChannelNotFound:
        text = 'Канал не найден'
    else:
        text = 'Ссылка успешно удалена!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.channel_detail)


async def handle_channel_change_autocommit(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    change_auto_commit = manager.middleware_data['container'].resolve(ChangeChannelAutoCommit)
    channel_uuid = manager.dialog_data['channel_uuid']

    try:
        await change_auto_commit.execute(channel_uuid=channel_uuid)
    except ChannelNotFound:
        pass
    await manager.switch_to(AdminCatalogState.channel_detail)


async def get_channel_autocommit_button_text(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    status = dialog_manager.dialog_data['channel_autocommit_status']
    return {'text': '🟢 Включено' if status else '🔴 Выключено'}


async def handle_channel_delete(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    delete_channel = manager.middleware_data['container'].resolve(DeleteChannel)
    channel_uuid = manager.dialog_data['channel_uuid']

    try:
        await delete_channel.execute(
            channel_uuid=channel_uuid,
        )
    except CategoryNotFound:
        text = 'Канал не найден'
    else:
        text = 'Канал успешно удален'

    await bot.send_message(
        callback.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.start)


async def change_state_to_get_welcome_message_detail(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_data: str,
) -> None:
    welcome_message_uuid, welcome_message_order = item_data.split(':')
    manager.dialog_data['welcome_message_uuid'] = welcome_message_uuid
    manager.dialog_data['welcome_message_order'] = welcome_message_order
    await manager.switch_to(AdminCatalogState.welcome_message_detail)


async def get_welcome_messages(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, str]:
    channel_uuid = dialog_manager.dialog_data['channel_uuid']
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

    await manager.switch_to(AdminCatalogState.get_welcome_messages)


async def handle_welcome_message_create_set_title(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['welcome_message_text'] = message.text
    await manager.switch_to(AdminCatalogState.welcome_message_create_set_media)


async def handle_welcome_message_create_set_media(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['welcome_message_media'] = message.photo[-1].file_id
    await manager.switch_to(AdminCatalogState.welcome_message_choose_button_or_create)


async def handle_welcome_message_create_set_button_type(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_type: str,
) -> None:
    manager.dialog_data['welcome_message_button_type'] = item_type
    await manager.switch_to(AdminCatalogState.welcome_message_create_set_buttons)


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
            object_uuid=manager.dialog_data['channel_uuid'],
            owner_type='channel',
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
        await manager.switch_to(AdminCatalogState.channel_detail)
    else:
        await bot.send_message(
            callback.from_user.id,
            '✅ Сообщение успешно создано!',
        )
        manager.dialog_data['welcome_message_uuid'] = welcome_message.uuid
        await manager.switch_to(AdminCatalogState.welcome_message_detail)
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
    await manager.switch_to(AdminCatalogState.welcome_message_detail)


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
    await manager.switch_to(AdminCatalogState.welcome_message_detail)
