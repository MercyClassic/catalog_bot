# Generated by Django 5.0.2 on 2024-02-17 16:56

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('telegram_owner_id', models.BigIntegerField()),
                ('telegram_bot_id', models.BigIntegerField()),
                ('text_main_menu', models.CharField(max_length=255)),
                ('media_main_menu', models.ImageField(upload_to='catalog_bot_images/')),
            ],
            options={
                'db_table': 'catalog_bot_bot',
            },
        ),
        migrations.CreateModel(
            name='TapClient',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('telegram_id', models.BigIntegerField(editable=False, unique=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'catalog_bot_tap_client',
            },
        ),
        migrations.CreateModel(
            name='BotAdmin',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('telegram_id', models.BigIntegerField()),
                (
                    'bot',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='admins',
                        to='catalog_bot.bot',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_admin',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('title', models.CharField(max_length=255)),
                (
                    'bot',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='categories',
                        to='catalog_bot.bot',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_category',
                'unique_together': {('bot', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('users_count', models.BigIntegerField(default=0)),
                ('in_the_block_count', models.BigIntegerField(default=0)),
                (
                    'bot',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='statistic',
                        to='catalog_bot.bot',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_statistic',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('title', models.CharField(max_length=255)),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subcategories',
                        to='catalog_bot.category',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_subcategory',
                'unique_together': {('category', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ('chat_id', models.BigIntegerField(editable=False, unique=True)),
                (
                    'subcategory',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='channels',
                        to='catalog_bot.subcategory',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_channel',
                'unique_together': {('chat_id', 'subcategory')},
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    'channel',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog_bot.channel',
                    ),
                ),
                (
                    'tap_client',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog_bot.tapclient',
                    ),
                ),
            ],
            options={
                'db_table': 'catalog_bot_subscription',
            },
        ),
    ]
