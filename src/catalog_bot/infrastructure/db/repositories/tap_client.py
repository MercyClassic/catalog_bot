from uuid import UUID

from asgiref.sync import sync_to_async

from catalog_bot.domain.entities.tap_client import TapClientEntity
from catalog_bot.infrastructure.db.models.tap_client import TapClient


class TapClientRepository:
    async def save_tap_client(
        self,
        telegram_id: int,
        bot_uuid: UUID,
        telegram_username: str | None,
    ) -> TapClientEntity:
        tap_client_db = TapClient(
            telegram_id=telegram_id,
            bot_id=bot_uuid,
            telegram_username=telegram_username,
        )
        await tap_client_db.asave()
        return TapClientEntity(
            uuid=tap_client_db.uuid,
            telegram_id=tap_client_db.telegram_id,
            bot_uuid=tap_client_db.bot_id,
            telegram_username=tap_client_db.telegram_username,
            joined_at=tap_client_db.joined_at,
        )

    async def get_tap_client_by_id_or_username(
        self,
        telegram_field: str | int,
        bot_uuid: UUID,
    ) -> TapClientEntity | None:
        try:
            int(telegram_field)
        except ValueError:
            search_params = {'telegram_username': telegram_field}
        else:
            search_params = {'telegram_id': telegram_field}

        try:
            tap_client = await TapClient.objects.aget(bot_id=bot_uuid, **search_params)
        except TapClient.DoesNotExist:
            return None
        return TapClientEntity(
            uuid=tap_client.uuid,
            telegram_id=tap_client.telegram_id,
            bot_uuid=tap_client.bot_id,
            telegram_username=tap_client.telegram_username,
            joined_at=tap_client.joined_at,
        )

    async def get_tap_clients(self, bot_uuid: UUID) -> list[TapClientEntity]:
        clients = await sync_to_async(list)(TapClient.objects.filter(bot_id=bot_uuid))
        return [
            TapClientEntity(
                uuid=client.uuid,
                telegram_id=client.telegram_id,
                bot_uuid=client.bot_id,
                telegram_username=client.telegram_username,
                joined_at=client.joined_at,
            )
            for client in clients
        ]

    async def is_tap_client_exist(self, telegram_id: int, bot_uuid: UUID) -> bool:
        return await TapClient.objects.filter(telegram_id=telegram_id, bot_id=bot_uuid).aexists()

    async def set_user_block_bot(self, bot_uuid: UUID, user_id: int) -> None:
        await TapClient.objects.filter(bot_id=bot_uuid, telegram_id=user_id).aupdate(is_block=True)
