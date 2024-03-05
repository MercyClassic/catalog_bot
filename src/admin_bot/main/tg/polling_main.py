import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from admin_bot.main.di.container import get_container
from admin_bot.main.tg.middlewares.dependency import DependencyMiddleware
from admin_bot.main.tg.middlewares.is_admin import IsAdminMiddleware
from admin_bot.presentators.routers import start_router


async def main() -> None:
    bot = Bot(os.environ['bot_token'])
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    container = get_container()
    dp.update.outer_middleware(DependencyMiddleware(container))
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True))
    is_admin_middleware = IsAdminMiddleware()

    start_router.message.middleware(is_admin_middleware)

    dp.include_router(start_router)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
