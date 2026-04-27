from __future__ import annotations

from rag.rag_item import RagItem


class PromptRagAssembler:
    DEFAULT_MAX_ITEMS: int = 5
    DEFAULT_MAX_CONTENT_CHARS: int = 500

    def __init__(
        self,
        max_items: int = 5,
        max_content_chars: int = 500,
    ) -> None:
        self.max_items: int = max_items
        self.max_content_chars: int = max_content_chars

    def assemble(self, items: list[RagItem], user_query: str) -> str:
        raise NotImplementedError

    def _format_item(self, item: RagItem, index: int) -> str:
        raise NotImplementedError

    def _truncate_content(self, content: str) -> str:
        raise NotImplementedError
