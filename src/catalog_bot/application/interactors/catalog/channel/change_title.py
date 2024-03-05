from uuid import UUID

from catalog_bot.domain.exceptions.catalog import ChannelNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class ChangeChannelTitle:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        channel_uuid: UUID,
        title: str,
    ) -> None:
        channel = await self.uow.channel_repo.get_channel(channel_uuid=channel_uuid)
        if not channel:
            raise ChannelNotFound
        await self.uow.channel_repo.change_channel_title(
            channel_uuid=channel_uuid,
            title=title,
        )
