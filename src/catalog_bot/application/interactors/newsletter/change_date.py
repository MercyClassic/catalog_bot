from datetime import datetime
from uuid import UUID

import pytz

from catalog_bot.domain.exceptions.newsletter import WrongTime
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class ChangePeriodicNewsletterDate:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        newsletter_uuid: UUID,
        date: datetime,
    ) -> None:
        if date < datetime.now(tz=pytz.timezone('Europe/Moscow')):
            raise WrongTime
        await self.uow.newsletter_repo.change_periodic_newsletter_date(
            newsletter_uuid=newsletter_uuid,
            date=date,
        )
