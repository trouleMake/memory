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
        memories = self.extractor.extract(user_id, message)

        for memory in memories:
            self.repository.save_or_update(memory)

        return memories

    def get_relevant_memories(self, user_id: int, query: str, limit: int = 5) -> List[MemoryItem]:
        return self.repository.search_relevant(user_id, query, limit)

    def get_all_memories(self, user_id: int) -> List[MemoryItem]:
        return self.repository.find_by_user_id(user_id)

    def delete_memory(self, user_id: int, key: str) -> None:
        self.repository.delete(user_id, key)