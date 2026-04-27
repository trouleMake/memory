from __future__ import annotations

import re
from typing import List

from memory_item import MemoryItem


class MemoryExtractor:
    def extract(self, user_id: int, message: str) -> List[MemoryItem]:
        #extract() 用来汇总其他四个函数得到的结果
        text = message.strip()
        memories: List[MemoryItem] = []

        if not text:
            return memories

        memories.extend(self._extract_name(user_id, text))
        memories.extend(self._extract_age(user_id, text))
        memories.extend(self._extract_city(user_id, text))
        memories.extend(self._extract_preference(user_id, text))

        return memories

    def _extract_name(self, user_id: int, text: str) -> List[MemoryItem]:
        patterns = [
            r"我叫(.+)",
            r"我的名字是(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip("。！，, ")
                return [self._build_memory(user_id, "name", value, "profile", 5)]
        return []

    def _extract_age(self, user_id: int, text: str) -> List[MemoryItem]:
        patterns = [
            r"我今年(\d{1,3})岁",
            r"我(\d{1,3})岁了",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1)
                return [self._build_memory(user_id, "age", value, "profile", 4)]
        return []

    def _extract_city(self, user_id: int, text: str) -> List[MemoryItem]:
        patterns = [
            r"我住在(.+)",
            r"我在(.+)工作",
            r"我在(.+)上班",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip("。！，, ")
                return [self._build_memory(user_id, "city", value, "profile", 4)]
        return []

    def _extract_preference(self, user_id: int, text: str) -> List[MemoryItem]:
        patterns = [
            (r"我喜欢(.+)", "like"),
            (r"我最喜欢(.+)", "favorite"),
            (r"我爱吃(.+)", "favorite_food"),
        ]

        for pattern, key in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip("。！，, ")
                return [self._build_memory(user_id, key, value, "preference", 3)]
        return []

    def _build_memory(
        self,
        user_id: int,
        key: str,
        value: str,
        memory_type: str,
        importance: int
    ) -> MemoryItem:
        return MemoryItem(
            id=None,
            user_id=user_id,
            key=key,
            value=value,
            type=memory_type,
            importance=importance,
            source="chat",
            status="active",
            created_at=None,
            updated_at=None
        )
