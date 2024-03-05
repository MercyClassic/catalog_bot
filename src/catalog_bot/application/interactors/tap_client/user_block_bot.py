from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class UserBlockBot:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        bot_id: int,
        user_id: int,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        await self.uow.tap_client_repo.set_user_block_bot(bot.uuid, user_id)
