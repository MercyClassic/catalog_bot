from django.contrib import admin

from admin_bot.db.models.admin import Admin


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


admin.site.register(Admin, BotAdminInAdmin)
