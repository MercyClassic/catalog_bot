from catalog_bot.domain.exceptions.bot import BotNotFound
from catalog_bot.domain.exceptions.tap_client import TapClientAlreadyExist
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class SaveTapClient:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow

    async def execute(
        self,
        telegram_user_id: int,
        bot_id: int,
        telegram_username: str | None,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound
        tap_client_exists = await self.uow.tap_client_repo.is_tap_client_exist(
            telegram_user_id,
            bot.uuid,
        )
        if tap_client_exists:
            raise TapClientAlreadyExist
        await self.uow.tap_client_repo.save_tap_client(
            telegram_id=telegram_user_id,
            bot_uuid=bot.uuid,
            telegram_username=telegram_username,
        )
