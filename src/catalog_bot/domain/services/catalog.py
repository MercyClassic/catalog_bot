from uuid import UUID

from catalog_bot.domain.entities.catalog import CategoryEntity, ChannelEntity


class CatalogService:
    def create_category(
        self,
        title: str,
        bot_uuid: UUID,
        category_uuid: UUID | None = None,
    ) -> CategoryEntity:
        return CategoryEntity(
            uuid=None,
            title=title,
            description=None,
            image=None,
            bot_uuid=bot_uuid,
            category_uuid=category_uuid,
        )

    def create_channel(
        self,
        chat_id: int,
        title: str,
        bot_uuid: UUID,
        category_uuid: UUID | None = None,
    ) -> ChannelEntity:
        return ChannelEntity(
            uuid=None,
            chat_id=chat_id,
            bot_uuid=bot_uuid,
            title=title,
            link=None,
            auto_commit=False,
            category_uuid=category_uuid,
        )
