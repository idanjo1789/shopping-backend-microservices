from typing import Any
from app.repository.database import database


class FavoritesRepository:
    @staticmethod
    async def add_favorite(user_id: int, item_id: int) -> None:
        query = """
        INSERT INTO customer_favorite_item (user_id, item_id)
        VALUES (:user_id, :item_id)
        """
        await database.execute(query=query, values={"user_id": user_id, "item_id": item_id})

    @staticmethod
    async def remove_favorite(user_id: int, item_id: int) -> None:
        query = """
        DELETE FROM customer_favorite_item
        WHERE user_id = :user_id AND item_id = :item_id
        """
        await database.execute(query=query, values={"user_id": user_id, "item_id": item_id})

    @staticmethod
    async def list_favorites(user_id: int) -> list[dict[str, Any]]:
        query = """
        SELECT i.*
        FROM customer_favorite_item f
        JOIN items i ON i.id = f.item_id
        WHERE f.user_id = :user_id
        ORDER BY f.id DESC
        """
        rows = await database.fetch_all(query=query, values={"user_id": user_id})
        return [dict(r) for r in rows]