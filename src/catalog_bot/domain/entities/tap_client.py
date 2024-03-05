from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TapClientEntity:
    uuid: UUID | None
    telegram_id: int
    bot_uuid: UUID
    telegram_username: str | None
    joined_at: datetime | None
