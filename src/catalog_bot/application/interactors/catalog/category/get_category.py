from uuid import UUID

from catalog_bot.domain.entities.catalog import CategoryEntity
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetCategory:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, category_uuid: UUID) -> CategoryEntity:
        category = await self.uow.category_repo.get_category(category_uuid)
        return category
