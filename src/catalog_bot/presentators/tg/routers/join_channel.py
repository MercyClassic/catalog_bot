from typing import Literal

from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from punq import Container

from catalog_bot.application.interactors.catalog.channel.join_channel import JoinChannel
from catalog_bot.application.interactors.tap_client.save_tap_client import SaveTapClient
from catalog_bot.application.services.welcome_message import WelcomeMessageService
from catalog_bot.application.tg.states.welcome_message import WelcomeMessageState
from catalog_bot.domain.entities.welcome_message import (
    ButtonEntity,
    WelcomeMessageEntity,
)
from catalog_bot.domain.exceptions.catalog import (
    ChannelNotFound,
    NoAutoCommitJoinRequest,
)
from catalog_bot.domain.exceptions.tap_client import TapClientAlreadyExist

router = Router()


@router.chat_join_request()
async def join_channel_handler(
    chat_join_request: types.ChatJoinRequest,
    bot: Bot,
    container: Container,
    fsm_storage: BaseStorage,
) -> None:
    join_channel = container.resolve(JoinChannel)

    try:
        await join_channel.execute(bot_id=bot.id, chat_id=chat_join_request.chat.id)
    except (ChannelNotFound, NoAutoCommitJoinRequest):
        return

    await bot.approve_chat_join_request(
        chat_join_request.chat.id,
        chat_join_request.from_user.id,
    )

    user_save = container.resolve(SaveTapClient)

    try:
        await user_save.execute(
            telegram_user_id=chat_join_request.from_user.id,
            bot_id=bot.id,
            telegram_username=chat_join_request.from_user.username,
        )
    except TapClientAlreadyExist:
        pass

    await start_sending_welcome_messages(
        chat_join_request.from_user.id,
        chat_join_request.chat.id,
        bot,
        container,
        fsm_storage,
        type_='channel',
    )


async def start_sending_welcome_messages(
    from_user_id: int,
    object_id: int,
    bot: Bot,
    container: Container,
    fsm_storage: BaseStorage,
    type_: Literal['bot', 'channel'] = None,
) -> list[WelcomeMessageEntity] | None:
    wm_service = container.resolve(WelcomeMessageService)

    if type_ == 'channel':
        messages = await wm_service.get_welcome_messages_by_chat_id(
            bot_id=bot.id,
            chat_id=object_id,
        )
    else:
        messages = await wm_service.get_welcome_messages_by_bot_id(bot_id=object_id)

    if not messages:
        await bot.send_message(
            from_user_id,
            'Нажмите /start чтобы получить контент',
        )
        return

    welcome_message = messages[0]
    markup = get_buttons_markup(welcome_message.buttons)
    if welcome_message.media:
        await bot.send_photo(
            from_user_id,
            photo=welcome_message.media,
            caption=welcome_message.text,
            reply_markup=markup,
        )
    else:
        await bot.send_message(
            from_user_id,
            text=welcome_message.text,
            reply_markup=markup,
        )
    storage_key = StorageKey(bot.id, from_user_id, from_user_id)
    state = FSMContext(key=storage_key, storage=fsm_storage)

    await state.update_data(
        current_message_number=1,
        messages=messages,
        messages_length=len(messages),
    )
    await state.set_state(WelcomeMessageState.main)


@router.message(WelcomeMessageState.main)
@router.callback_query(F.data == 'welcome_message')
async def send_welcome_message(
    event: types.Message | types.CallbackQuery,
    bot: Bot,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    current_message_number = state_data['current_message_number']
    if current_message_number == state_data['messages_length']:
        await state.clear()
        await bot.send_message(
            event.from_user.id,
            'Нажмите /start чтобы получить контент',
        )
        return

    messages = state_data['messages']
    message = messages[current_message_number]
    await state.update_data(current_message_number=current_message_number + 1)
    markup = get_buttons_markup(message.buttons)
    if message.media:
        await bot.send_photo(
            event.from_user.id,
            photo=message.media,
            caption=message.text,
            reply_markup=markup,
        )
    else:
        await bot.send_message(event.from_user.id, text=message.text, reply_markup=markup)


def build_markup(
    buttons: list[ButtonEntity],
    builder_type: Literal['inline', 'reply'],
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    markup_params = {}
    if builder_type == 'inline':
        builder = InlineKeyboardBuilder()
        for button in buttons:
            builder.button(text=button.text, callback_data='welcome_message')
    else:
        builder = ReplyKeyboardBuilder()
        for button in buttons:
            builder.button(text=button.text)
        markup_params.update({'one_time_keyboard': True, 'resize_keyboard': True})
    builder.adjust(2)
    return builder.as_markup(**markup_params)


def get_buttons_markup(
    buttons: list[ButtonEntity],
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    if buttons:
        markup = build_markup(buttons, buttons[0].type)
    else:
        markup = InlineKeyboardBuilder()
        markup.button(text='Далее', callback_data='welcome_message')
        markup = markup.as_markup()
    return markup
