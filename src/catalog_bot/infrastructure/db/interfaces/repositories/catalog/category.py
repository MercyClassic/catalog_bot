from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.catalog import CategoryEntity


class CategoryRepositoryInterface(Protocol):
    async def get_categories(self, bot_uuid: UUID) -> list[CategoryEntity]:
        raise NotImplementedError

    async def get_category(self, category_uuid: UUID) -> CategoryEntity:
        raise NotImplementedError

    async def save_category(
        self,
        category: CategoryEntity,
    ) -> None:
        raise NotImplementedError

    async def is_category_exists(
        self,
        title: str,
        category_uuid: UUID,
    ) -> bool:
        raise NotImplementedError

    async def is_category_exists_by_uuid(
        self,
        uuid: UUID,
    ) -> bool:
        raise NotImplementedError

    async def change_category_title(
        self,
        category_uuid: UUID,
        title: str,
    ) -> None:
        raise NotImplementedError

    async def change_category_description(
        self,
        category_uuid: UUID,
        description: str,
    ) -> None:
        raise NotImplementedError

    async def change_category_image(
        self,
        category_uuid: UUID,
        image: str,
    ) -> None:
        raise NotImplementedError

    async def delete_category(self, category_uuid: UUID) -> None:
        raise NotImplementedError
