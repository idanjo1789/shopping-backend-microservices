from app.repository.database import database


async def delete_user_favorites(user_id: int) -> None:
    query = """
    DELETE FROM customer_favorite_item
    WHERE user_id = :user_id
    """
    await database.execute(query=query, values={"user_id": user_id})


async def delete_user_chat_sessions(user_id: int) -> None:
    query = """
    DELETE FROM chat_sessions
    WHERE user_id = :user_id
    """
    await database.execute(query=query, values={"user_id": user_id})


async def delete_user_orders(user_id: int) -> None:
    query = """
    DELETE FROM orders
    WHERE user_id = :user_id
    """
    await database.execute(query=query, values={"user_id": user_id})