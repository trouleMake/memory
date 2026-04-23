from datetime import datetime
import os


BASE_DIR = os.path.abspath(os.getcwd())


def get_time():
    """Return the current local time."""
    now = datetime.now()
    return {
        "success": True,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": now.timestamp()
    }


def read_file(path):
    if not os.path.isabs(path):
        return {
            "success": False,
            "error": "path must be an absolute path"
        }

    target_path = os.path.abspath(path)

    if os.path.commonpath([BASE_DIR, target_path]) != BASE_DIR:
        return {
            "success": False,
            "error": "only files under the current project directory can be read"
        }

    if not os.path.exists(target_path):
        return {
            "success": False,
            "error": "file does not exist"
        }

    if not os.path.isfile(target_path):
        return {
            "success": False,
            "error": "path is not a file"
        }

    try:
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        return {
            "success": True,
            "path": target_path,
            "content": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


TOOL_MAP = {
    "get_time": get_time,
    "read_file": read_file
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current system time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file by absolute path, limited to the current project directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path of the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    }
]
