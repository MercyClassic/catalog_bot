from django.contrib import admin

from catalog_bot.infrastructure.db.models import Bot, BotAdmin, TapClient


class BotInAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    list_display = ('uuid', 'telegram_owner_id', 'telegram_bot_id')
    list_display_links = ('uuid', 'telegram_owner_id', 'telegram_bot_id')
    search_fields = ('telegram_owner_id', 'telegram_bot_id', 'text_main_menu')


class BotAdminInAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    list_display = (
        'uuid',
        'telegram_id',
    )
    list_display_links = (
        'uuid',
        'telegram_id',
    )
    search_fields = ('telegram_id',)


class TapClientInAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'telegram_id', 'joined_at')
    list_display = (
        'uuid',
        'telegram_id',
    )
    list_display_links = (
        'uuid',
        'telegram_id',
    )
    search_fields = ('telegram_id',)


admin.site.register(Bot, BotInAdmin)
admin.site.register(BotAdmin, BotAdminInAdmin)
admin.site.register(TapClient, TapClientInAdmin)
