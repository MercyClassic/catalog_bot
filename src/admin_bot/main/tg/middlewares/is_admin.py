from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from admin_bot.application.services.admin import AdminService


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[..., Any],
        event: types.TelegramObject,
        data: Dict,
    ) -> None:
        bot = data['bot']
        container = data['container']

        user_id = event.from_user.id
        admin_service = container.resolve(AdminService)

        if await admin_service.is_admin(telegram_id=user_id):
            await handler(event, data)
        else:
            await bot.send_message(
                user_id,
                'Это команда доступна только администратору',
            )
