from uuid import UUID

from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.exceptions.catalog import CategoryNotFound, ChannelAlreadyExists
from catalog_bot.domain.services.catalog import CatalogService
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class RegisterChannel:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow
        self.catalog_service = CatalogService()

    async def execute(
        self,
        chat_id: int,
        title: str,
        bot_id: int,
        category_uuid: UUID | None,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        if category_uuid:
            category_exists = await self.uow.category_repo.is_category_exists_by_uuid(
                uuid=category_uuid,
            )
            if not category_exists:
                raise CategoryNotFound
        channel_exists = await self.uow.channel_repo.is_channel_exists(
            chat_id=chat_id,
            category_uuid=category_uuid,
        )
        if channel_exists:
            raise ChannelAlreadyExists
        channel = self.catalog_service.create_channel(
            chat_id=chat_id,
            bot_uuid=bot.uuid,
            title=title,
            category_uuid=category_uuid,
        )
        await self.uow.channel_repo.save_channel(channel)
