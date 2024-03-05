from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.bot import AdminEntity


class BotServiceInterface(Protocol):
    def create_admin(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> AdminEntity:
        raise NotImplementedError
