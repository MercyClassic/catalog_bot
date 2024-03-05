from aiogram import Bot, F, Router, types
from punq import Container

from catalog_bot.application.interactors.statistic.get_statistic import GetStatistic

router = Router()


@router.message(F.text == '📊 Статистика')
async def get_statistic_handler(
    message: types.Message,
    bot: Bot,
    container: Container,
) -> None:
    get_statistic = container.resolve(GetStatistic)

    statistic = await get_statistic.execute(bot_id=bot.id)

    text = (
        '📊 Статистика бота:\n\n'
        f'Всего пользователей: {statistic.users_count}\n'
        f'Заблокировали бота: {statistic.in_the_block_count}\n'
        f'Новых сегодня: {statistic.new_this_day}\n'
        f'За месяц: {statistic.new_this_month}\n'
    )

    await bot.send_message(
        message.from_user.id,
        text,
    )
