from typing import Protocol

from catalog_bot.infrastructure.db.interfaces.repositories.bot import (
    BotRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.catalog.category import (
    CategoryRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.catalog.channel import (
    ChannelRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.newsletter import (
    NewsletterRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.statistics import (
    StatisticsRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.tap_client import (
    TapClientRepositoryInterface,
)
from catalog_bot.infrastructure.db.interfaces.repositories.welcome_message import (
    WelcomeMessageRepositoryInterface,
)


class UoWInterface(Protocol):
    bot_repo: BotRepositoryInterface
    category_repo: CategoryRepositoryInterface
    channel_repo: ChannelRepositoryInterface
    statistics_repo: StatisticsRepositoryInterface
    tap_client_repo: TapClientRepositoryInterface
    newsletter_repo: NewsletterRepositoryInterface
    welcome_message_repo: WelcomeMessageRepositoryInterface

    async def start_transaction(self) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError
