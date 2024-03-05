from catalog_bot.domain.exceptions.base import DomainException


class CaptchaExpired(DomainException):
    pass


class CaptchaDoesNotMatch(DomainException):
    pass
