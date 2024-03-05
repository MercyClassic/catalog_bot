from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal
from uuid import UUID


@dataclass
class ButtonEntity:
    uuid: UUID | None
    message_uuid: UUID | None
    type: Literal['inline', 'reply']
    text: str


@dataclass
class WelcomeMessageEntity:
    uuid: UUID | None
    object_uuid: UUID
    owner_type: Literal['bot', 'channel']
    text: str
    media: str
    order: datetime | None
    buttons: list[ButtonEntity] = field(default_factory=list)
