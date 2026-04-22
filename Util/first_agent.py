# brain.py
from openai import OpenAI
from Util.api_key import DEEPSEEK_API_KEY,DEEPSEEK_API_URL



client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL)


class AgentBrain:
    """Agent 的大脑，负责思考与决策"""

    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.messages = [
            {"role": "system", "content": "你是一个简洁、准确的 AI 助手。"}
        ]

    def think(self, prompt):
        """单轮思考：接收用户输入，返回模型回复"""
        try:
            self.messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.5,  # 控制创造性，越低越专注
                max_tokens=500  # 控制回复长度
            )
            # 提取模型返回的文本内容（v1.x 版本属性路径变更）
            reply=response.choices[0].message.content.strip()
            self.messages.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"思考过程出错: {e}"

    def clear_memory(self):
        self.messages = [
            {"role": "system", "content": "你是一个简洁、准确的 AI 助手。"}
        ]

def chat_loop():
        """命令行连续对话"""
        brain = AgentBrain()

        print("=== Agent 已启动 ===")
        print("输入 quit / exit 退出")
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

# 简单测试一下大脑是否工作
if __name__ == "__main__":
    chat_loop()