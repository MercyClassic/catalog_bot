from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class BotAdmin(UUIDPKModel, models.Model):
    telegram_id = models.BigIntegerField('Телеграм айди админа')
    bot = models.ForeignKey(
        'catalog_bot.Bot',
        on_delete=models.CASCADE,
        related_name='admins',
    )

    class Meta:
        db_table = 'catalog_bot_admin'
        verbose_name = 'Админ каталог бота'
        verbose_name_plural = 'Админы каталог ботов'

    def __str__(self) -> str:
        return f'Admin telegram id: {self.telegram_id}, bot uuid: {self.bot_id}'
