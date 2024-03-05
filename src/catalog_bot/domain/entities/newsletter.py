from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PeriodicNewsletterEntity:
    uuid: UUID | None
    title: str
    message_id: int
    from_chat_id: int
    started_at: datetime
    status: bool
