from uuid import UUID

from asgiref.sync import sync_to_async

from catalog_bot.domain.entities.bot import AdminEntity, BotEntity
from catalog_bot.infrastructure.db.models import Bot, BotAdmin


class BotRepository:
    async def get_bot_by_id(self, telegram_bot_id: int) -> BotEntity | None:
        try:
            bot_db = await Bot.objects.aget(telegram_bot_id=telegram_bot_id)
        except Bot.DoesNotExist:
            return None
        return BotEntity(
            uuid=bot_db.uuid,
            telegram_owner_id=bot_db.telegram_owner_id,
            telegram_bot_id=bot_db.telegram_bot_id,
            text_menu=bot_db.text_menu,
            media_menu=bot_db.media_menu,
        )

    async def change_text_menu(
        self,
        text: str,
        bot_uuid: UUID,
    ) -> None:
        await Bot.objects.filter(uuid=bot_uuid).aupdate(text_menu=text)

    async def change_media_menu(
        self,
        file_id: str,
        bot_uuid: UUID,
    ) -> None:
        await Bot.objects.filter(uuid=bot_uuid).aupdate(media_menu=file_id)

    async def save_admin(self, admin: AdminEntity) -> None:
        admin_db = BotAdmin(
            telegram_id=admin.telegram_id,
            bot_id=admin.bot_uuid,
        )
        await admin_db.asave()

    async def get_admins(self, bot_uuid: UUID) -> list[AdminEntity]:
        query = await sync_to_async(list)(BotAdmin.objects.filter(bot_id=bot_uuid).all())
        return [
            AdminEntity(
                uuid=admin.uuid,
                telegram_id=admin.telegram_id,
                bot_uuid=admin.bot_id,
            )
            for admin in query
        ]

    async def is_admin_exists(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> bool:
        query = BotAdmin.objects.filter(
            telegram_id=telegram_id,
            bot_id=bot_uuid,
        ).aexists()
        return await query

    async def delete_admin(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> None:
        await BotAdmin.objects.filter(
            telegram_id=telegram_id,
            bot_id=bot_uuid,
        ).adelete()
