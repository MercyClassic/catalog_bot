# Generated by Django 4.2.10 on 2024-03-03 14:02

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("telegram_id", models.BigIntegerField()),
            ],
            options={
                "db_table": "admin_bot_admin",
            },
        ),
    ]
