from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class IsTapClientExist:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, telegram_id: int, bot_id: int) -> bool:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        return await self.uow.tap_client_repo.is_tap_client_exist(telegram_id, bot.uuid)
