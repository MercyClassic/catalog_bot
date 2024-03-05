from catalog_bot.domain.exceptions.bot import (
    AdminNotFound,
    BotNotFound,
    CantDeleteBotOwner,
    CantDeleteItself,
)
from catalog_bot.domain.exceptions.tap_client import TapClientNotFound
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class DeleteAdmin:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        executor_id: int,
        telegram_field: int | str,
        bot_id: int,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        if bot.telegram_owner_id == telegram_field:
            raise CantDeleteBotOwner

        tap_client = await self.uow.tap_client_repo.get_tap_client_by_id_or_username(
            telegram_field,
            bot.uuid,
        )
        if not tap_client:
            raise TapClientNotFound
        if executor_id == tap_client.telegram_id:
            raise CantDeleteItself

        admin_exists = await self.uow.bot_repo.is_admin_exists(
            telegram_id=tap_client.telegram_id,
            bot_uuid=bot.uuid,
        )
        if not admin_exists:
            raise AdminNotFound

        await self.uow.bot_repo.delete_admin(
            telegram_id=tap_client.telegram_id,
            bot_uuid=bot.uuid,
        )
