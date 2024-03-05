from datetime import datetime
from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models import F

from catalog_bot.domain.entities.newsletter import PeriodicNewsletterEntity
from catalog_bot.infrastructure.db.models import PeriodicNewsletter


class NewsletterRepository:
    def _serialize_newsletter(self, newsletter: PeriodicNewsletter) -> PeriodicNewsletterEntity:
        return PeriodicNewsletterEntity(
            uuid=newsletter.uuid,
            title=newsletter.title,
            message_id=newsletter.message_id,
            from_chat_id=newsletter.from_chat_id,
            started_at=newsletter.started_at,
            status=newsletter.status,
        )

    async def get_periodic_newsletters(self, bot_uuid: UUID) -> list[PeriodicNewsletterEntity]:
        newsletters = await sync_to_async(list)(PeriodicNewsletter.objects.filter(bot_id=bot_uuid))
        return [self._serialize_newsletter(newsletter) for newsletter in newsletters]

    async def get_periodic_newsletter(
        self,
        bot_uuid: UUID,
        newsletter_uuid: UUID,
    ) -> PeriodicNewsletterEntity:
        newsletter = await PeriodicNewsletter.objects.aget(uuid=newsletter_uuid, bot_id=bot_uuid)
        return self._serialize_newsletter(newsletter)

    async def save_periodic_newsletter(
        self,
        title: str,
        message_id: int,
        from_chat_id: int,
        bot_uuid: UUID,
    ) -> UUID:
        newsletter = PeriodicNewsletter(
            title=title,
            message_id=message_id,
            from_chat_id=from_chat_id,
            bot_id=bot_uuid,
        )
        await newsletter.asave()
        return newsletter.uuid

    async def change_periodic_newsletter_status(self, newsletter_uuid: UUID) -> None:
        await PeriodicNewsletter.objects.filter(uuid=newsletter_uuid).aupdate(status=~F('status'))

    async def change_periodic_newsletter_date(self, newsletter_uuid: UUID, date: datetime) -> None:
        await PeriodicNewsletter.objects.filter(uuid=newsletter_uuid).aupdate(started_at=date)

    async def delete_periodic_newsletter(self, newsletter_uuid: UUID) -> None:
        await PeriodicNewsletter.objects.filter(uuid=newsletter_uuid).adelete()
