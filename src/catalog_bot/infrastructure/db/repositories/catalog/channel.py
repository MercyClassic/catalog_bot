from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models import F

from catalog_bot.domain.entities.catalog import ChannelEntity
from catalog_bot.infrastructure.db.models.catalog import Channel


class ChannelRepository:
    async def get_channels(self, bot_uuid: UUID) -> list[ChannelEntity]:
        channels = await sync_to_async(list)(
            Channel.objects.filter(bot_id=bot_uuid, category_id=None),
        )
        return [
            ChannelEntity(
                uuid=channel.uuid,
                chat_id=channel.chat_id,
                bot_uuid=channel.bot_id,
                title=channel.title,
                link=channel.link,
                auto_commit=channel.auto_commit,
                category_uuid=channel.category_id,
            )
            for channel in channels
        ]

    async def save_channel(
        self,
        channel: ChannelEntity,
    ) -> None:
        channel_db = Channel(
            chat_id=channel.chat_id,
            bot_id=channel.bot_uuid,
            title=channel.title,
            category_id=channel.category_uuid,
        )
        await channel_db.asave()

    async def is_channel_exists(
        self,
        chat_id: int,
        category_uuid: UUID | None,
    ) -> bool:
        query = Channel.objects.filter(chat_id=chat_id, category_id=category_uuid).aexists()
        return await query

    def _serialize_channel(self, channel_db: Channel) -> ChannelEntity:
        return ChannelEntity(
            uuid=channel_db.uuid,
            bot_uuid=channel_db.bot_id,
            chat_id=channel_db.chat_id,
            title=channel_db.title,
            link=channel_db.link,
            auto_commit=channel_db.auto_commit,
            category_uuid=channel_db.category_id,
        )

    async def get_channel(
        self,
        channel_uuid: int,
    ) -> ChannelEntity | None:
        query = Channel.objects.filter(uuid=channel_uuid).afirst()
        try:
            channel_db = await query
        except Channel.DoesNotExist:
            return None
        return self._serialize_channel(channel_db)

    async def get_channel_by_chat_id(
        self,
        chat_id: int,
        bot_uuid: UUID,
    ) -> ChannelEntity | None:
        query = Channel.objects.aget(chat_id=chat_id, bot_id=bot_uuid)
        try:
            channel_db = await query
        except Channel.DoesNotExist:
            return None
        return self._serialize_channel(channel_db)

    async def change_channel_title(
        self,
        channel_uuid: UUID,
        title: str,
    ) -> None:
        await Channel.objects.filter(uuid=channel_uuid).aupdate(title=title)

    async def change_channel_link(
        self,
        channel_uuid: UUID,
        link: str | None,
    ) -> None:
        await Channel.objects.filter(uuid=channel_uuid).aupdate(link=link)

    async def change_channel_auto_commit(
        self,
        channel_uuid: UUID,
    ) -> None:
        await Channel.objects.filter(uuid=channel_uuid).aupdate(auto_commit=~F('auto_commit'))

    async def delete_channel(self, channel_uuid: UUID) -> None:
        await Channel.objects.filter(uuid=channel_uuid).adelete()
