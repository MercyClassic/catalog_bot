from uuid import UUID

from catalog_bot.domain.entities.welcome_message import WelcomeMessageEntity


class WelcomeMessageRepositoryInterface:
    async def get_messages(self, object_uuid: UUID) -> list[WelcomeMessageEntity]:
        raise NotImplementedError

    async def get_welcome_message(self, welcome_message_uuid: UUID) -> WelcomeMessageEntity:
        raise NotImplementedError

    async def get_welcome_messages_count(self, object_uuid: UUID) -> int:
        raise NotImplementedError

    async def delete_welcome_message(self, welcome_message_uuid: UUID) -> None:
        raise NotImplementedError

    async def save_welcome_message(
        self,
        welcome_message: WelcomeMessageEntity,
    ) -> WelcomeMessageEntity:
        raise NotImplementedError

    async def edit_message_text(self, welcome_message_uuid: UUID, text: str) -> None:
        raise NotImplementedError

    async def edit_message_media(self, welcome_message_uuid: UUID, media_id: str) -> None:
        raise NotImplementedError
