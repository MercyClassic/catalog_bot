from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models import Prefetch

from catalog_bot.domain.entities.catalog import CategoryEntity, ChannelEntity
from catalog_bot.infrastructure.db.models.catalog import Category, Channel


class CategoryRepository:
    async def get_categories(self, bot_uuid: UUID) -> list[CategoryEntity]:
        categories = await sync_to_async(list)(
            Category.objects.filter(bot_id=bot_uuid, category_id=None).prefetch_related(
                Prefetch(
                    'subcategories',
                    Category.objects.all().prefetch_related('channels'),
                ),
                'channels',
            ),
        )
        categories = self._serialize_catalog(categories)
        return categories

    async def get_category(self, category_uuid: UUID) -> CategoryEntity:
        query = Category.objects.prefetch_related('subcategories', 'channels').aget(
            uuid=category_uuid,
        )
        category = await query
        return self._serialize_category(
            category,
            category.subcategories.all(),
            category.channels.all(),
        )

    def _serialize_channels(self, category: CategoryEntity, channels: list[Channel]) -> None:
        for channel in channels:
            serialized_channel = ChannelEntity(
                uuid=channel.uuid,
                chat_id=channel.chat_id,
                bot_uuid=channel.bot_id,
                title=channel.title,
                link=channel.link,
                auto_commit=channel.auto_commit,
                category_uuid=channel.category_id,
            )
            category.channels.append(serialized_channel)

    def _serialize_category(
        self,
        category: Category,
        subcategories: list[Category] = None,
        channels: list[Channel] = None,
    ) -> CategoryEntity:
        return CategoryEntity(
            uuid=category.uuid,
            title=category.title,
            description=category.description,
            bot_uuid=category.bot_id,
            image=category.image,
            category_uuid=category.category_id,
            subcategories=subcategories or [],
            channels=channels or [],
        )

    def _serialize_catalog(self, categories: list[Category]) -> list[CategoryEntity]:
        entities = []
        for category in categories:
            serialized_category = self._serialize_category(category)
            self._serialize_channels(serialized_category, category.channels.all())

            for subcategory in category.subcategories.all():
                serialized_subcategory = self._serialize_category(subcategory)
                serialized_category.subcategories.append(serialized_subcategory)
                self._serialize_channels(subcategory, subcategory.channels.all())

            entities.append(serialized_category)
        return entities

    async def save_category(
        self,
        category: CategoryEntity,
    ) -> None:
        category_db = Category(
            title=category.title,
            bot_id=category.bot_uuid,
            category_id=category.category_uuid,
        )
        await category_db.asave()

    async def is_category_exists(
        self,
        title: str,
        category_uuid: UUID,
    ) -> bool:
        query = Category.objects.filter(title=title, category_id=category_uuid).aexists()
        return await query

    async def is_category_exists_by_uuid(
        self,
        uuid: UUID,
    ) -> bool:
        return await Category.objects.filter(uuid=uuid).aexists()

    async def change_category_title(
        self,
        category_uuid: UUID,
        title: str,
    ) -> None:
        await Category.objects.filter(uuid=category_uuid).aupdate(title=title)

    async def change_category_description(
        self,
        category_uuid: UUID,
        description: str,
    ) -> None:
        await Category.objects.filter(uuid=category_uuid).aupdate(description=description)

    async def change_category_image(
        self,
        category_uuid: UUID,
        image: str,
    ) -> None:
        await Category.objects.filter(uuid=category_uuid).aupdate(image=image)

    async def delete_category(self, category_uuid: UUID) -> None:
        await Category.objects.filter(uuid=category_uuid).adelete()
