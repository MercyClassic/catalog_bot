from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class IsAdmin:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        user_id: int,
        bot_id: int,
    ) -> bool:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        is_admin = await self.uow.bot_repo.is_admin_exists(
            telegram_id=user_id,
            bot_uuid=bot.uuid,
        )
        return is_admin
