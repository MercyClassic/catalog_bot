import asyncio
from datetime import datetime, timedelta
from typing import Any

import pytz
from aiogram import types
from aiogram.exceptions import TelegramForbiddenError
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from catalog_bot.application.interactors.newsletter.change_date import (
    ChangePeriodicNewsletterDate,
)
from catalog_bot.application.interactors.newsletter.change_status import (
    ChangePeriodicNewsletterStatus,
)
from catalog_bot.application.interactors.newsletter.create_periodic_newsletter import (
    CreatePeriodicNewsletter,
)
from catalog_bot.application.interactors.newsletter.delete_periodic_newsletter import (
    DeletePeriodicNewsletter,
)
from catalog_bot.application.interactors.newsletter.get_periodic_newsletter import (
    GetPeriodicNewsletter,
)
from catalog_bot.application.interactors.newsletter.get_periodic_newsletters import (
    GetPeriodicNewsletters,
)
from catalog_bot.application.interactors.tap_client.get_clients import GetTapClients
from catalog_bot.application.tg.states.newsletter import NewsletterState
from catalog_bot.domain.entities.newsletter import PeriodicNewsletterEntity
from catalog_bot.domain.exceptions.newsletter import WrongTime


async def change_state_to_send_approve(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    await message.reply('Вы действительно хотите разослать это сообщение?')
    manager.dialog_data['message_id'] = message.message_id
    await manager.switch_to(NewsletterState.approve)


async def handle_default_newsletter_cancel(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    manager.dialog_data.update({'message_id': None})
    await manager.switch_to(NewsletterState.default)


async def handle_periodic_newsletter_cancel(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    manager.dialog_data.update({'message_id': None})
    await manager.switch_to(NewsletterState.periodic_list)


async def handle_default_newsletter_send(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    get_tap_clients = manager.middleware_data['container'].resolve(GetTapClients)
    tap_clients = await get_tap_clients.execute(bot.id)

    tasks = [
        asyncio.create_task(
            bot.copy_message(
                chat_id=tap_client.telegram_id,
                from_chat_id=callback.from_user.id,
                message_id=manager.dialog_data['message_id'],
            ),
        )
        for tap_client in tap_clients
    ]
    await bot.send_message(
        callback.from_user.id,
        '✅ Рассылка поставлена в очередь',
    )
    result = await asyncio.gather(*tasks, return_exceptions=True)
    blocked = len(tuple(filter(lambda task: isinstance(task, TelegramForbiddenError), result)))
    await bot.send_message(
        callback.from_user.id,
        '✅ Сообщение разослано!\n'
        f'Рассылку получили: {len(result)}\n'
        f'Из них заблокировали бота: {blocked}',
    )
    manager.dialog_data.update({'message_id': None})
    await manager.switch_to(NewsletterState.start)


async def handle_set_periodic_newsletter_title(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['periodic_newsletter_title'] = message.text
    await manager.switch_to(NewsletterState.set_periodic_entity)


async def handle_set_periodic_newsletter_entity(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data['message_id'] = message.message_id
    manager.dialog_data['from_chat_id'] = message.chat.id
    await manager.switch_to(NewsletterState.periodic_create_approve)


async def handle_periodic_newsletter_create(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    bot = manager.middleware_data['bot']
    create_periodic_newsletter = manager.middleware_data['container'].resolve(
        CreatePeriodicNewsletter,
    )

    title = manager.dialog_data['periodic_newsletter_title']
    message_id = manager.dialog_data['message_id']
    from_chat_id = manager.dialog_data['from_chat_id']

    newsletter_uuid = await create_periodic_newsletter.execute(
        bot_id=bot.id,
        title=title,
        message_id=message_id,
        from_chat_id=from_chat_id,
    )
    await bot.send_message(
        callback.from_user.id,
        '✅ Периодическая рассылка успешно создана!',
    )
    manager.dialog_data['newsletter_uuid'] = newsletter_uuid
    await manager.switch_to(NewsletterState.periodic_detail)


def _serialize_date(dt: datetime, td: timedelta = None) -> str:
    if not dt:
        return '-'
    dt = dt.astimezone(pytz.timezone('Europe/Moscow'))
    if td:
        dt += td
    return dt.strftime('%H:%M %d.%m.%Y')


def _serialize_newsletter(newsletter: PeriodicNewsletterEntity) -> None:
    newsletter.next_at = _serialize_date(newsletter.started_at, td=timedelta(days=1))
    newsletter.started_at = _serialize_date(newsletter.started_at)
    newsletter.status = 'Неактивна' if not newsletter.status else 'Активна'


async def change_state_to_get_detail(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data['newsletter_uuid'] = item_id
    await manager.switch_to(NewsletterState.periodic_detail)


async def get_periodic_newsletter_detail(
    **middleware_data,
) -> dict:
    dialog_manager = middleware_data['dialog_manager']
    bot = dialog_manager.middleware_data['bot']
    newsletter_uuid = dialog_manager.dialog_data['newsletter_uuid']
    get_periodic_newsletter = dialog_manager.middleware_data['container'].resolve(
        GetPeriodicNewsletter,
    )

    newsletter = await get_periodic_newsletter.execute(
        bot_id=bot.id,
        newsletter_uuid=newsletter_uuid,
    )
    _serialize_newsletter(newsletter)
    return {'newsletter': newsletter}


async def get_periodic_newsletter_list(
    **middleware_data,
) -> dict[str, list[PeriodicNewsletterEntity]]:
    bot_id = middleware_data['bot'].id
    get_periodic_newsletters = middleware_data['container'].resolve(GetPeriodicNewsletters)

    periodic_newsletters = await get_periodic_newsletters.execute(bot_id)

    return {'newsletters': periodic_newsletters}


async def handle_change_periodic_newsletter_date(
    message: types.Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    change_date = manager.middleware_data['container'].resolve(ChangePeriodicNewsletterDate)
    newsletter_uuid = manager.dialog_data['newsletter_uuid']

    try:
        date = datetime.strptime(message.text, '%H:%M %d.%m.%Y').astimezone(
            tz=pytz.timezone('Europe/Moscow'),
        )
    except ValueError:
        await manager.middleware_data['bot'].send_message(
            message.from_user.id,
            'Введённые данные неверны, попробуйте ещё раз',
        )
        return

    try:
        await change_date.execute(
            newsletter_uuid=newsletter_uuid,
            date=date,
        )
    except WrongTime:
        await manager.middleware_data['bot'].send_message(
            message.from_user.id,
            'Дата не может быть раньше текущей',
        )
        return
    await manager.switch_to(NewsletterState.periodic_detail)


async def handle_change_periodic_newsletter_status(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    change_status = manager.middleware_data['container'].resolve(ChangePeriodicNewsletterStatus)
    newsletter_uuid = manager.dialog_data['newsletter_uuid']

    await change_status.execute(newsletter_uuid=newsletter_uuid)


async def handle_change_periodic_newsletter_delete(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    delete_newsletter = manager.middleware_data['container'].resolve(DeletePeriodicNewsletter)
    newsletter_uuid = manager.dialog_data['newsletter_uuid']

    await delete_newsletter.execute(newsletter_uuid=newsletter_uuid)
    await manager.switch_to(NewsletterState.periodic_list)
