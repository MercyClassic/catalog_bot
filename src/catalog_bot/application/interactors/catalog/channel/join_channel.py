from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.exceptions.catalog import (
    ChannelNotFound,
    NoAutoCommitJoinRequest,
)
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class JoinChannel:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, bot_id: int, chat_id: int) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        channel = await self.uow.channel_repo.get_channel_by_chat_id(
            chat_id=chat_id,
            bot_uuid=bot.uuid,
        )
        if not channel:
            raise ChannelNotFound
        if not channel.auto_commit:
            raise NoAutoCommitJoinRequest
