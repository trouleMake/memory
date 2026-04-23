from __future__ import annotations

from typing import List

from memory_item import MemoryItem


class MemoryExtractor:
    def extract(self, user_id: int, message: str) -> List[MemoryItem]:
        pass