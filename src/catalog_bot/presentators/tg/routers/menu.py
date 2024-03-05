import operator

from aiogram import Router
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, Radio, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from catalog_bot.application.handlers.menu import (
    change_state_to_get_welcome_message_detail,
    get_welcome_message_detail,
    get_welcome_messages,
    handle_media_change,
    handle_text_change,
    handle_welcome_message_change_media,
    handle_welcome_message_change_text,
    handle_welcome_message_create,
    handle_welcome_message_create_set_button,
    handle_welcome_message_create_set_button_type,
    handle_welcome_message_create_set_media,
    handle_welcome_message_create_set_title,
    handle_welcome_message_delete,
    set_bot_uuid,
)
from catalog_bot.application.tg.states.menu import MenuState

router = Router()


dialog = Dialog(
    Window(
        Const('Настройки:\n'),
        SwitchTo(
            Const('Текст главного меню'),
            id='text_main_menu',
            state=MenuState.text,
        ),
        SwitchTo(
            Const('Медиа главного меню'),
            id='media_main_menu',
            state=MenuState.media,
        ),
        SwitchTo(
            Const('Приветственные сообщения'),
            id='get_welcome_messages',
            state=MenuState.get_welcome_messages,
        ),
        state=MenuState.start,
    ),
    Window(
        Const('Введите новый текст главного меню'),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_menu_text',
            state=MenuState.start,
        ),
        MessageInput(handle_text_change),
        state=MenuState.text,
    ),
    Window(
        Const('Отправьте новое изображение главного меню'),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_menu_media',
            state=MenuState.start,
        ),
        MessageInput(handle_media_change, content_types=[ContentType.PHOTO]),
        state=MenuState.media,
    ),
    Window(
        Const('Список сообщений, которые увидит пользователь (максимум 5)\n\n'),
        Column(
            Select(
                Format('{item.order}. {item.text}'),
                id='to_msg_detail',
                items='welcome_messages',
                item_id_getter=operator.attrgetter('button_data'),
                on_click=change_state_to_get_welcome_message_detail,
            ),
        ),
        SwitchTo(
            Const('Создать новое сообщение'),
            id='create_new_welcome_message',
            state=MenuState.welcome_message_create_set_title,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_welcome_messages',
            state=MenuState.start,
        ),
        getter=get_welcome_messages,
        state=MenuState.get_welcome_messages,
    ),
    Window(
        DynamicMedia('message_media'),
        Format('{message}'),
        SwitchTo(
            Const('🗑 Удалить'),
            id='delete_welcome_message',
            state=MenuState.welcome_message_delete,
        ),
        SwitchTo(
            Const('Изменить'),
            id='change_welcome_message',
            state=MenuState.welcome_message_change,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_detail',
            state=MenuState.get_welcome_messages,
        ),
        getter=get_welcome_message_detail,
        state=MenuState.welcome_message_detail,
    ),
    Window(
        Const('Выберите действие'),
        SwitchTo(
            Const('Изменить текст'),
            id='change_welcome_message_text',
            state=MenuState.welcome_message_change_text,
        ),
        SwitchTo(
            Const('Изменить медиа'),
            id='change_welcome_message_media',
            state=MenuState.welcome_message_change_media,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_change',
            state=MenuState.welcome_message_detail,
        ),
        state=MenuState.welcome_message_change,
    ),
    Window(
        Const('Введите новый текст приветственного сообщения'),
        MessageInput(handle_welcome_message_change_text),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_change_text',
            state=MenuState.welcome_message_change,
        ),
        state=MenuState.welcome_message_change_text,
    ),
    Window(
        Const('Отправьте новое медиа приветственного сообщения'),
        MessageInput(
            handle_welcome_message_change_media,
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_change_media',
            state=MenuState.welcome_message_change,
        ),
        state=MenuState.welcome_message_change_media,
    ),
    Window(
        Const('Вы действительно хотите удалить сообщение?'),
        Button(
            Const('✅ Да'),
            id='delete_welcome_message_approve',
            on_click=handle_welcome_message_delete,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_delete',
            state=MenuState.get_welcome_messages,
        ),
        state=MenuState.welcome_message_delete,
    ),
    Window(
        Const('Напишите текст, который увидит пользователь, когда присоединится к каналу'),
        MessageInput(handle_welcome_message_create_set_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_create',
            state=MenuState.get_welcome_messages,
        ),
        state=MenuState.welcome_message_create_set_title,
    ),
    Window(
        Const('Отправьте фото, которое будет прикреплено к сообщению'),
        SwitchTo(
            Const('Продолжить без фото'),
            id='continue_without_image',
            state=MenuState.welcome_message_choose_button_or_create,
        ),
        MessageInput(handle_welcome_message_create_set_media, content_types=[ContentType.PHOTO]),
        state=MenuState.welcome_message_create_set_media,
    ),
    Window(
        Const('Вы хотите добавить кнопки к этому сообщению?'),
        SwitchTo(
            Const('Да'),
            id='set_message_button_type',
            state=MenuState.welcome_message_create_set_button_type,
        ),
        SwitchTo(
            Const('Нет'),
            id='move_to_create_welcome_message',
            state=MenuState.welcome_message_create,
        ),
        state=MenuState.welcome_message_choose_button_or_create,
    ),
    Window(
        Const('Выберите тип кнопок, для этого сообщения'),
        Radio(
            Format('{item[0]}'),
            Format('{item[0]}'),
            id='set_message_button_type',
            item_id_getter=operator.itemgetter(1),
            items='buttons',
            on_click=handle_welcome_message_create_set_button_type,
        ),
        getter={'buttons': (('Вверху', 'inline'), ('Внизу', 'reply'))},
        state=MenuState.welcome_message_create_set_button_type,
    ),
    Window(
        Const(
            'Напишите текст, который будет отображаться на кнопке\n'
            'Или нажмите кнопку ниже, чтобы продолжить создание',
        ),
        SwitchTo(
            Const('Продолжить'),
            id='buttons_continue_to_create',
            state=MenuState.welcome_message_create,
        ),
        MessageInput(handle_welcome_message_create_set_button),
        state=MenuState.welcome_message_create_set_buttons,
    ),
    Window(
        Const('Подтвердите создание'),
        Button(
            Const('Создать'),
            id='create_welcome_message_button',
            on_click=handle_welcome_message_create,
        ),
        state=MenuState.welcome_message_create,
    ),
    on_start=set_bot_uuid,
)

router.include_router(dialog)
