from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class RagItem:
    id: int | None
    user_id: int | None
    title: str
    content: str
    category: str
    tags: list[str] = field(default_factory=list)
    source: str = "manual"
    status: str = "active"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    score: float = 0.0
