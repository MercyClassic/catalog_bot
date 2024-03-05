from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class ChannelEntity:
    uuid: UUID | None
    chat_id: int
    title: str
    link: str | None
    auto_commit: bool
    bot_uuid: UUID | None
    category_uuid: UUID | None


@dataclass
class CategoryEntity:
    uuid: UUID | None
    title: str
    description: str | None
    image: str | None
    bot_uuid: UUID | None
    category_uuid: UUID | None
    subcategories: list['CategoryEntity'] = field(default_factory=list)
    channels: list['ChannelEntity'] = field(default_factory=list)
