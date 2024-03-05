from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types
from punq import Container


class DependencyMiddleware(BaseMiddleware):
    def __init__(
        self,
        container: Container,
    ) -> None:
        self.container = container

    async def __call__(
        self,
        handler: Callable[..., Any],
        event: types.TelegramObject,
        data: Dict,
    ) -> None:
        data['container'] = self.container
        await handler(event, data)
