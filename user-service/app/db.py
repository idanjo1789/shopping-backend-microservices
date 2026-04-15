from databases import Database
from app.config import settings
import asyncio

DATABASE_URL = settings.DATABASE_URL
database = Database(DATABASE_URL)


async def connect_with_retry(database_instance: Database, retries: int = 5, delay: int = 2):
    for i in range(retries):
        try:
            if not database_instance.is_connected:
                await database_instance.connect()
            print("DB connected")
            return
        except Exception as e:
            print(f"DB connection failed (attempt {i + 1}/{retries}): {e}")
            await asyncio.sleep(delay)

    raise Exception("DB connection failed after retries")