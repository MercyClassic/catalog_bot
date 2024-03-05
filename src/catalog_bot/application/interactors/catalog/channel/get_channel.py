from catalog_bot.domain.entities.catalog import ChannelEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetChannel:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, bot_id: int, chat_id: int) -> ChannelEntity:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        channel = await self.uow.channel_repo.get_channel_by_chat_id(
            chat_id=chat_id,
            bot_uuid=bot.uuid,
        )
        return channel
