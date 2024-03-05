from catalog_bot.domain.entities.newsletter import PeriodicNewsletterEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetPeriodicNewsletters:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        bot_id: int,
    ) -> list[PeriodicNewsletterEntity]:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        newsletters = await self.uow.newsletter_repo.get_periodic_newsletters(bot_uuid=bot.uuid)
        return newsletters
