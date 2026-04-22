import json
from openai import OpenAI
from Util.api_key import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from tools import TOOLS, TOOL_MAP


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL
)


class AgentBrain:
    """Agent 的大脑，负责思考与决策"""

    def __init__(self, model="deepseek-chat"):
        self.model = model
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

    def think(self, prompt):
        """支持 tool call 的单轮思考"""
        try:
            self.messages.append({"role": "user", "content": prompt})

            # 第一次请求：让模型决定要不要调用工具
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # 1. 没有工具调用，直接返回文本
            if not message.tool_calls:
                reply = (message.content or "").strip()
                self.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                return reply

            # 2. 有工具调用：先把 assistant 的 tool_call 消息放进上下文
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

            # 3. 执行工具，并把结果回填
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
                    tool_func = TOOL_MAP[tool_name]
                    tool_result = tool_func(**tool_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

            # 4. 第二次请求：把 tool result 交回模型，让模型生成最终回答
            second_response = client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )

            final_reply = (second_response.choices[0].message.content or "").strip()
            self.messages.append({
                "role": "assistant",
                "content": final_reply
            })

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


def chat_loop():
    """命令行连续对话"""
    brain = AgentBrain()

    print("=== Agent 已启动 ===")
    print("输入 quit / exit 退出")
    print("输入 clear 清空上下文")
    print()

    while True:
        user_input = input("你：").strip()

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in {"quit", "exit"}:
            print("Agent：再见。")
            break

        if cmd == "clear":
            brain.clear_memory()
            print("Agent：上下文已清空。")
            print()
            continue

        reply = brain.think(user_input)
        print(f"Agent：{reply}")
        print()


if __name__ == "__main__":
    chat_loop()