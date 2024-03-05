from asgiref.sync import async_to_sync
from django.apps import AppConfig


class CatalogBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog_bot'
    verbose_name = 'Каталог бот'

    def ready(self):
        from catalog_bot.main.tg.dispatcher import startup_dispatcher

        async_to_sync(startup_dispatcher)()
