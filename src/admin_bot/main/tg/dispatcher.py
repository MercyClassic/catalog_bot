import json
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from django.http import HttpRequest

from admin_bot.main.di.container import get_container
from admin_bot.main.tg.middlewares.dependency import DependencyMiddleware
from admin_bot.main.tg.middlewares.is_admin import IsAdminMiddleware
from admin_bot.presentators.routers import start_router

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_admin_bot_startup() -> None:
    bot = Bot(os.environ['bot_token'])
    await bot.set_webhook(
        drop_pending_updates=True,
        url=f'{os.environ["NGINX_URI"]}/admin_bot/webhook',
        secret_token=os.environ['WEBHOOK_SECRET'],
    )
    await bot.session.close()


async def startup_dispatcher() -> None:
    await on_admin_bot_startup()

    container = get_container()
    dp.update.outer_middleware(DependencyMiddleware(container))
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True))

    admin_bot_is_admin_middleware = IsAdminMiddleware()
    start_router.message.middleware(admin_bot_is_admin_middleware)
    dp.include_router(start_router)

    setup_dialogs(dp)


async def proceed_update(
    request: HttpRequest,
):
    bot = Bot(os.environ['bot_token'])
    update = Update.model_validate(json.loads(request.body), context={'bot': bot})
    await dp.feed_update(bot, update)
    await bot.session.close()
