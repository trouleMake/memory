import json

from openai import OpenAI

from Util.api_key import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from Util.mysql_config import DB_CONFIG
from tools import TOOLS, TOOL_MAP

from memory.memory_extractor import MemoryExtractor
from memory.memory_repository import MemoryRepository
from memory.memory_service import MemoryService
from memory.prompt_memory_assembler import PromptMemoryAssembler


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL
)


class AgentBrain:
    def __init__(self, model="deepseek-chat", user_id=1):
        self.model = model
        self.user_id = user_id

        repository = MemoryRepository(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        extractor = MemoryExtractor()

        self.memory_service = MemoryService(extractor, repository)
        self.prompt_memory_assembler = PromptMemoryAssembler()

        self.messages = [
            {
                "role": "system",
                "content": (
                    "你是一个简洁、准确的 AI 助手。"
                    "当用户的问题需要获取当前时间时，优先调用工具。"
                    "拿到工具结果后，再用自然语言回答用户。"
                )
            }
        ]

    def think(self, prompt: str) -> str:
        try:
            # 1. 先查历史记忆，用于辅助当前回答
            memories = self.memory_service.get_relevant_memories(
                self.user_id,
                prompt,
                limit=5
            )
            enhanced_prompt = self.prompt_memory_assembler.assemble(memories, prompt)

            # 2. 用增强后的 prompt 让模型回答
            self.messages.append({"role": "user", "content": enhanced_prompt})

            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                reply = (message.content or "").strip()
                self.messages.append({"role": "assistant", "content": reply})

                # 3. 回答结束后，再把当前输入提取并保存为新记忆
                self.memory_service.extract_and_save(self.user_id, prompt)
                return reply

            self.messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args_str = tool_call.function.arguments or "{}"
                tool_args = json.loads(tool_args_str)

                if tool_name not in TOOL_MAP:
                    tool_result = {
                        "success": False,
                        "error": f"未知工具: {tool_name}"
                    }
                else:
                    tool_result = TOOL_MAP[tool_name](**tool_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

            second_response = client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )

            final_reply = (second_response.choices[0].message.content or "").strip()
            self.messages.append({"role": "assistant", "content": final_reply})

            # 4. 工具调用结束后，同样再保存当前轮输入中的新记忆
            self.memory_service.extract_and_save(self.user_id, prompt)
            return final_reply

        except Exception as e:
            return f"思考过程出错: {e}"

    def clear_memory(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "你是一个简洁、准确的 AI 助手。"
                    "当用户的问题需要获取当前时间时，优先调用工具。"
                    "拿到工具结果后，再用自然语言回答用户。"
                )
            }
        ]
