from databases import Database
from app.config import settings

database = Database(settings.DATABASE_URL)


async def connect_db() -> None:
    if not database.is_connected:
        await database.connect()


async def disconnect_db() -> None:
    if database.is_connected:
        await database.disconnect()