from typing import Protocol
from uuid import UUID

from catalog_bot.domain.entities.bot import AdminEntity, BotEntity


class BotRepositoryInterface(Protocol):
    async def get_bot_by_id(self, telegram_bot_id: int) -> BotEntity:
        raise NotImplementedError

    async def change_text_menu(
        self,
        text: str,
        bot_uuid: UUID,
    ) -> None:
        raise NotImplementedError

    async def change_media_menu(
        self,
        file_id: str,
        bot_uuid: UUID,
    ) -> None:
        raise NotImplementedError

    async def save_admin(self, admin: AdminEntity) -> None:
        raise NotImplementedError

    async def get_admins(self, bot_uuid: UUID) -> list[AdminEntity]:
        raise NotImplementedError

    async def is_admin_exists(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> bool:
        raise NotImplementedError

    async def delete_admin(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> None:
        raise NotImplementedError
