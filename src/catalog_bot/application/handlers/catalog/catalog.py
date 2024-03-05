from typing import Any

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from catalog_bot.application.interactors.catalog.category.get_categories import (
    GetCategories,
)
from catalog_bot.application.interactors.catalog.channel.get_channels import GetChannels
from catalog_bot.application.interactors.menu.get_menu import GetMenu


async def handle_get_catalog(
    for_admin: bool = False,
    **middleware_data,
) -> dict[str, Any]:
    container = middleware_data['container']
    bot = middleware_data['bot']
    menu = await container.resolve(GetMenu).execute(bot.id)
    categories = await container.resolve(GetCategories).execute(bot.id)
    channels = await container.resolve(GetChannels).execute(bot.id)
    if not for_admin:
        channels = list(filter(lambda channel: channel.link is not None, channels))

    data = {
        'menu': menu,
        'menu_media': None,
        'categories': categories,
        'channels': channels,
    }
    if menu.media:
        data['menu_media'] = MediaAttachment(ContentType.PHOTO, file_id=MediaId(menu.media))
    return data
