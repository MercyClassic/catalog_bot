from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class BotEntity:
    uuid: UUID | None
    telegram_owner_id: int
    telegram_bot_id: int
    text_menu: str
    media_menu: str
    admins: list['AdminEntity'] = field(default_factory=list)


@dataclass
class AdminEntity:
    uuid: UUID | None
    telegram_id: int
    bot_uuid: UUID


@dataclass
class MenuEntity:
    bot_uuid: UUID | None
    text: str
    media: str
