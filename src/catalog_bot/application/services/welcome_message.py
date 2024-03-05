from typing import Literal
from uuid import UUID

from catalog_bot.domain.entities.welcome_message import (
    ButtonEntity,
    WelcomeMessageEntity,
)
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.exceptions.catalog import ChannelNotFound
from catalog_bot.domain.exceptions.welcome_message import WelcomeMessageLimit
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class WelcomeMessageService:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def get_welcome_messages_by_bot_id(self, bot_id: int) -> list[WelcomeMessageEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        messages = await self.uow.welcome_message_repo.get_messages(object_uuid=bot.uuid)
        return messages

    async def get_welcome_messages_by_chat_id(
        self,
        bot_id: int,
        chat_id: int,
    ) -> list[WelcomeMessageEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        channel = await self.uow.channel_repo.get_channel_by_chat_id(
            bot_uuid=bot.uuid,
            chat_id=chat_id,
        )
        if not channel:
            raise ChannelNotFound
        messages = await self.uow.welcome_message_repo.get_messages(object_uuid=channel.uuid)
        return messages

    async def get_welcome_messages(self, object_uuid: UUID) -> list[WelcomeMessageEntity]:
        messages = await self.uow.welcome_message_repo.get_messages(object_uuid=object_uuid)
        return messages

    async def get_welcome_message(self, welcome_message_uuid: UUID) -> WelcomeMessageEntity:
        return await self.uow.welcome_message_repo.get_welcome_message(welcome_message_uuid)

    async def delete_welcome_message(self, welcome_message_uuid: UUID) -> None:
        await self.uow.welcome_message_repo.delete_welcome_message(welcome_message_uuid)

    async def create_welcome_message(
        self,
        object_uuid: UUID,
        owner_type: Literal['bot', 'channel'],
        text: str,
        media: str,
        buttons: list[ButtonEntity],
    ) -> WelcomeMessageEntity:
        count = await self.uow.welcome_message_repo.get_welcome_messages_count(
            object_uuid=object_uuid,
        )
        if count >= 5:
            raise WelcomeMessageLimit
        entity = WelcomeMessageEntity(
            uuid=None,
            object_uuid=object_uuid,
            owner_type=owner_type,
            text=text,
            media=media,
            order=None,
            buttons=buttons,
        )
        message = await self.uow.welcome_message_repo.save_welcome_message(entity)
        return message

    async def change_welcome_message_text(self, welcome_message_uuid: UUID, text: str) -> None:
        await self.uow.welcome_message_repo.edit_message_text(welcome_message_uuid, text)

    async def change_welcome_message_media(self, welcome_message_uuid: UUID, media_id: str) -> None:
        await self.uow.welcome_message_repo.edit_message_media(welcome_message_uuid, media_id)
