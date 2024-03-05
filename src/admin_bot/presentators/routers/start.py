import operator

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from admin_bot.application.handlers.admin import (
    change_state_to_catalog_bot_detail,
    get_catalog_bot,
    get_catalog_bots_by_telegram_owner_id,
    handle_catalog_bot_set_title,
    handle_catalog_bot_set_token,
    switch_container_status,
)
from admin_bot.application.state.start import StartState

router = Router()


@router.message(CommandStart())
async def start_start_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(StartState.main)


dialog = Dialog(
    Window(
        Const('Добро пожаловать в конструктор ботов'),
        SwitchTo(
            Const('Список ботов для подписок'),
            id='get_catalog_bot_list',
            state=StartState.catalog_bot_list,
        ),
        state=StartState.main,
    ),
    Window(
        Const('👇 Список ваших ботов для подписок'),
        Column(
            Select(
                Format('{item.title}'),
                id='catalog_bot_detail',
                item_id_getter=operator.attrgetter('uuid'),
                on_click=change_state_to_catalog_bot_detail,
                items='catalog_bots',
            ),
        ),
        SwitchTo(
            Const('➕ Бот для подписок'),
            id='create_catalog_bot',
            state=StartState.create_bot_set_title,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_catalog_bot_list',
            state=StartState.main,
        ),
        getter=get_catalog_bots_by_telegram_owner_id,
        state=StartState.catalog_bot_list,
    ),
    Window(
        Format(
            'Название: {catalog_bot.title}\n'
            'Токен бота: <span class="tg-spoiler">{catalog_bot.token}</span>',
        ),
        Button(
            Format('{status_text}'),
            id='switch_container_status',
            on_click=switch_container_status,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_catalog_bot_detail',
            state=StartState.catalog_bot_list,
        ),
        parse_mode='html',
        getter=get_catalog_bot,
        state=StartState.catalog_bot_detail,
    ),
    Window(
        Const('👇 Напишите название для бота'),
        MessageInput(handle_catalog_bot_set_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_catalog_bot_set_title',
            state=StartState.catalog_bot_list,
        ),
        state=StartState.create_bot_set_title,
    ),
    Window(
        Const('👇 Отправьте токен'),
        MessageInput(handle_catalog_bot_set_token),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_catalog_bot_set_token',
            state=StartState.create_bot_set_title,
        ),
        state=StartState.create_bot_set_token,
    ),
)

router.include_router(dialog)
