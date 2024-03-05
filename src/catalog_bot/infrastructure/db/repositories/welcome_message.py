from uuid import UUID

from asgiref.sync import sync_to_async

from catalog_bot.domain.entities.welcome_message import (
    ButtonEntity,
    WelcomeMessageEntity,
)
from catalog_bot.infrastructure.db.models import Button, WelcomeMessage


class WelcomeMessageRepository:
    def _serialize_welcome_message(
        self,
        message: WelcomeMessage,
        buttons: list[Button] = None,
    ) -> WelcomeMessageEntity:
        return WelcomeMessageEntity(
            uuid=message.uuid,
            object_uuid=message.object_id,
            owner_type=message.owner_type,
            text=message.text,
            media=message.media,
            order=message.order,
            buttons=buttons or [],
        )

    async def get_messages(self, object_uuid: UUID) -> list[WelcomeMessageEntity]:
        messages = await sync_to_async(list)(
            WelcomeMessage.objects.filter(object_id=object_uuid)
            .prefetch_related('buttons')
            .order_by('order'),
        )
        entities = []
        for message in messages:
            serialized_message = self._serialize_welcome_message(message)
            for button in message.buttons.all():
                serialized_message.buttons.append(
                    ButtonEntity(
                        uuid=button.uuid,
                        message_uuid=message.uuid,
                        type=button.type,
                        text=button.text,
                    ),
                )
            entities.append(serialized_message)
        return entities

    async def get_welcome_message(self, welcome_message_uuid: UUID) -> WelcomeMessageEntity:
        message = await WelcomeMessage.objects.aget(uuid=welcome_message_uuid)
        return self._serialize_welcome_message(message)

    async def get_welcome_messages_count(self, object_uuid: UUID) -> int:
        return await WelcomeMessage.objects.filter(object_id=object_uuid).acount()

    async def delete_welcome_message(self, welcome_message_uuid: UUID) -> None:
        await WelcomeMessage.objects.filter(uuid=welcome_message_uuid).adelete()

    async def save_welcome_message(
        self,
        welcome_message: WelcomeMessageEntity,
    ) -> WelcomeMessageEntity:
        message_db = WelcomeMessage(
            object_id=welcome_message.object_uuid,
            owner_type=welcome_message.owner_type,
            text=welcome_message.text,
            media=welcome_message.media,
            order=welcome_message.order,
        )
        await message_db.asave()
        buttons = [
            Button(
                message_id=message_db.uuid,
                type=button.type,
                text=button.text,
            )
            for button in welcome_message.buttons
        ]
        await Button.objects.abulk_create(buttons)
        welcome_message.uuid = message_db.uuid
        return welcome_message

    async def edit_message_text(self, welcome_message_uuid: UUID, text: str) -> None:
        await WelcomeMessage.objects.filter(uuid=welcome_message_uuid).aupdate(text=text)

    async def edit_message_media(self, welcome_message_uuid: UUID, media_id: str) -> None:
        await WelcomeMessage.objects.filter(uuid=welcome_message_uuid).aupdate(media=media_id)
