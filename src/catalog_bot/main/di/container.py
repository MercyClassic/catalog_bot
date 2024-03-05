from punq import Container

from catalog_bot.application.interactors.admin.create_admin import CreateAdmin
from catalog_bot.application.interactors.admin.delete_admin import DeleteAdmin
from catalog_bot.application.interactors.admin.get_admins import GetAdmins
from catalog_bot.application.interactors.admin.is_admin import IsAdmin
from catalog_bot.application.interactors.catalog.category.change_description import (
    ChangeCategoryDescription,
)
from catalog_bot.application.interactors.catalog.category.change_image import (
    ChangeCategoryImage,
)
from catalog_bot.application.interactors.catalog.category.change_title import (
    ChangeCategoryTitle,
)
from catalog_bot.application.interactors.catalog.category.create_category import (
    CreateCategory,
)
from catalog_bot.application.interactors.catalog.category.delete_category import (
    DeleteCategory,
)
from catalog_bot.application.interactors.catalog.category.get_categories import (
    GetCategories,
)
from catalog_bot.application.interactors.catalog.category.get_category import (
    GetCategory,
)
from catalog_bot.application.interactors.catalog.channel.change_auto_commit import (
    ChangeChannelAutoCommit,
)
from catalog_bot.application.interactors.catalog.channel.change_link import (
    ChangeChannelLink,
)
from catalog_bot.application.interactors.catalog.channel.change_title import (
    ChangeChannelTitle,
)
from catalog_bot.application.interactors.catalog.channel.delete_channel import (
    DeleteChannel,
)
from catalog_bot.application.interactors.catalog.channel.get_channel import GetChannel
from catalog_bot.application.interactors.catalog.channel.get_channel_by_uuid import (
    GetChannelByUUID,
)
from catalog_bot.application.interactors.catalog.channel.get_channels import GetChannels
from catalog_bot.application.interactors.catalog.channel.join_channel import JoinChannel
from catalog_bot.application.interactors.catalog.channel.register_channel import (
    RegisterChannel,
)
from catalog_bot.application.interactors.menu.change_media import ChangeMedia
from catalog_bot.application.interactors.menu.change_text import ChangeText
from catalog_bot.application.interactors.menu.get_menu import GetMenu
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
from catalog_bot.application.interactors.statistic.get_statistic import GetStatistic
from catalog_bot.application.interactors.tap_client.get_clients import GetTapClients
from catalog_bot.application.interactors.tap_client.is_tap_client_exist import (
    IsTapClientExist,
)
from catalog_bot.application.interactors.tap_client.save_tap_client import SaveTapClient
from catalog_bot.application.interactors.tap_client.user_block_bot import UserBlockBot
from catalog_bot.application.services.welcome_message import WelcomeMessageService
from catalog_bot.infrastructure.db.interfaces.uow import UoWInterface
from catalog_bot.infrastructure.db.uow import UoW


def get_container() -> Container:
    container = Container()
    container.register(UoWInterface, UoW)

    container.register(SaveTapClient)
    container.register(GetTapClients)
    container.register(IsTapClientExist)
    container.register(UserBlockBot)

    container.register(CreateCategory)
    container.register(GetCategories)
    container.register(GetCategory)

    container.register(ChangeCategoryTitle)
    container.register(ChangeCategoryDescription)
    container.register(ChangeCategoryImage)
    container.register(DeleteCategory)

    container.register(RegisterChannel)
    container.register(GetChannels)
    container.register(GetChannel)
    container.register(GetChannelByUUID)
    container.register(JoinChannel)

    container.register(ChangeChannelTitle)
    container.register(ChangeChannelLink)
    container.register(ChangeChannelAutoCommit)
    container.register(DeleteChannel)
    container.register(WelcomeMessageService)

    container.register(IsAdmin)
    container.register(GetAdmins)
    container.register(CreateAdmin)
    container.register(DeleteAdmin)

    container.register(ChangeText)
    container.register(ChangeMedia)
    container.register(GetMenu)

    container.register(GetStatistic)

    container.register(CreatePeriodicNewsletter)
    container.register(GetPeriodicNewsletters)
    container.register(GetPeriodicNewsletter)
    container.register(ChangePeriodicNewsletterStatus)
    container.register(ChangePeriodicNewsletterDate)
    container.register(DeletePeriodicNewsletter)

    return container
