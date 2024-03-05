from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class TapClient(UUIDPKModel, models.Model):
    telegram_id = models.BigIntegerField(
        'Телеграм айди',
        unique=True,
        editable=False,
    )
    telegram_username = models.CharField(
        'Телеграм @username',
        max_length=255,
        blank=True,
        null=True,
    )
    bot = models.ForeignKey(
        'catalog_bot.Bot',
        on_delete=models.CASCADE,
        related_name='clients',
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_block = models.BooleanField(default=False)

    class Meta:
        db_table = 'catalog_bot_tap_client'
        verbose_name = 'Клиенты каталог бота'
        verbose_name_plural = 'Клиенты каталог ботов'

    def __str__(self) -> str:
        return f'Tap client telegram id: {self.telegram_id}'
