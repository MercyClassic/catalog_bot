from catalog_bot.domain.entities.statistic import StatisticEntity
from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class GetStatistic:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        bot_id: int,
    ) -> StatisticEntity:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        statistic = await self.uow.statistics_repo.get_statistic(bot_uuid=bot.uuid)
        return statistic
