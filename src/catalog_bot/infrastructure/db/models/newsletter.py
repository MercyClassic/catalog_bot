from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class PeriodicNewsletter(UUIDPKModel, models.Model):
    title = models.CharField(max_length=255)
    message_id = models.BigIntegerField()
    from_chat_id = models.BigIntegerField()
    started_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    bot = models.ForeignKey(
        'catalog_bot.Bot',
        on_delete=models.CASCADE,
        related_name='periodic_newsletters',
    )

    class Meta:
        db_table = 'catalog_bot_periodic_newsletter'
        unique_together = ('title', 'bot')

    def __str__(self) -> str:
        return f'Periodic newsletter: {self.title}'
