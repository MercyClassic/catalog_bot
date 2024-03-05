from catalog_bot.domain.exceptions.bot import AdminAlreadyExist, BotNotFound
from catalog_bot.domain.exceptions.tap_client import TapClientNotFound
from catalog_bot.domain.services.bot import BotService
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface


class CreateAdmin:
    def __init__(
        self,
        uow: UoWInterface,
    ) -> None:
        self.uow = uow
        self.bot_service = BotService()

    async def execute(
        self,
        telegram_field: str | int,
        bot_id: int,
    ) -> None:
        bot = await self.uow.bot_repo.get_bot_by_id(bot_id)
        if not bot:
            raise BotNotFound

        tap_client = await self.uow.tap_client_repo.get_tap_client_by_id_or_username(
            telegram_field,
            bot.uuid,
        )
        if not tap_client:
            raise TapClientNotFound

        if await self.uow.bot_repo.is_admin_exists(
            telegram_id=tap_client.telegram_id,
            bot_uuid=bot.uuid,
        ):
            raise AdminAlreadyExist

        admin = self.bot_service.create_admin(
            telegram_id=tap_client.telegram_id,
            bot_uuid=bot.uuid,
        )
        await self.uow.bot_repo.save_admin(admin)
