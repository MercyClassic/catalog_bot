from aiogram import Bot


async def get_catalog_bot_status(bot_token: str) -> bool:
    bot = Bot(bot_token)
    info = await bot.get_webhook_info()
    await bot.session.close()
    return bool(info.url)  # todo: replace
