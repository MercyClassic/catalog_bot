from django.db import transaction

from catalog_bot.infrastructure.db.repositories.bot import BotRepository
from catalog_bot.infrastructure.db.repositories.catalog.category import (
    CategoryRepository,
)
from catalog_bot.infrastructure.db.repositories.catalog.channel import ChannelRepository
from catalog_bot.infrastructure.db.repositories.newsletter import NewsletterRepository
from catalog_bot.infrastructure.db.repositories.statistics import StatisticsRepository
from catalog_bot.infrastructure.db.repositories.tap_client import TapClientRepository
from catalog_bot.infrastructure.db.repositories.welcome_message import (
    WelcomeMessageRepository,
)


class UoW:
    def __init__(self) -> None:
        self.bot_repo = BotRepository()
        self.category_repo = CategoryRepository()
        self.channel_repo = ChannelRepository()
        self.statistics_repo = StatisticsRepository()
        self.tap_client_repo = TapClientRepository()
        self.newsletter_repo = NewsletterRepository()
        self.welcome_message_repo = WelcomeMessageRepository()

    async def start_transaction(self) -> None:
        transaction.atomic()

    async def commit(self) -> None:
        transaction.commit()
