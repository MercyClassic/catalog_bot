import operator
from functools import partial

from aiogram import Router, types
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    Group,
    ListGroup,
    Radio,
    Row,
    Select,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from catalog_bot.application.handlers.catalog.catalog import handle_get_catalog
from catalog_bot.application.handlers.catalog.category import (
    change_admin_state_to_get_category_detail,
    change_client_state_to_get_category_detail,
    handle_category_change_description,
    handle_category_change_image,
    handle_category_change_title,
    handle_category_create,
    handle_category_delete,
    handle_get_category,
)
from catalog_bot.application.handlers.catalog.channel import (
    change_state_to_get_channel_detail,
    change_state_to_get_welcome_message_detail,
    get_channel_autocommit_button_text,
    get_welcome_message_detail,
    get_welcome_messages,
    handle_channel_change_autocommit,
    handle_channel_change_link,
    handle_channel_change_title,
    handle_channel_create,
    handle_channel_delete,
    handle_get_channel,
    handle_welcome_message_change_media,
    handle_welcome_message_change_text,
    handle_welcome_message_create,
    handle_welcome_message_create_set_button,
    handle_welcome_message_create_set_button_type,
    handle_welcome_message_create_set_media,
    handle_welcome_message_create_set_title,
    handle_welcome_message_delete,
)
from catalog_bot.application.interactors.admin.is_admin import IsAdmin
from catalog_bot.application.interactors.tap_client.save_tap_client import SaveTapClient
from catalog_bot.application.tg.markups.start import get_admin_menu_markup
from catalog_bot.application.tg.states.admin import AdminCatalogState
from catalog_bot.application.tg.states.client import ClientCatalogState
from catalog_bot.domain.exceptions.tap_client import TapClientAlreadyExist
from catalog_bot.presentators.tg.routers.join_channel import (
    start_sending_welcome_messages,
)

router = Router()


@router.message(CommandStart())
async def start_catalog_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    bot = dialog_manager.middleware_data['bot']
    is_admin = dialog_manager.middleware_data['container'].resolve(IsAdmin)
    user_save = dialog_manager.middleware_data['container'].resolve(SaveTapClient)
    is_admin = await is_admin.execute(bot_id=bot.id, user_id=message.from_user.id)
    if is_admin:
        markup = get_admin_menu_markup()
    else:
        markup = None

    await bot.send_message(
        message.from_user.id,
        f'Добро пожаловать в бота @{message.from_user.username or message.from_user.first_name}',
        reply_markup=markup,
    )
    if not is_admin:
        try:
            await user_save.execute(
                telegram_user_id=message.from_user.id,
                bot_id=bot.id,
                telegram_username=message.from_user.username,
            )
        except TapClientAlreadyExist:
            pass
        else:
            await start_sending_welcome_messages(
                message.from_user.id,
                bot.id,
                bot,
                dialog_manager.middleware_data['container'],
                dialog_manager.middleware_data['fsm_storage'],
                type_='bot',
            )
            return
    await dialog_manager.start(ClientCatalogState.start, mode=StartMode.RESET_STACK)


user_categories = Column(
    Select(
        Format('{item.title}'),
        id='categories',
        item_id_getter=operator.attrgetter('uuid'),
        items='categories',
        on_click=change_client_state_to_get_category_detail,
    ),
)

user_channels = ListGroup(
    Url(
        Format('{item.title}'),
        Format('{item.link}'),
    ),
    id='user_channels',
    item_id_getter=operator.attrgetter('uuid'),
    items='channels',
)

client_dialog = Dialog(
    Window(
        DynamicMedia('menu_media'),
        Format('{menu.text}'),
        user_categories,
        user_channels,
        state=ClientCatalogState.start,
        getter=handle_get_catalog,
    ),
    Window(
        DynamicMedia('category_media'),
        Format('{message}'),
        user_categories,
        user_channels,
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_user_category_detail',
            state=ClientCatalogState.start,
        ),
        state=ClientCatalogState.category_detail,
        getter=handle_get_category,
    ),
)

admin_categories = Column(
    Select(
        Format('{item.title}'),
        id='categories',
        item_id_getter=operator.attrgetter('uuid'),
        items='categories',
        on_click=change_admin_state_to_get_category_detail,
    ),
)

admin_channels = Column(
    Select(
        Format('{item.title}'),
        id='admin_channels',
        item_id_getter=operator.attrgetter('uuid'),
        items='channels',
        on_click=change_state_to_get_channel_detail,
    ),
)

admin_dialog = Dialog(
    Window(
        DynamicMedia('menu_media'),
        Format('{menu.text}'),
        admin_categories,
        admin_channels,
        Row(
            SwitchTo(
                Const('➕ Категория'),
                id='category_create_category_main',
                state=AdminCatalogState.category_create,
            ),
            SwitchTo(
                Const('➕ Канал'),
                id='category_create_channel_main',
                state=AdminCatalogState.channel_create,
            ),
        ),
        state=AdminCatalogState.start,
        getter=partial(handle_get_catalog, for_admin=True),
    ),
    Window(
        DynamicMedia('category_media'),
        Format('{message}'),
        admin_categories,
        admin_channels,
        Group(
            SwitchTo(
                Const('📝 Название категории'),
                id='change_category_title',
                state=AdminCatalogState.category_change_title,
            ),
            SwitchTo(
                Const('📝 Описание категории'),
                id='change_category_description',
                state=AdminCatalogState.category_change_description,
            ),
            SwitchTo(
                Const('📝 Фото категории'),
                id='change_category_image',
                state=AdminCatalogState.category_change_image,
            ),
            width=2,
        ),
        Group(
            SwitchTo(
                Const('➕ Категория'),
                id='category_create_category',
                state=AdminCatalogState.category_create,
            ),
            SwitchTo(
                Const('➕ Канал'),
                id='category_create_channel',
                state=AdminCatalogState.channel_create,
            ),
            SwitchTo(
                Const('🗑 Удалить'),
                id='delete_category',
                state=AdminCatalogState.category_delete,
            ),
            width=2,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_admin_category_detail',
            state=AdminCatalogState.start,
        ),
        getter=handle_get_category,
        state=AdminCatalogState.category_detail,
    ),
    Window(
        Const('Отправьте боту название категории'),
        MessageInput(handle_category_create),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_create_category',
            state=AdminCatalogState.start,
        ),
        state=AdminCatalogState.category_create,
    ),
    Window(
        Const('Отправьте боту название категории'),
        MessageInput(handle_category_change_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_category_change_title',
            state=AdminCatalogState.category_detail,
        ),
        state=AdminCatalogState.category_change_title,
    ),
    Window(
        Const('Отправьте боту описание категории'),
        MessageInput(handle_category_change_description),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_category_change_description',
            state=AdminCatalogState.category_detail,
        ),
        state=AdminCatalogState.category_change_description,
    ),
    Window(
        Const('Отправьте боту фото категории'),
        MessageInput(
            handle_category_change_image,
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_category_change_photo',
            state=AdminCatalogState.category_detail,
        ),
        state=AdminCatalogState.category_change_image,
    ),
    Window(
        Const('Вы действительно хотите удалить категорию?'),
        Button(
            Const('✅ Да'),
            id='delete_category_approve',
            on_click=handle_category_delete,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_category_delete',
            state=AdminCatalogState.category_detail,
        ),
        state=AdminCatalogState.category_delete,
    ),
    Window(
        Format('{message}'),
        SwitchTo(
            Const('Изменить название канала'),
            id='change_channel_title',
            state=AdminCatalogState.channel_change_title,
        ),
        SwitchTo(
            Const('Изменить ссылку'),
            id='change_channel_link',
            state=AdminCatalogState.channel_change_link,
        ),
        SwitchTo(
            Const('Автоподтверждение заявок'),
            id='change_channel_autocommit',
            state=AdminCatalogState.channel_change_autocommit,
        ),
        SwitchTo(
            Const('Приветственные сообщения'),
            id='get_welcome_messages',
            state=AdminCatalogState.get_welcome_messages,
        ),
        SwitchTo(
            Const('🗑 Удалить'),
            id='delete_channel',
            state=AdminCatalogState.channel_delete,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_admin_channel_detail',
            state=AdminCatalogState.start,
        ),
        getter=handle_get_channel,
        state=AdminCatalogState.channel_detail,
    ),
    Window(
        Const(
            '1. Сделайте бота админом в канале\n' '2. Перешлите сюда любое сообщение с канала',
        ),
        MessageInput(handle_channel_create),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_channel_create',
            state=AdminCatalogState.start,
        ),
        state=AdminCatalogState.channel_create,
    ),
    Window(
        Const('Отправьте боту название канала'),
        MessageInput(handle_channel_change_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_channel_change_title',
            state=AdminCatalogState.channel_detail,
        ),
        state=AdminCatalogState.channel_change_title,
    ),
    Window(
        Const('Отправьте боту ссылку'),
        MessageInput(handle_channel_change_link),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_channel_change_link',
            state=AdminCatalogState.channel_detail,
        ),
        state=AdminCatalogState.channel_change_link,
    ),
    Window(
        Const('Статус автоприёма заявок: '),
        Button(
            Format('{text}'),
            id='handle_change_channel_autocommit',
            on_click=handle_channel_change_autocommit,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_channel_change_autocommit',
            state=AdminCatalogState.channel_detail,
        ),
        getter=get_channel_autocommit_button_text,
        state=AdminCatalogState.channel_change_autocommit,
    ),
    Window(
        Const('Вы действительно хотите удалить канал?'),
        Button(
            Const('✅ Да'),
            id='delete_channel_approve',
            on_click=handle_channel_delete,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_channel_delete',
            state=AdminCatalogState.channel_detail,
        ),
        state=AdminCatalogState.channel_delete,
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
            state=AdminCatalogState.welcome_message_create_set_title,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_welcome_messages',
            state=AdminCatalogState.channel_detail,
        ),
        getter=get_welcome_messages,
        state=AdminCatalogState.get_welcome_messages,
    ),
    Window(
        DynamicMedia('message_media'),
        Format('{message}'),
        SwitchTo(
            Const('🗑 Удалить'),
            id='delete_welcome_message',
            state=AdminCatalogState.welcome_message_delete,
        ),
        SwitchTo(
            Const('Изменить'),
            id='change_welcome_message',
            state=AdminCatalogState.welcome_message_change,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_detail',
            state=AdminCatalogState.get_welcome_messages,
        ),
        getter=get_welcome_message_detail,
        state=AdminCatalogState.welcome_message_detail,
    ),
    Window(
        Const('Выберите действие'),
        SwitchTo(
            Const('Изменить текст'),
            id='change_welcome_message_text',
            state=AdminCatalogState.welcome_message_change_text,
        ),
        SwitchTo(
            Const('Изменить медиа'),
            id='change_welcome_message_media',
            state=AdminCatalogState.welcome_message_change_media,
        ),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_change',
            state=AdminCatalogState.welcome_message_detail,
        ),
        state=AdminCatalogState.welcome_message_change,
    ),
    Window(
        Const('Введите новый текст приветственного сообщения'),
        MessageInput(handle_welcome_message_change_text),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_change_text',
            state=AdminCatalogState.welcome_message_change,
        ),
        state=AdminCatalogState.welcome_message_change_text,
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
            state=AdminCatalogState.welcome_message_change,
        ),
        state=AdminCatalogState.welcome_message_change_media,
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
            state=AdminCatalogState.get_welcome_messages,
        ),
        state=AdminCatalogState.welcome_message_delete,
    ),
    Window(
        Const('Напишите текст, который увидит пользователь, когда присоединится к каналу'),
        MessageInput(handle_welcome_message_create_set_title),
        SwitchTo(
            Const('🔙 Назад'),
            id='back_from_message_create',
            state=AdminCatalogState.get_welcome_messages,
        ),
        state=AdminCatalogState.welcome_message_create_set_title,
    ),
    Window(
        Const('Отправьте фото, которое будет прикреплено к сообщению'),
        SwitchTo(
            Const('Продолжить без фото'),
            id='continue_without_image',
            state=AdminCatalogState.welcome_message_choose_button_or_create,
        ),
        MessageInput(handle_welcome_message_create_set_media, content_types=[ContentType.PHOTO]),
        state=AdminCatalogState.welcome_message_create_set_media,
    ),
    Window(
        Const('Вы хотите добавить кнопки к этому сообщению?'),
        SwitchTo(
            Const('Да'),
            id='set_message_button_type',
            state=AdminCatalogState.welcome_message_create_set_button_type,
        ),
        SwitchTo(
            Const('Нет'),
            id='move_to_create_welcome_message',
            state=AdminCatalogState.welcome_message_create,
        ),
        state=AdminCatalogState.welcome_message_choose_button_or_create,
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
        state=AdminCatalogState.welcome_message_create_set_button_type,
    ),
    Window(
        Const(
            'Напишите текст, который будет отображаться на кнопке\n'
            'Или нажмите кнопку ниже, чтобы продолжить создание',
        ),
        SwitchTo(
            Const('Продолжить'),
            id='buttons_continue_to_create',
            state=AdminCatalogState.welcome_message_create,
        ),
        MessageInput(handle_welcome_message_create_set_button),
        state=AdminCatalogState.welcome_message_create_set_buttons,
    ),
    Window(
        Const('Подтвердите создание'),
        Button(
            Const('Создать'),
            id='create_welcome_message_button',
            on_click=handle_welcome_message_create,
        ),
        state=AdminCatalogState.welcome_message_create,
    ),
)

router.include_router(client_dialog)
router.include_router(admin_dialog)
