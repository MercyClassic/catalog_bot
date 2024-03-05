import os

from aiogram import Bot


async def start_catalog_bot(bot_token: str) -> None:
    bot = Bot(bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=f'{os.environ["NGINX_URI"]}/catalog_bot/webhook/{bot.id}',
        secret_token=os.environ['WEBHOOK_SECRET'],
    )
    await bot.session.close()


async def stop_catalog_bot(bot_token: str) -> None:
    bot = Bot(bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
