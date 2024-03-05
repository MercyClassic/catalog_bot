import operator

from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from catalog_bot.application.handlers.newsletter import (
    change_state_to_get_detail,
    change_state_to_send_approve,
    get_periodic_newsletter_detail,
    get_periodic_newsletter_list,
    handle_change_periodic_newsletter_date,
    handle_change_periodic_newsletter_delete,
    handle_change_periodic_newsletter_status,
    handle_default_newsletter_cancel,
    handle_default_newsletter_send,
    handle_periodic_newsletter_cancel,
    handle_periodic_newsletter_create,
    handle_set_periodic_newsletter_entity,
    handle_set_periodic_newsletter_title,
)
from catalog_bot.application.tg.states.newsletter import NewsletterState

router = Router()


dialog = Dialog(
    Window(
        Const('👇 Выберите тип рассылки'),
        SwitchTo(
            Const('Обычная рассылка'),
            id='default_newsletter',
            state=NewsletterState.default,
        ),
        SwitchTo(
            Const('Периодическая рассылка'),
            id='periodic_newsletter',
            state=NewsletterState.periodic_list,
        ),
        state=NewsletterState.start,
    ),
    Window(
        Const(
            'Отправьте боту то, что хотите отправить. '
            'Это может быть текст, картинка, видео, гифка или стикер.',
        ),
        MessageInput(change_state_to_send_approve),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_default',
            state=NewsletterState.start,
        ),
        state=NewsletterState.default,
    ),
    Window(
        Const('Вы действительно хотите хотите отрпавить эту рассылку?'),
        Button(
            Const('✅ Да'),
            id='send_newsletter_approve',
            on_click=handle_default_newsletter_send,
        ),
        Button(
            Const('❌ Нет'),
            id='send_newsletter_cancel',
            on_click=handle_default_newsletter_cancel,
        ),
        state=NewsletterState.approve,
    ),
    Window(
        Const('👇 Список переодичных рассылок'),
        Column(
            Select(
                Format('{item.title}'),
                id='periodic_newsletters',
                item_id_getter=operator.attrgetter('uuid'),
                items='newsletters',
                on_click=change_state_to_get_detail,
            ),
        ),
        SwitchTo(
            Const('➕ Создать рассылку'),
            id='create_periodic_newsletter',
            state=NewsletterState.set_periodic_title,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_periodic_list',
            state=NewsletterState.start,
        ),
        getter=get_periodic_newsletter_list,
        state=NewsletterState.periodic_list,
    ),
    Window(
        Const('👇 Отправьте боту название переодичной рассылки.'),
        MessageInput(handle_set_periodic_newsletter_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_title',
            state=NewsletterState.start,
        ),
        state=NewsletterState.set_periodic_title,
    ),
    Window(
        Const(
            'Отправьте боту то, что хотите отправить. '
            'Это может быть текст, картинка, видео, гифка или стикер.',
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_periodic_newsletter',
            state=NewsletterState.periodic_list,
        ),
        MessageInput(handle_set_periodic_newsletter_entity),
        state=NewsletterState.set_periodic_entity,
    ),
    Window(
        Const('Вы действительно хотите хотите отрпавить эту рассылку?'),
        Button(
            Const('✅ Да'),
            id='create_periodic_newsletter_approve',
            on_click=handle_periodic_newsletter_create,
        ),
        Button(
            Const('❌ Нет'),
            id='create_periodic_newsletter_cancel',
            on_click=handle_periodic_newsletter_cancel,
        ),
        state=NewsletterState.periodic_create_approve,
    ),
    Window(
        Format(
            'Название: {newsletter.title}\n'
            'Дата начала: {newsletter.started_at}\n'
            'Следующая рассылка: {newsletter.next_at}\n'
            'Статус: {newsletter.status}\n\n'
            '* Периодичность 1 день',
        ),
        Column(
            SwitchTo(
                Const('📝 Дата начала'),
                id='back_from_change_periodic_newsletter_date',
                state=NewsletterState.periodic_change_date,
            ),
            Button(
                Format('▶️ Включить/Выключить'),
                id='back_from_change_periodic_newsletter_status',
                on_click=handle_change_periodic_newsletter_status,
            ),
            Button(
                Const('🗑 Удалить'),
                id='back_from_delete_periodic_newsletter',
                on_click=handle_change_periodic_newsletter_delete,
            ),
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_periodic_detail',
            state=NewsletterState.periodic_list,
        ),
        state=NewsletterState.periodic_detail,
        getter=get_periodic_newsletter_detail,
    ),
    Window(
        Jinja(
            """
        Отправьте время в следующем формате
        <pre><code class="language-python">00:00 01.01.1970</code></pre>
        """,
        ),
        MessageInput(handle_change_periodic_newsletter_date),
        state=NewsletterState.periodic_change_date,
        parse_mode='html',
    ),
)

router.include_router(dialog)
