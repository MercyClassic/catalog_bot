# Generated by Django 4.2.10 on 2024-02-21 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog_bot",
            "0003_alter_bot_media_main_menu_alter_subscription_channel_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="channel",
        ),
        migrations.AddField(
            model_name="category",
            name="description",
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, default=None, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="channel",
            name="link",
            field=models.URLField(default="default", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="channel",
            name="title",
            field=models.CharField(default="default", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subcategory",
            name="description",
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="image",
            field=models.ImageField(blank=True, default=None, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="subscription",
            name="bot",
            field=models.ForeignKey(
                default="809cf698-2922-4bbb-ae91-adefc864d659",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bots",
                to="catalog_bot.bot",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bot",
            name="media_main_menu",
            field=models.ImageField(blank=True, default=None, null=True, upload_to=""),
        ),
    ]