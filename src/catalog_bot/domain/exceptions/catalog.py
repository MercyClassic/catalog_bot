from catalog_bot.domain.exceptions.base import DomainException


class ChannelNotFound(DomainException):
    pass


class ChannelAlreadyExists(DomainException):
    pass


class CategoryNotFound(DomainException):
    pass


class CategoryAlreadyExists(DomainException):
    pass


class NoAutoCommitJoinRequest(DomainException):
    pass
