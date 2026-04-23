from __future__ import annotations

from typing import List

from memory_extractor import MemoryExtractor
from memory_item import MemoryItem
from memory_repository import MemoryRepository


class MemoryService:
    def __init__(self, extractor: MemoryExtractor, repository: MemoryRepository) -> None:
        self.extractor: MemoryExtractor = extractor
        self.repository: MemoryRepository = repository

    def extract_and_save(self, user_id: int, message: str) -> List[MemoryItem]:
        pass

    def get_relevant_memories(self, user_id: int, query: str, limit: int = 5) -> List[MemoryItem]:
        pass

    def get_all_memories(self, user_id: int) -> List[MemoryItem]:
        pass

    def delete_memory(self, user_id: int, key: str) -> None:
        pass