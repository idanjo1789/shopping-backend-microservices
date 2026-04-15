from typing import Optional, List

from app.model.customer_favorite_item import CustomerFavoriteItem
from app.repository.database import database

TABLE_NAME = "customer_favorite_item"


async def get_by_id(favorite_id: int) -> Optional[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id=:favorite_id"
    result = await database.fetch_one(query, values={"favorite_id": favorite_id})
    return CustomerFavoriteItem(**result) if result else None


async def get_by_user_id(user_id: int) -> List[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id ORDER BY id DESC"
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [CustomerFavoriteItem(**r) for r in results]


async def get_by_user_id_and_item_id(user_id: int, item_id: int) -> Optional[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id AND item_id=:item_id"
    result = await database.fetch_one(query, values={"user_id": user_id, "item_id": item_id})
    return CustomerFavoriteItem(**result) if result else None


async def create_favorite(user_id: int, item_id: int) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (user_id, item_id)
        VALUES (:user_id, :item_id)
    """
    async with database.transaction():
        await database.execute(query, values={"user_id": user_id, "item_id": item_id})
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]


async def delete_by_user_id_and_item_id(user_id: int, item_id: int) -> None:
    query = f"DELETE FROM {TABLE_NAME} WHERE user_id=:user_id AND item_id=:item_id"
    await database.execute(query, values={"user_id": user_id, "item_id": item_id})