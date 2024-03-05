from django.db import models

from admin_bot.db.models.base import UUIDPKModel


class Admin(UUIDPKModel, models.Model):
    telegram_id = models.BigIntegerField()

    class Meta:
        db_table = 'admin_bot_admin'
