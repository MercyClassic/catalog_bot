from asgiref.sync import async_to_sync
from django.apps import AppConfig


class AdminBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_bot'
    verbose_name = 'Админ бот'

    def ready(self):
        from admin_bot.main.tg.dispatcher import startup_dispatcher

        async_to_sync(startup_dispatcher)()
