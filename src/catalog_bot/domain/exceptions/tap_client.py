from catalog_bot.domain.exceptions.base import DomainException


class TapClientAlreadyExist(DomainException):
    pass


class TapClientNotFound(DomainException):
    pass
