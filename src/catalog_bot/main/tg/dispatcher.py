import json

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from django.http import HttpRequest

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

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def startup_dispatcher() -> None:
    container = get_container()
    dp.update.outer_middleware(DependencyMiddleware(container))
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True))

    catalog_bot_is_admin_middleware = IsAdminMiddleware()
    main_admin_router.message.middleware(catalog_bot_is_admin_middleware)
    admin_router.message.middleware(catalog_bot_is_admin_middleware)
    statistic_router.message.middleware(catalog_bot_is_admin_middleware)
    newsletter_router.message.middleware(catalog_bot_is_admin_middleware)
    menu_router.message.middleware(catalog_bot_is_admin_middleware)
    cancel_state_router.message.middleware(catalog_bot_is_admin_middleware)

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


async def proceed_update(
    request: HttpRequest,
    bot_token: str,
):
    bot = Bot(bot_token)
    update = Update.model_validate(json.loads(request.body), context={'bot': bot})
    await dp.feed_update(bot, update)
    await bot.session.close()
