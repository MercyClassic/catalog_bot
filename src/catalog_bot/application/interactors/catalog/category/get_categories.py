from catalog_bot.domain.entities.catalog import CategoryEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetCategories:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, bot_id: int) -> list[CategoryEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        categories = await self.uow.category_repo.get_categories(bot.uuid)
        return categories
