import uuid

from django.db import models


class UUIDPKModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        editable=False,
    )

    class Meta:
        abstract = True
