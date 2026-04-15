from typing import Optional, List

from app.exceptions import not_found, bad_request
from app.model.item import Item
from app.repository import items_repository

VALID_OPERATORS = {"lt", "gt", "eq"}


async def get_item_by_id(item_id: int) -> Item:
    item = await items_repository.get_by_id(item_id)

    if not item:
        raise not_found("Item not found")

    return item


async def get_items() -> List[Item]:
    return await items_repository.get_all()


async def create_item(item: Item) -> dict:
    if item.price is None or item.price < 0:
        raise bad_request("Invalid price")

    if item.stock is None or item.stock < 0:
        raise bad_request("Invalid stock")

    item_id = await items_repository.create_item(item)
    return {"id": item_id}


async def update_item(item_id: int, item: Item) -> dict:
    existing_item = await items_repository.get_by_id(item_id)

    if not existing_item:
        raise not_found("Item not found")

    if item.price is None or item.price < 0:
        raise bad_request("Invalid price")

    if item.stock is None or item.stock < 0:
        raise bad_request("Invalid stock")

    await items_repository.update_item(item_id, item)
    return {"message": "Item updated successfully"}


async def delete_item(item_id: int) -> dict:
    existing_item = await items_repository.get_by_id(item_id)

    if not existing_item:
        raise not_found("Item not found")

    await items_repository.soft_delete_item(item_id)
    return {"message": "Item deleted successfully"}


async def search_items(
    name: Optional[str] = None,
    price_op: Optional[str] = None,
    price_value: Optional[float] = None,
    stock_op: Optional[str] = None,
    stock_value: Optional[int] = None,
) -> List[Item]:
    if price_op is not None and price_op not in VALID_OPERATORS:
        raise bad_request("Invalid price_op. Use: lt | gt | eq")

    if stock_op is not None and stock_op not in VALID_OPERATORS:
        raise bad_request("Invalid stock_op. Use: lt | gt | eq")

    if price_value is not None and price_value < 0:
        raise bad_request("Invalid price_value")

    if stock_value is not None and stock_value < 0:
        raise bad_request("Invalid stock_value")

    if price_op and price_value is None:
        raise bad_request("price_value is required when price_op is used")

    if stock_op and stock_value is None:
        raise bad_request("stock_value is required when stock_op is used")

    return await items_repository.search_items(
        name=name,
        price_op=price_op,
        price_value=price_value,
        stock_op=stock_op,
        stock_value=stock_value,
    )