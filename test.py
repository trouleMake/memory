from memory.memory_repository import MemoryRepository
from Util.mysql_config import DB_CONFIG2

memory_reop=MemoryRepository(**DB_CONFIG2)

ans=memory_reop.find_by_user_id(1)

print(ans)