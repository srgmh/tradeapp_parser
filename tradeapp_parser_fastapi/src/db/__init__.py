from src.db.database_manager import DatabaseManager
from src.db.mongodb_manager import MongoManager

db = MongoManager()


async def get_database() -> DatabaseManager:
    return db
