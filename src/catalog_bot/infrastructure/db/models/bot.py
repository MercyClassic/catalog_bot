from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class Bot(UUIDPKModel, models.Model):
    telegram_owner_id = models.BigIntegerField('Телеграм айди владельца')
    telegram_bot_id = models.BigIntegerField('Телеграм айди бота')
    token = models.CharField('Токен бота', max_length=200, unique=True)
    title = models.CharField(
        'Название бота',
        max_length=200,
        blank=True,
        null=True,
    )
    text_menu = models.CharField('Текст меню', max_length=255)
    media_menu = models.CharField(
        'Медиа меню',
        max_length=300,
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'catalog_bot_bot'
        verbose_name = 'Каталог бот'
        verbose_name_plural = 'Каталог боты'

    def __str__(self) -> str:
        return (
            f'Telegram bot id:{self.telegram_bot_id}, '
            f'telegram owner id: {self.telegram_owner_id}'
        )
