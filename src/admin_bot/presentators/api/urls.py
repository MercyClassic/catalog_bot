from django.urls import path

from . import views

urlpatterns = [
    path('webhook', views.AdminBotAPIView.as_view(), name='admin_bot_webhook'),
]
