from __future__ import annotations

from typing import List

from memory_item import MemoryItem


class PromptMemoryAssembler:
        def assemble(self, memories: List[MemoryItem], user_query: str) -> str:
            if not memories:
                return user_query

            memory_lines = []
            for memory in memories:
                memory_lines.append(
                    f"- {memory.key}: {memory.value} "
                    f"(type={memory.type}, importance={memory.importance})"
                )

            memory_text = "\n".join(memory_lines)

            return (
                "以下是该用户的相关记忆，请在回答时作为参考。\n"
                "如果记忆与当前问题无关，就不要强行使用。\n\n"
                f"{memory_text}\n\n"
                f"用户当前问题：{user_query}"
            )