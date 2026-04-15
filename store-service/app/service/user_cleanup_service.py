from app.repository.database import database
from app.repository import user_cleanup_repository


async def delete_all_user_data(user_id: int) -> dict:
    async with database.transaction():
        await user_cleanup_repository.delete_user_favorites(user_id)
        await user_cleanup_repository.delete_user_chat_sessions(user_id)
        await user_cleanup_repository.delete_user_orders(user_id)

    return {
        "message": "All user data deleted from store service",
        "user_id": user_id,
    }