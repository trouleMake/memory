from __future__ import annotations

from rag.prompt_rag_assembler import PromptRagAssembler
from rag.query_rewriter import QueryRewriter
from rag.rag_item import RagItem
from rag.rag_repository import RagRepository
from rag.ranker import Ranker
from rag.retrieval_plan import RetrievalPlan


class RagService:
    def __init__(
        self,
        query_rewriter: QueryRewriter,
        repository: RagRepository,
        ranker: Ranker,
        prompt_assembler: PromptRagAssembler,
    ) -> None:
        self.query_rewriter: QueryRewriter = query_rewriter
        self.repository: RagRepository = repository
        self.ranker: Ranker = ranker
        self.prompt_assembler: PromptRagAssembler = prompt_assembler

    def build_plan(
        self,
        user_query: str,
        user_id: int | None = None,
        limit: int | None = None,
    ) -> RetrievalPlan:
        raise NotImplementedError

    def retrieve(
        self,
        user_query: str,
        user_id: int | None = None,
        limit: int | None = None,
    ) -> list[RagItem]:
        raise NotImplementedError

    def retrieve_and_assemble(
        self,
        user_query: str,
        user_id: int | None = None,
        limit: int | None = None,
    ) -> str:
        raise NotImplementedError
