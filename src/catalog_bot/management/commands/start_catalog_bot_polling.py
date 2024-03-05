import asyncio
import logging
import sys

from django.core.management.base import BaseCommand

from catalog_bot.main.tg.polling_main import main


class Command(BaseCommand):
    help = 'Start catalog bot'

    def handle(self, *args: tuple, **options: dict) -> None:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
