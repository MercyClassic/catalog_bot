from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.catalog import ChannelEntity


class ChannelRepositoryInterface(Protocol):
    async def get_channels(self, bot_uuid: UUID) -> list[ChannelEntity]:
        raise NotImplementedError

    async def save_channel(self, channel: ChannelEntity) -> None:
        raise NotImplementedError

    async def is_channel_exists(
        self,
        chat_id: int,
        category_uuid: UUID | None,
    ) -> bool:
        raise NotImplementedError

    async def get_channel(self, channel_uuid: UUID) -> ChannelEntity | None:
        raise NotImplementedError

    async def get_channel_by_chat_id(
        self,
        chat_id: int,
        bot_uuid: UUID,
    ) -> ChannelEntity | None:
        raise NotImplementedError

    async def change_channel_title(
        self,
        channel_uuid: UUID,
        title: str,
    ) -> None:
        raise NotImplementedError

    async def change_channel_link(
        self,
        channel_uuid: UUID,
        link: str | None,
    ) -> None:
        raise NotImplementedError

    async def change_channel_auto_commit(self, channel_uuid: UUID) -> None:
        raise NotImplementedError

    async def delete_channel(self, channel_uuid: UUID) -> None:
        raise NotImplementedError
