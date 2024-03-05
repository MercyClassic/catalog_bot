from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.statistic import StatisticEntity


class StatisticsRepositoryInterface(Protocol):
    async def get_statistic(self, bot_uuid: UUID) -> StatisticEntity:
        raise NotImplementedError
