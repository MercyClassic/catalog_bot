from catalog_bot.domain.exceptions.base import DomainException


class BotNotFound(DomainException):
    pass


class CantDeleteBotOwner(DomainException):
    pass


class AdminNotFound(DomainException):
    pass


class AdminAlreadyExist(DomainException):
    pass


class CantDeleteItself(DomainException):
    pass
