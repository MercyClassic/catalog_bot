from uuid import UUID

from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class CreatePeriodicNewsletter:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        bot_id: int,
        title: str,
        message_id: int,
        from_chat_id: int,
    ) -> UUID:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        uuid = await self.uow.newsletter_repo.save_periodic_newsletter(
            title=title,
            message_id=message_id,
            from_chat_id=from_chat_id,
            bot_uuid=bot.uuid,
        )
        return uuid
