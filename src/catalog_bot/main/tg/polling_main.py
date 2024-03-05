import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from catalog_bot.main.di.container import get_container
from catalog_bot.main.tg.middlewares.dependency import DependencyMiddleware
from catalog_bot.main.tg.middlewares.is_admin import IsAdminMiddleware
from catalog_bot.presentators.tg.routers import (
    admin_router,
    cancel_state_router,
    catalog_router,
    error_router,
    join_channel_router,
    main_admin_router,
    menu_router,
    newsletter_router,
    statistic_router,
)


async def main() -> None:
    bot = Bot(os.environ['bot_token'])
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    container = get_container()
    dp.update.outer_middleware(DependencyMiddleware(container))
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True))
    is_admin_middleware = IsAdminMiddleware()

    main_admin_router.message.middleware(is_admin_middleware)
    admin_router.message.middleware(is_admin_middleware)
    statistic_router.message.middleware(is_admin_middleware)
    newsletter_router.message.middleware(is_admin_middleware)
    menu_router.message.middleware(is_admin_middleware)
    cancel_state_router.message.middleware(is_admin_middleware)

    dp.include_router(main_admin_router)
    dp.include_router(error_router)
    dp.include_router(cancel_state_router)
    dp.include_router(join_channel_router)
    dp.include_router(statistic_router)
    dp.include_router(catalog_router)
    dp.include_router(menu_router)
    dp.include_router(newsletter_router)
    dp.include_router(admin_router)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
