from asgiref.sync import async_to_sync
from django.http import HttpResponse
from rest_framework.views import APIView

from catalog_bot.infrastructure.db.models import Bot
from catalog_bot.main.tg.dispatcher import proceed_update


class CatalogBotAPIView(APIView):
    def post(self, request, bot_id: int, **kwargs) -> HttpResponse:
        bot = Bot.objects.get(telegram_bot_id=bot_id)  # todo: move to repo/service
        async_to_sync(proceed_update)(request, bot_token=bot.token)
        return HttpResponse(status=200)
