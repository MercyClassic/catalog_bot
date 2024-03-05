from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from catalog_bot.application.interactors.admin.is_admin import IsAdmin


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
        bot_id = bot.id
        is_admin = container.resolve(IsAdmin)

        if await is_admin.execute(
            user_id=user_id,
            bot_id=bot_id,
        ):
            await handler(event, data)
        else:
            await bot.send_message(
                user_id,
                'Это команда доступна только администратору',
            )
