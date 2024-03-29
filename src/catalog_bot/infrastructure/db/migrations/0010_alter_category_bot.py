# Generated by Django 4.2.10 on 2024-02-22 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog_bot", "0009_alter_category_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="bot",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="categories",
                to="catalog_bot.bot",
            ),
        ),
    ]
