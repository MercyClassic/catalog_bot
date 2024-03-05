from aiogram import Bot, F, Router, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode

from catalog_bot.application.tg import states

router = Router()


@router.message(F.text == 'Админ меню')
async def start_main_admin_dialog(
    message: types.Message,
    bot: Bot,
) -> None:
    markup = ReplyKeyboardBuilder()
    for text in (
        '📖 Каталог каналов',  # :book:
        '✉️ Рассылка',  # :envelope:
        '📊 Статистика',  # :bar_chart:
        '✏️ Администраторы',  # :pencil2:
        '⚙️ Настройки интерфейса',  # :gear:
    ):
        markup.button(text=text)
    markup.adjust(1, 2, 1, 1, 1)
    markup = markup.as_markup(resize_keyboard=True, one_time_keyboard=False)

    await bot.send_message(
        message.from_user.id,
        'Admin menu\n\nГлавное меню - /start',
        reply_markup=markup,
    )


@router.message(F.text == '📖 Каталог каналов')
async def start_catalog_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(states.admin.AdminCatalogState.start, mode=StartMode.RESET_STACK)


@router.message(F.text == '✉️ Рассылка')
async def start_newsletter_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(states.newsletter.NewsletterState.start, mode=StartMode.RESET_STACK)


@router.message(F.text == '✏️ Администраторы')
async def start_newsletter_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(states.admin.AdminState.start, mode=StartMode.RESET_STACK)


@router.message(F.text == '⚙️ Настройки интерфейса')
async def start_newsletter_dialog(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(states.menu.MenuState.start, mode=StartMode.RESET_STACK)
