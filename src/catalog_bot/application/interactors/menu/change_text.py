from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class ChangeText:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        text: str,
        bot_id: int,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        await self.uow.bot_repo.change_text_menu(
            text=text,
            bot_uuid=bot.uuid,
        )
