from uuid import UUID

from catalog_bot.domain.exceptions.catalog import ChannelNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class ChangeChannelLink:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        channel_uuid: UUID,
        link: str | None,
    ) -> None:
        channel = await self.uow.channel_repo.get_channel(channel_uuid=channel_uuid)
        if not channel:
            raise ChannelNotFound
        await self.uow.channel_repo.change_channel_link(
            channel_uuid=channel_uuid,
            link=link,
        )
