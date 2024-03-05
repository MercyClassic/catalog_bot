from catalog_bot.domain.entities.bot import MenuEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.services.bot import BotService
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetMenu:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow
        self.bot_service = BotService()

    async def execute(
        self,
        bot_id: int,
    ) -> MenuEntity:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        menu = self.bot_service.create_menu(bot)
        return menu
