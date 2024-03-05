from uuid import UUID

from admin_bot.db.repositories.catalog_bot import CatalogBotRepository
from catalog_bot.infrastructure.db.models import Bot


class CatalogService:
    def __init__(self, catalog_bot_repo: CatalogBotRepository) -> None:
        self.catalog_bot_repo = catalog_bot_repo

    async def create_catalog_bot(
        self,
        title: str,
        bot_token: str,
        telegram_owner_id: int,
        telegram_bot_id: int,
    ) -> UUID:
        catalog_bot_uuid = await self.catalog_bot_repo.save_catalog_bot(
            title,
            bot_token,
            telegram_owner_id,
            telegram_bot_id,
        )
        return catalog_bot_uuid

    async def get_bots_by_telegram_owner_id(
        self,
        telegram_owner_id: int,
    ) -> list[Bot]:
        return await self.catalog_bot_repo.get_bots_by_telegram_owner_id(telegram_owner_id)

    async def get_bot_by_uuid(
        self,
        catalog_bot_uuid: UUID,
    ) -> Bot:
        return await self.catalog_bot_repo.get_bot_by_uuid(catalog_bot_uuid)
