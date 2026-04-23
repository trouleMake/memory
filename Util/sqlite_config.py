from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DB_PATH = PROJECT_ROOT / "memory.db"


def get_memory_db_path() -> str:
    return str(MEMORY_DB_PATH)
