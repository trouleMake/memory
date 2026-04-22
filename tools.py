from datetime import datetime


def get_time():
    """返回当前本地时间"""
    now = datetime.now()
    return {
        "success": True,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": now.timestamp()
    }


TOOL_MAP = {
    "get_time": get_time
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前系统时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]