from admin_bot.db.repositories.admin import AdminRepository


class AdminService:
    def __init__(self, admin_repo: AdminRepository) -> None:
        self.admin_repo = admin_repo

    async def is_admin(self, telegram_id: int) -> bool:
        return await self.admin_repo.is_admin(telegram_id=telegram_id)

    async def is_catalog_bot_admin(self, telegram_id: int) -> bool:
        return await self.admin_repo.is_catalog_bot_admin(telegram_id=telegram_id)
