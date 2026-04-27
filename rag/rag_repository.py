from __future__ import annotations

from typing import Any, Mapping

from rag.rag_item import RagItem
from rag.retrieval_plan import RetrievalPlan


class RagRepository:
    TABLE_NAME: str = "rag_document"
    DEFAULT_FIELDS: tuple[str, ...] = (
        "id",
        "user_id",
        "title",
        "content",
        "category",
        "tags",
        "source",
        "status",
        "created_at",
        "updated_at",
    )

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        charset: str = "utf8mb4",
    ) -> None:
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.database: str = database
        self.charset: str = charset

    def _get_connection(self) -> Any:
        raise NotImplementedError

    def search(self, plan: RetrievalPlan) -> list[RagItem]:
        raise NotImplementedError

    def _build_search_sql(self, plan: RetrievalPlan) -> tuple[str, tuple[Any, ...]]:
        raise NotImplementedError

    def _row_to_rag_item(self, row: Mapping[str, Any]) -> RagItem:
        raise NotImplementedError

    def _parse_tags(self, raw_tags: str | None) -> list[str]:
        raise NotImplementedError
