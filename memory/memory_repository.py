from __future__ import annotations

from typing import List, Optional

from memory_item import MemoryItem


class MemoryRepository:
    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.database: str = database

    def save_or_update(self, memory_item: MemoryItem) -> None:
        pass

    def find_by_user_id(self, user_id: int) -> List[MemoryItem]:
        pass

    def search_relevant(self, user_id: int, query: str, limit: int = 10) -> List[MemoryItem]:
        pass

    def delete(self, user_id: int, key: str) -> None:
        pass

    def find_by_user_id_and_key(self, user_id: int, key: str) -> Optional[MemoryItem]:
        pass