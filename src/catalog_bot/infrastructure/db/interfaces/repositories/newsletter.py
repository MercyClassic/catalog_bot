from datetime import datetime
from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.newsletter import PeriodicNewsletterEntity


class NewsletterRepositoryInterface(Protocol):
    async def get_periodic_newsletters(self, bot_uuid: UUID) -> list[PeriodicNewsletterEntity]:
        raise NotImplementedError

    async def get_periodic_newsletter(
        self,
        bot_uuid: UUID,
        newsletter_uuid: UUID,
    ) -> PeriodicNewsletterEntity:
        raise NotImplementedError

    async def save_periodic_newsletter(
        self,
        title: str,
        message_id: int,
        from_chat_id: int,
        bot_uuid: UUID,
    ) -> UUID:
        raise NotImplementedError

    async def change_periodic_newsletter_status(self, newsletter_uuid: UUID) -> None:
        raise NotImplementedError

    async def change_periodic_newsletter_date(self, newsletter_uuid: UUID, date: datetime) -> None:
        raise NotImplementedError

    async def delete_periodic_newsletter(self, newsletter_uuid: UUID) -> None:
        raise NotImplementedError
