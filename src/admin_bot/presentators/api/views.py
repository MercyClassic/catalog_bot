from asgiref.sync import async_to_sync
from django.http import HttpResponse
from rest_framework.views import APIView

from admin_bot.main.tg.dispatcher import proceed_update


class AdminBotAPIView(APIView):
    def post(self, request, *args, **kwargs) -> HttpResponse:
        async_to_sync(proceed_update)(request)
        return HttpResponse(status=200)
