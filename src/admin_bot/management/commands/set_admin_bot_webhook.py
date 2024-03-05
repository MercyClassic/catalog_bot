import os

from aiogram import Bot
from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand


async def on_admin_bot_startup() -> None:
    bot = Bot(os.environ['bot_token'])
    await bot.set_webhook(
        drop_pending_updates=True,
        url=f'{os.environ["NGINX_URI"]}/admin_bot/webhook',
        secret_token=os.environ['WEBHOOK_SECRET'],
    )
    await bot.session.close()


class Command(BaseCommand):
    help = 'Set admin bot webhook'

    def handle(self, *args: tuple, **options: dict) -> None:
        async_to_sync(on_admin_bot_startup)()
