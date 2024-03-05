from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class Category(UUIDPKModel, models.Model):
    bot = models.ForeignKey(
        'catalog_bot.Bot',
        on_delete=models.DO_NOTHING,
        related_name='categories',
    )
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    image = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'catalog_bot_category'
        unique_together = ('bot', 'title')

    def __str__(self) -> str:
        return f'Category id: {self.pk}'


class Channel(UUIDPKModel, models.Model):
    bot = models.ForeignKey(
        'catalog_bot.Bot',
        on_delete=models.DO_NOTHING,
        related_name='channels',
    )
    chat_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255, blank=True, null=True)
    auto_commit = models.BooleanField(default=False)
    category = models.ForeignKey(
        'catalog_bot.Category',
        on_delete=models.CASCADE,
        related_name='channels',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'catalog_bot_channel'
        unique_together = ('chat_id', 'category')

    def __str__(self) -> str:
        return f'Channel id: {self.chat_id}'
