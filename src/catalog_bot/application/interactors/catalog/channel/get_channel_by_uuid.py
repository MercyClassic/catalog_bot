from uuid import UUID

from catalog_bot.domain.entities.catalog import ChannelEntity
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetChannelByUUID:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(self, channel_uuid: UUID) -> ChannelEntity:
        channel = await self.uow.channel_repo.get_channel(channel_uuid=channel_uuid)
        return channel
