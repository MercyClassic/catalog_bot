from admin_bot.db.models import Admin
from catalog_bot.infrastructure.db.models import BotAdmin


class AdminRepository:
    async def is_admin(self, telegram_id: int) -> bool:
        return await Admin.objects.filter(telegram_id=telegram_id).aexists()

    async def is_catalog_bot_admin(self, telegram_id: int) -> bool:
        return await BotAdmin.objects.filter(telegram_id=telegram_id).aexists()
