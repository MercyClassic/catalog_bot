from django.core.management.base import BaseCommand

from admin_bot.db.models import Admin


class Command(BaseCommand):
    help = 'Create superuser for admin bot'

    def handle(self, *args: tuple, **options: dict) -> None:
        telegram_owner_id = int(input('Введите telegram ID владельца: '))
        Admin.objects.create(telegram_id=telegram_owner_id)
