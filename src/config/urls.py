from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'catalog_bot/',
        include(
            ('catalog_bot.presentators.api.urls', 'catalog_bot'),
            namespace='catalog_bot',
        ),
    ),
    path(
        'admin_bot/',
        include(
            ('admin_bot.presentators.api.urls', 'admin_bot'),
            namespace='admin_bot',
        ),
    ),
]
