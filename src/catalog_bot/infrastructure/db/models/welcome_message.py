import uuid

from django.db import models

from catalog_bot.infrastructure.db.models.base import UUIDPKModel


class WelcomeMessage(UUIDPKModel, models.Model):
    OWNER_CHOICES = (
        ('bot', 'bot'),
        ('channel', 'channel'),
    )
    object_id = models.UUIDField(default=uuid.uuid4)
    owner_type = models.CharField(max_length=7, choices=OWNER_CHOICES)
    text = models.CharField(max_length=500)
    media = models.CharField(max_length=255, blank=True, null=True)
    order = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_bot_welcome_message'


class Button(UUIDPKModel, models.Model):
    BUTTON_CHOICES = (
        ('inline', 'inline'),
        ('reply', 'reply'),
    )

    message = models.ForeignKey(
        'catalog_bot.WelcomeMessage',
        on_delete=models.CASCADE,
        related_name='buttons',
    )
    type = models.CharField(max_length=6, choices=BUTTON_CHOICES)
    text = models.CharField(max_length=50)

    class Meta:
        db_table = 'catalog_bot_welcome_message_button'
