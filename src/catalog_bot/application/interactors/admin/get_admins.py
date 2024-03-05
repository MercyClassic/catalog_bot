from catalog_bot.domain.entities.bot import AdminEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetAdmins:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, bot_id: int) -> list[AdminEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        admins = await self.uow.bot_repo.get_admins(
            bot_uuid=bot.uuid,
        )
        return admins
