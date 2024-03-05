from uuid import UUID

from asgiref.sync import sync_to_async

from catalog_bot.infrastructure.db.models import Bot, BotAdmin


class CatalogBotRepository:
    async def save_catalog_bot(
        self,
        title: str,
        bot_token: str,
        telegram_owner_id: int,
        telegram_bot_id: int,
    ) -> UUID:
        bot = await Bot.objects.acreate(
            telegram_owner_id=telegram_owner_id,
            telegram_bot_id=telegram_bot_id,
            title=title,
            text_menu=title,
            token=bot_token,
        )
        await BotAdmin.objects.acreate(bot_id=bot.uuid, telegram_id=telegram_owner_id)
        return bot.uuid

    async def get_bots_by_telegram_owner_id(
        self,
        telegram_owner_id: int,
    ) -> list[Bot]:
        return await sync_to_async(list)(Bot.objects.filter(telegram_owner_id=telegram_owner_id))

    async def get_bot_by_uuid(
        self,
        catalog_bot_uuid: UUID,
    ) -> Bot:
        return await Bot.objects.aget(uuid=catalog_bot_uuid)
