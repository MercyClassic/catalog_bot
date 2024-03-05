from typing import Any

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput

from catalog_bot.application.interactors.catalog.category.change_description import (
    ChangeCategoryDescription,
)
from catalog_bot.application.interactors.catalog.category.change_image import (
    ChangeCategoryImage,
)
from catalog_bot.application.interactors.catalog.category.change_title import (
    ChangeCategoryTitle,
)
from catalog_bot.application.interactors.catalog.category.create_category import (
    CreateCategory,
)
from catalog_bot.application.interactors.catalog.category.delete_category import (
    DeleteCategory,
)
from catalog_bot.application.interactors.catalog.category.get_category import (
    GetCategory,
)
from catalog_bot.application.tg.states.admin import AdminCatalogState
from catalog_bot.application.tg.states.client import ClientCatalogState
from catalog_bot.domain.exceptions.catalog import (
    CategoryAlreadyExists,
    CategoryNotFound,
)


async def change_client_state_to_get_category_detail(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data['category_uuid'] = item_id
    await manager.switch_to(ClientCatalogState.category_detail)


async def change_admin_state_to_get_category_detail(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data['category_uuid'] = item_id
    await manager.switch_to(AdminCatalogState.category_detail)


async def handle_get_category(
    dialog_manager: DialogManager,
    **middleware_data,
) -> dict[str, Any]:
    get_category = middleware_data['container'].resolve(GetCategory)
    category_uuid = dialog_manager.dialog_data['category_uuid']

    category = await get_category.execute(category_uuid=category_uuid)

    message = f'Название категории: {category.title}\n'
    if category.description:
        message += f'Описание категории: {category.description}'

    data = {
        'message': message,
        'categories': category.subcategories,
        'channels': category.channels,
        'category_media': None,
    }
    if category.image:
        data['category_media'] = MediaAttachment(ContentType.PHOTO, file_id=MediaId(category.image))
    return data


async def handle_category_create(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    create_category = manager.middleware_data['container'].resolve(CreateCategory)
    parent_category_uuid = manager.dialog_data.get('category_uuid')
    try:
        await create_category.execute(
            title=message.text,
            bot_id=bot.id,
            category_uuid=parent_category_uuid,
        )
    except CategoryAlreadyExists:
        text = 'Категория с таким названием уже существует, попробуйте другое название'
    else:
        text = 'Категория успешно создана!'
        await manager.switch_to(AdminCatalogState.start)

    await bot.send_message(
        message.from_user.id,
        text,
    )


async def handle_category_change_title(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_title = manager.middleware_data['container'].resolve(ChangeCategoryTitle)
    category_uuid = manager.dialog_data['category_uuid']

    try:
        await change_title.execute(
            category_uuid=category_uuid,
            title=message.text,
        )
    except CategoryNotFound:
        text = 'Категория не найдена'
    else:
        text = 'Название успешно изменено!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.category_detail)


async def handle_category_change_description(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_description = manager.middleware_data['container'].resolve(ChangeCategoryDescription)
    category_uuid = manager.dialog_data['category_uuid']

    try:
        await change_description.execute(
            category_uuid=category_uuid,
            description=message.text,
        )
    except CategoryNotFound:
        text = 'Категория не найден'
    else:
        text = 'Описание успешно удалено!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.category_detail)


async def handle_category_change_image(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    change_image = manager.middleware_data['container'].resolve(ChangeCategoryImage)
    category_uuid = manager.dialog_data['category_uuid']
    if message.video:
        media_id = message.video.file_id
    else:
        media_id = message.photo[-1].file_id

    try:
        await change_image.execute(
            category_uuid=category_uuid,
            image=media_id,
        )
    except CategoryNotFound:
        text = 'Категория не найдена'
    else:
        text = 'Фото успешно изменено!'

    await bot.send_message(
        message.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.category_detail)


async def handle_category_delete(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    delete_category = manager.middleware_data['container'].resolve(DeleteCategory)
    category_uuid = manager.dialog_data['category_uuid']

    try:
        await delete_category.execute(
            category_uuid=category_uuid,
        )
    except CategoryNotFound:
        text = 'Категория не найдена'
    else:
        text = 'Категория успешно удалена'

    await bot.send_message(
        callback.from_user.id,
        text,
    )
    await manager.switch_to(AdminCatalogState.start)
