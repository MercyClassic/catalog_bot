from django.urls import path

from . import views

urlpatterns = [
    path('webhook/<bot_id>', views.CatalogBotAPIView.as_view(), name='catalog_bot_webhook'),
]
