import logging
from datetime import datetime

from aiogram import Router, types
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters.exception import ExceptionTypeFilter
from punq import Container

from catalog_bot.application.interactors.tap_client.user_block_bot import UserBlockBot
from catalog_bot.domain.exceptions.bot import BotNotFound

router = Router()

logger = logging.getLogger(__name__)


@router.errors(ExceptionTypeFilter(BotNotFound))
async def handle_bot_not_found_error(
    event: types.ErrorEvent,
) -> None:
    logger.error(
        f'Бот с айди: {event.update.bot.id} не был зарегистрирован. '
        f'Время по utc: {datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")}',
    )
    await event.update.message.answer(
        'Бот не был зарегистрирован, обратитесь к администратору',
    )


@router.errors(ExceptionTypeFilter(TelegramForbiddenError))
async def handle_user_block_bot(
    event: types.ErrorEvent,
    container: Container,
) -> None:
    user_block_bot = container.resolve(UserBlockBot)
    if event.exception.message == 'Forbidden: bot was blocked by the user':
        await user_block_bot.execute(
            bot_id=event.update.bot.id,
            user_id=event.event.update.message.from_user.id,
        )


@router.errors()
async def handle_unexpected_error(
    event: types.ErrorEvent,
) -> None:
    logger.error(
        event.exception,
        exc_info=True,
    )
    if event.update.message:
        await event.update.message.answer(
            'Возникли неожиданные проблемы, обратитесь к администратуору',
        )
