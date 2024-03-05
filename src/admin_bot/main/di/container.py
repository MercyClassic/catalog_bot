from punq import Container

from admin_bot.application.services.admin import AdminService
from admin_bot.application.services.catalog_bot import CatalogService
from admin_bot.db.repositories.admin import AdminRepository
from admin_bot.db.repositories.catalog_bot import CatalogBotRepository


def get_container() -> Container:
    container = Container()
    container.register(AdminRepository)
    container.register(CatalogBotRepository)
    container.register(AdminService)
    container.register(CatalogService)
    return container
