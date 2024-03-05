from uuid import UUID

from catalog_bot.domain.entities.bot import AdminEntity, BotEntity, MenuEntity


class BotService:
    def create_admin(
        self,
        telegram_id: int,
        bot_uuid: UUID,
    ) -> AdminEntity:
        return AdminEntity(
            uuid=None,
            telegram_id=telegram_id,
            bot_uuid=bot_uuid,
        )

    def create_menu(
        self,
        bot: BotEntity,
    ) -> MenuEntity:
        return MenuEntity(
            bot_uuid=bot.uuid,
            text=bot.text_menu,
            media=bot.media_menu,
        )
