from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.tap_client import TapClientEntity


class TapClientRepositoryInterface(Protocol):
    async def save_tap_client(
        self,
        telegram_id: int,
        bot_uuid: UUID,
        telegram_username: str | None,
    ) -> TapClientEntity:
        raise NotImplementedError

    async def get_tap_client_by_id_or_username(
        self,
        telegram_id: str | int,
        bot_uuid: UUID,
    ) -> TapClientEntity | None:
        raise NotImplementedError

    async def get_tap_clients(self, bot_uuid: UUID) -> list[TapClientEntity]:
        raise NotImplementedError

    async def is_tap_client_exist(self, telegram_id: int, bot_uuid: UUID) -> bool:
        raise NotImplementedError

    async def set_user_block_bot(self, bot_uuid: UUID, user_id: int) -> None:
        raise NotImplementedError
