from uuid import UUID

from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.exceptions.catalog import CategoryAlreadyExists
from catalog_bot.domain.services.catalog import CatalogService
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class CreateCategory:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow
        self.catalog_service = CatalogService()

    async def execute(
        self,
        title: str,
        bot_id: int,
        category_uuid: UUID | None,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        category_exists = await self.uow.category_repo.is_category_exists(
            title=title,
            category_uuid=category_uuid,
        )
        if category_exists:
            raise CategoryAlreadyExists
        category = self.catalog_service.create_category(
            title=title,
            bot_uuid=bot.uuid,
            category_uuid=category_uuid,
        )
        await self.uow.category_repo.save_category(category)
