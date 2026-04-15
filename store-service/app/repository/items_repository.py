from typing import Optional, List, Dict, Any

from app.model.item import Item
from app.repository.database import database

TABLE_NAME = "items"


async def get_by_id(item_id: int) -> Optional[Item]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE id = :item_id
          AND is_active = :is_active
    """
    result = await database.fetch_one(
        query=query,
        values={
            "item_id": item_id,
            "is_active": 1,
        },
    )
    return Item(**result) if result else None


async def get_all() -> List[Item]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE is_active = :is_active
        ORDER BY id DESC
    """
    results = await database.fetch_all(
        query=query,
        values={"is_active": 1},
    )
    return [Item(**result) for result in results]


async def create_item(item: Item) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (
            name,
            description,
            price,
            stock,
            is_active
        )
        VALUES (
            :name,
            :description,
            :price,
            :stock,
            :is_active
        )
    """

    values = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "stock": item.stock,
        "is_active": 1 if item.is_active else 0,
    }

    async with database.transaction():
        await database.execute(query=query, values=values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID() AS id")

    return last_record_id["id"]


async def update_item(item_id: int, item: Item) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET
            name = :name,
            description = :description,
            price = :price,
            stock = :stock,
            is_active = :is_active
        WHERE id = :item_id
    """

    values = {
        "item_id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "stock": item.stock,
        "is_active": 1 if item.is_active else 0,
    }

    await database.execute(query=query, values=values)


async def soft_delete_item(item_id: int) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET is_active = 0
        WHERE id = :item_id
    """
    await database.execute(query=query, values={"item_id": item_id})


async def search_items(
    name: Optional[str] = None,
    price_op: Optional[str] = None,
    price_value: Optional[float] = None,
    stock_op: Optional[str] = None,
    stock_value: Optional[int] = None,
) -> List[Item]:
    where_clauses = ["is_active = :is_active"]
    values: Dict[str, Any] = {"is_active": 1}

    if name:
        raw_keywords = [part.strip() for part in name.split(",") if part.strip()]

        if not raw_keywords:
            raw_keywords = [name.strip()]

        keyword_clauses = []

        for index, keyword in enumerate(raw_keywords):
            param_name = f"name_kw_{index}"
            keyword_clauses.append(f"name LIKE :{param_name}")
            values[param_name] = f"%{keyword}%"

        if keyword_clauses:
            where_clauses.append(f"({' OR '.join(keyword_clauses)})")

    operator_map = {
        "lt": "<",
        "gt": ">",
        "eq": "=",
    }

    if price_op and price_value is not None:
        where_clauses.append(f"price {operator_map[price_op]} :price_value")
        values["price_value"] = price_value

    if stock_op and stock_value is not None:
        where_clauses.append(f"stock {operator_map[stock_op]} :stock_value")
        values["stock_value"] = stock_value

    where_sql = " AND ".join(where_clauses)

    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE {where_sql}
        ORDER BY id DESC
    """

    results = await database.fetch_all(query=query, values=values)
    return [Item(**result) for result in results]