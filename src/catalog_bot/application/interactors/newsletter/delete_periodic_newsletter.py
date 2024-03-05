from uuid import UUID

from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class DeletePeriodicNewsletter:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        newsletter_uuid: UUID,
    ) -> None:
        await self.uow.newsletter_repo.delete_periodic_newsletter(newsletter_uuid)
