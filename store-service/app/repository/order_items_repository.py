from typing import Optional, List, Dict, Any
from decimal import Decimal

from app.model.order_item import OrderItem
from app.repository.database import database

TABLE_NAME = "order_items"


async def get_by_order_id(order_id: int) -> List[OrderItem]:
    query = f"""
        SELECT * FROM {TABLE_NAME}
        WHERE order_id=:order_id
        ORDER BY id DESC
    """
    results = await database.fetch_all(query, values={"order_id": order_id})
    return [OrderItem(**result) for result in results]


async def get_detailed_items_by_order_id(order_id: int) -> List[Dict[str, Any]]:
    query = f"""
        SELECT
            oi.item_id,
            oi.quantity,
            oi.unit_price AS price,
            i.name,
            i.description,
            i.stock,
            i.is_active
        FROM {TABLE_NAME} oi
        JOIN items i ON i.id = oi.item_id
        WHERE oi.order_id=:order_id
        ORDER BY oi.id DESC
    """
    results = await database.fetch_all(query, values={"order_id": order_id})
    return [dict(result) for result in results]


async def get_by_order_id_and_item_id(order_id: int, item_id: int) -> Optional[OrderItem]:
    query = f"""
        SELECT * FROM {TABLE_NAME}
        WHERE order_id=:order_id AND item_id=:item_id
    """
    result = await database.fetch_one(
        query,
        values={"order_id": order_id, "item_id": item_id},
    )
    return OrderItem(**result) if result else None


async def upsert_item(order_id: int, item_id: int, quantity: int, unit_price: Decimal) -> None:
    query = f"""
        INSERT INTO {TABLE_NAME} (order_id, item_id, quantity, unit_price)
        VALUES (:order_id, :item_id, :quantity, :unit_price)
        ON DUPLICATE KEY UPDATE
            quantity = quantity + VALUES(quantity),
            unit_price = VALUES(unit_price)
    """
    await database.execute(
        query,
        values={
            "order_id": order_id,
            "item_id": item_id,
            "quantity": quantity,
            "unit_price": unit_price,
        },
    )


async def set_quantity(order_id: int, item_id: int, quantity: int, unit_price: Decimal) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET quantity=:quantity,
            unit_price=:unit_price
        WHERE order_id=:order_id AND item_id=:item_id
    """
    await database.execute(
        query,
        values={
            "order_id": order_id,
            "item_id": item_id,
            "quantity": quantity,
            "unit_price": unit_price,
        },
    )


async def delete_item(order_id: int, item_id: int) -> None:
    query = f"""
        DELETE FROM {TABLE_NAME}
        WHERE order_id=:order_id AND item_id=:item_id
    """
    await database.execute(query, values={"order_id": order_id, "item_id": item_id})


async def calc_total_price(order_id: int) -> Decimal:
    query = f"""
        SELECT COALESCE(SUM(quantity * unit_price), 0) AS total
        FROM {TABLE_NAME}
        WHERE order_id=:order_id
    """
    result = await database.fetch_one(query, values={"order_id": order_id})
    return result["total"] if result else Decimal("0.00")