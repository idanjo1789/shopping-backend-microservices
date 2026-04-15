from app.exceptions import conflict_exception, not_found_exception
from app.repository.database import database

TABLE_NAME = "items"


async def get_stock_and_price(item_id: int):
    query = f"""
        SELECT id, stock, price, is_active
        FROM {TABLE_NAME}
        WHERE id = :item_id
    """
    return await database.fetch_one(query, values={"item_id": item_id})


async def reduce_stock(item_id: int, quantity: int) -> None:
    row = await database.fetch_one(
        f"""
        SELECT stock, is_active
        FROM {TABLE_NAME}
        WHERE id = :item_id
        """,
        values={"item_id": item_id},
    )

    if not row or row["is_active"] != 1:
        raise not_found_exception("Item not found")

    if int(row["stock"]) < quantity:
        raise conflict_exception("Not enough stock")

    await database.execute(
        f"""
        UPDATE {TABLE_NAME}
        SET stock = stock - :quantity
        WHERE id = :item_id
        """,
        values={"item_id": item_id, "quantity": quantity},
    )

    updated_row = await database.fetch_one(
        f"SELECT stock FROM {TABLE_NAME} WHERE id = :item_id",
        values={"item_id": item_id},
    )

    if not updated_row:
        raise not_found_exception("Item not found after update")

    if int(updated_row["stock"]) < 0:
        raise conflict_exception("Stock inconsistency detected")