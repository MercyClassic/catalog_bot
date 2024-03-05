from uuid import UUID

from django.db.models import Case, Count, Q, When
from django.utils import timezone

from catalog_bot.domain.entities.statistic import StatisticEntity
from catalog_bot.infrastructure.db.models import TapClient


class StatisticsRepository:
    async def get_statistic(self, bot_uuid: UUID) -> StatisticEntity | None:
        query = (
            TapClient.objects.filter(bot_id=bot_uuid)
            .annotate(
                users_count=Count(
                    'is_block',
                    filter=Q(is_block=False),
                ),
                in_the_block_count=Count(
                    'is_block',
                    filter=Q(is_block=True),
                ),
                new_this_month=Count(
                    Case(
                        When(
                            joined_at__month=timezone.now().month,
                            joined_at__year=timezone.now().year,
                            then=1,
                        ),
                        default=None,
                    ),
                ),
                new_this_day=Count(
                    Case(
                        When(
                            joined_at__date=timezone.now().date(),
                            then=1,
                        ),
                        default=None,
                    ),
                ),
            )
            .only('uuid')
            .afirst()
        )
        statistic = await query
        if not statistic:
            return StatisticEntity(0, 0, 0, 0)
        return StatisticEntity(
            users_count=statistic.users_count,
            in_the_block_count=statistic.in_the_block_count,
            new_this_month=statistic.new_this_month,
            new_this_day=statistic.new_this_day,
        )
