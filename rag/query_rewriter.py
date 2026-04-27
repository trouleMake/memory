from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rag.retrieval_plan import RetrievalPlan


class QueryRewriter:
    DEFAULT_RULES_PATH: Path = Path(__file__).resolve().parent.parent / "Util" / "rewrite_rules.json"

    def __init__(
        self,
        rules_path: str | Path | None = None,
        default_limit: int = 5,
        default_sort_hint: str = "relevance",
    ) -> None:
        self.rules_path: Path = Path(rules_path) if rules_path is not None else self.DEFAULT_RULES_PATH
        self.default_limit: int = default_limit
        self.default_sort_hint: str = default_sort_hint
        self.rules: dict[str, Any] = self._load_rules()

        self.stopwords: list[str] = self.rules.get("stopwords", [])
        self.punctuation: list[str] = self.rules.get("punctuation", [])
        self.synonyms: dict[str, list[str]] = self.rules.get("synonyms", {})
        self.category_rules: dict[str, list[str]] = self.rules.get("category_rules", {})
        self.sort_rules: dict[str, list[str]] = self.rules.get("sort_rules", {})
        self.keyword_blacklist: list[str] = self.rules.get("keyword_blacklist", [])
        self.phrase_whitelist: list[str] = self.rules.get("phrase_whitelist", [])
        self.default_filters: dict[str, Any] = self.rules.get("default_filters", {})
        self.rule_default_limit: int = int(self.rules.get("default_limit", self.default_limit))
        self.rule_default_sort_hint: str = str(
            self.rules.get("default_sort_hint", self.default_sort_hint)
        )

    def rewrite(
        self,
        user_query: str,
        user_id: int | None = None,
        limit: int | None = None,
    ) -> RetrievalPlan:
        normalized_query = self._normalize_query(user_query)
        cleaned_query = self._remove_stopwords(normalized_query)

        sort_hint = self._infer_sort_hint(normalized_query)
        filters = self._infer_filters(normalized_query)

        keywords = self._extract_keywords(cleaned_query)
        keywords = self._expand_keywords(keywords)
        keywords = self._deduplicate_keywords(keywords)

        search_text = self._build_search_text(cleaned_query, keywords)
        final_limit = limit if limit is not None else self.rule_default_limit

        return RetrievalPlan(
            user_query=user_query,
            search_text=search_text,
            keywords=keywords,
            filters=filters,
            sort_hint=sort_hint,
            limit=final_limit,
            user_id=user_id,
        )

    def _load_rules(self) -> dict[str, Any]:
        raise NotImplementedError

    def _normalize_query(self, user_query: str) -> str:
        #转为小写，去空格，统一标点
        raise NotImplementedError

    def _remove_stopwords(self, normalized_query: str) -> str:
        raise NotImplementedError

    def _infer_filters(self, normalized_query: str) -> dict[str, Any]:

        raise NotImplementedError

    def _infer_category(self, normalized_query: str) -> str | None:
        # 根据 category_rules 推断分类
        raise NotImplementedError

    def _infer_sort_hint(self, normalized_query: str) -> str:
        raise NotImplementedError

    def _extract_keywords(self, cleaned_query: str) -> list[str]:
        raise NotImplementedError

    def _expand_keywords(self, keywords: list[str]) -> list[str]:
        raise NotImplementedError

    def _deduplicate_keywords(self, keywords: list[str]) -> list[str]:
        raise NotImplementedError

    def _build_search_text(self, cleaned_query: str, keywords: list[str]) -> str:
        raise NotImplementedError
