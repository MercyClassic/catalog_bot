from uuid import UUID

from catalog_bot.domain.exceptions.catalog import CategoryNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class ChangeCategoryDescription:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        category_uuid: UUID,
        description: str,
    ) -> None:
        category_exists = await self.uow.category_repo.is_category_exists_by_uuid(category_uuid)
        if not category_exists:
            raise CategoryNotFound
        await self.uow.category_repo.change_category_description(
            category_uuid=category_uuid,
            description=description,
        )
