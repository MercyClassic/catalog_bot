import asyncio
from datetime import datetime

import pytz
from aiogram import Bot as TGBot
from celery import shared_task
from django.db.models import Prefetch

from catalog_bot.infrastructure.db.models import Bot, PeriodicNewsletter, TapClient


async def _send(
    bot: TGBot,
    newsletter: PeriodicNewsletter,
    client: TapClient,
) -> None:
    await bot.copy_message(client.telegram_id, newsletter.from_chat_id, newsletter.message_id)


@shared_task
def process_send_periodic_newsletter():
    date = datetime.now(tz=pytz.timezone('Europe/Moscow'))
    date = date.replace(second=0, microsecond=0)
    bots = Bot.objects.all().prefetch_related(
        Prefetch(
            'periodic_newsletters',
            PeriodicNewsletter.objects.filter(
                status=True,
                started_at__date__gte=date.date(),
                started_at__hour=date.hour,
                started_at__minute=date.minute,
            ),
        ),
        'clients',
    )
    loop = asyncio.get_event_loop_policy().new_event_loop()
    tasks = []
    tg_bots = []
    for bot in bots:
        tg_bot = TGBot(token=bot.token)
        tg_bots.append(tg_bot)
        for newsletter in bot.periodic_newsletters.all():
            for client in bot.clients.all():
                tasks.append(
                    loop.create_task(
                        _send(
                            bot=tg_bot,
                            newsletter=newsletter,
                            client=client,
                        ),
                    ),
                )
    if tasks:
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    loop.close()
