from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalPlan:
    user_query: str
    search_text: str
    keywords: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    sort_hint: str = "relevance"
    limit: int = 5
    user_id: int | None = None
