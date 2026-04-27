from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MemoryItem:
    id: Optional[int]
    user_id: int
    key: str
    value: str
    type: str
    importance: int
    source: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]