from __future__ import annotations

from rag.rag_item import RagItem
from rag.retrieval_plan import RetrievalPlan


class Ranker:
    DEFAULT_TITLE_WEIGHT: float = 3.0
    DEFAULT_TAG_WEIGHT: float = 2.0
    DEFAULT_CONTENT_WEIGHT: float = 1.0
    DEFAULT_RECENCY_WEIGHT: float = 1.0

    def __init__(
        self,
        title_weight: float = 3.0,
        tag_weight: float = 2.0,
        content_weight: float = 1.0,
        recency_weight: float = 1.0,
    ) -> None:
        self.title_weight: float = title_weight
        self.tag_weight: float = tag_weight
        self.content_weight: float = content_weight
        self.recency_weight: float = recency_weight

    def rank(self, items: list[RagItem], plan: RetrievalPlan) -> list[RagItem]:
        raise NotImplementedError

    def score(self, item: RagItem, plan: RetrievalPlan) -> float:
        raise NotImplementedError

    def _count_keyword_hits(self, text: str, keywords: list[str]) -> int:
        raise NotImplementedError

    def _calculate_recency_bonus(self, item: RagItem) -> float:
        raise NotImplementedError
