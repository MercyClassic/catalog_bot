from catalog_bot.domain.entities.tap_client import TapClientEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetTapClients:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, bot_id: int) -> list[TapClientEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        clients = await self.uow.tap_client_repo.get_tap_clients(bot.uuid)
        return clients
