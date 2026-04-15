from typing import Optional

from app.repository.database import database

TABLE_NAME = "chat_sessions"


async def get_active_session(user_id: int, session_key: str) -> Optional[dict]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE user_id = :user_id
          AND session_key = :session_key
          AND is_active = 1
        LIMIT 1
    """
    return await database.fetch_one(
        query=query,
        values={
            "user_id": user_id,
            "session_key": session_key,
        },
    )


async def create_session(user_id: int, session_key: str) -> dict:
    insert_query = f"""
        INSERT INTO {TABLE_NAME} (
            user_id,
            session_key,
            prompts_used,
            max_prompts,
            is_active
        )
        VALUES (
            :user_id,
            :session_key,
            0,
            5,
            1
        )
    """

    await database.execute(
        query=insert_query,
        values={
            "user_id": user_id,
            "session_key": session_key,
        },
    )

    return await get_active_session(user_id, session_key)


async def increment_prompts(session_id: int) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET prompts_used = prompts_used + 1
        WHERE id = :session_id
    """
    await database.execute(query=query, values={"session_id": session_id})


async def reset_session(user_id: int, session_key: str) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET prompts_used = 0,
            is_active = 1
        WHERE user_id = :user_id
          AND session_key = :session_key
    """
    await database.execute(
        query=query,
        values={
            "user_id": user_id,
            "session_key": session_key,
        },
    )