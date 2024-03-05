from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.catalog import CategoryEntity, ChannelEntity


class CatalogServiceInterface(Protocol):
    def create_category(
        self,
        title: str,
        bot_uuid: UUID,
    ) -> CategoryEntity:
        raise NotImplementedError

    def create_channel(
        self,
        chat_id: int,
        subcategory_uuid: UUID,
    ) -> ChannelEntity:
        raise NotImplementedError
