# Generated by Django 4.2.10 on 2024-02-21 21:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog_bot", "0006_alter_bot_options_alter_botadmin_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bot",
            old_name="media_main_menu",
            new_name="media_menu",
        ),
        migrations.RenameField(
            model_name="bot",
            old_name="text_main_menu",
            new_name="text_menu",
        ),
    ]