from typing import Optional, List
from decimal import Decimal

from app.model.order import Order
from app.repository.database import database

TABLE_NAME = "orders"


async def get_by_id(order_id: int) -> Optional[Order]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE id = :order_id
    """
    result = await database.fetch_one(query=query, values={"order_id": order_id})
    return Order(**result) if result else None


async def get_temp_by_user_id(user_id: int) -> Optional[Order]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE user_id = :user_id
          AND status = 'TEMP'
        LIMIT 1
    """
    result = await database.fetch_one(query=query, values={"user_id": user_id})
    return Order(**result) if result else None


async def get_closed_by_user_id(user_id: int) -> List[Order]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE user_id = :user_id
          AND status = 'CLOSE'
        ORDER BY id DESC
    """
    results = await database.fetch_all(query=query, values={"user_id": user_id})
    return [Order(**result) for result in results]


async def create_temp_order(user_id: int) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (
            user_id,
            status,
            total_price
        )
        VALUES (
            :user_id,
            'TEMP',
            :total_price
        )
    """

    async with database.transaction():
        await database.execute(
            query=query,
            values={
                "user_id": user_id,
                "total_price": Decimal("0.00"),
            },
        )
        result = await database.fetch_one("SELECT LAST_INSERT_ID() AS id")

    return result["id"]


async def update_total_price(order_id: int, total_price: Decimal) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET total_price = :total_price
        WHERE id = :order_id
    """
    await database.execute(
        query=query,
        values={
            "order_id": order_id,
            "total_price": total_price,
        },
    )


async def close_order(order_id: int, total_price: Decimal) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET status = 'CLOSE',
            total_price = :total_price
        WHERE id = :order_id
          AND status = 'TEMP'
    """
    await database.execute(
        query=query,
        values={
            "order_id": order_id,
            "total_price": total_price,
        },
    )


async def delete_order(order_id: int) -> None:
    query = f"""
        DELETE FROM {TABLE_NAME}
        WHERE id = :order_id
    """
    await database.execute(query=query, values={"order_id": order_id})