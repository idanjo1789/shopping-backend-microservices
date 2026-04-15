from typing import Dict, Any, List

from app.exceptions import bad_request, not_found_exception, conflict_exception
from app.model.order_item_request import AddOrderItemRequest
from app.repository import (
    orders_repository,
    order_items_repository,
    items_stock_repository,
)
from app.repository.database import database


async def _get_or_create_temp_order(user_id: int) -> int:
    order = await orders_repository.get_temp_by_user_id(user_id)

    if order:
        return order.id

    return await orders_repository.create_temp_order(user_id)


async def _build_order_response(order) -> Dict[str, Any]:
    items = await order_items_repository.get_detailed_items_by_order_id(order.id)
    total = await order_items_repository.calc_total_price(order.id)

    await orders_repository.update_total_price(order.id, total)

    return {
        "order": {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_price": float(total),
        },
        "items": items,
    }


async def create_or_get_temp_order(user_id: int) -> Dict[str, Any]:
    order_id = await _get_or_create_temp_order(user_id)
    order = await orders_repository.get_by_id(order_id)

    if not order:
        raise not_found_exception("Order not found")

    return await _build_order_response(order)


async def get_temp_order(user_id: int) -> Dict[str, Any]:
    order = await orders_repository.get_temp_by_user_id(user_id)

    if not order:
        raise not_found_exception("TEMP order not found")

    return await _build_order_response(order)


async def get_orders_history(user_id: int) -> List[Dict[str, Any]]:
    orders = await orders_repository.get_closed_by_user_id(user_id)
    response: List[Dict[str, Any]] = []

    for order in orders:
        items = await order_items_repository.get_detailed_items_by_order_id(order.id)

        response.append(
            {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "total_price": float(order.total_price),
                "items": items,
            }
        )

    return response


async def add_item_to_temp_order(user_id: int, req: AddOrderItemRequest) -> Dict[str, Any]:
    if req.quantity <= 0:
        raise bad_request("Invalid quantity")

    row = await items_stock_repository.get_stock_and_price(req.item_id)

    if not row or row["is_active"] != 1:
        raise not_found_exception("Item not found")

    stock = int(row["stock"])
    unit_price = row["price"]

    if stock <= 0:
        raise conflict_exception("Item is out of stock")

    order_id = await _get_or_create_temp_order(user_id)

    existing_item = await order_items_repository.get_by_order_id_and_item_id(
        order_id,
        req.item_id,
    )
    current_quantity = existing_item.quantity if existing_item else 0
    new_total_quantity = current_quantity + req.quantity

    if new_total_quantity > stock:
        raise conflict_exception("Not enough stock")

    await order_items_repository.upsert_item(
        order_id=order_id,
        item_id=req.item_id,
        quantity=req.quantity,
        unit_price=unit_price,
    )

    order = await orders_repository.get_by_id(order_id)

    if not order:
        raise not_found_exception("Order not found")

    return await _build_order_response(order)


async def update_item_quantity_in_temp_order(user_id: int, req: AddOrderItemRequest) -> Dict[str, Any]:
    if req.quantity <= 0:
        raise bad_request("Invalid quantity")

    order = await orders_repository.get_temp_by_user_id(user_id)

    if not order:
        raise not_found_exception("TEMP order not found")

    existing_item = await order_items_repository.get_by_order_id_and_item_id(order.id, req.item_id)

    if not existing_item:
        raise not_found_exception("Item not found in TEMP order")

    row = await items_stock_repository.get_stock_and_price(req.item_id)

    if not row or row["is_active"] != 1:
        raise not_found_exception("Item not found")

    stock = int(row["stock"])
    unit_price = row["price"]

    if stock <= 0:
        raise conflict_exception("Item is out of stock")

    if req.quantity > stock:
        raise conflict_exception("Not enough stock")

    await order_items_repository.set_quantity(
        order_id=order.id,
        item_id=req.item_id,
        quantity=req.quantity,
        unit_price=unit_price,
    )

    return await _build_order_response(order)


async def remove_item_from_temp_order(user_id: int, item_id: int) -> Dict[str, Any]:
    order = await orders_repository.get_temp_by_user_id(user_id)

    if not order:
        raise not_found_exception("TEMP order not found")

    existing_item = await order_items_repository.get_by_order_id_and_item_id(order.id, item_id)

    if not existing_item:
        raise not_found_exception("Item not found in TEMP order")

    await order_items_repository.delete_item(order.id, item_id)

    remaining_items = await order_items_repository.get_by_order_id(order.id)

    if not remaining_items:
        await orders_repository.delete_order(order.id)
        return {
            "message": "TEMP order deleted because it became empty",
            "order_deleted": True,
        }

    return await _build_order_response(order)


async def close_temp_order(user_id: int) -> Dict[str, Any]:
    order = await orders_repository.get_temp_by_user_id(user_id)

    if not order:
        raise not_found_exception("TEMP order not found")

    items = await order_items_repository.get_by_order_id(order.id)

    if not items:
        raise bad_request("Cannot close empty order")

    async with database.transaction():
        for order_item in items:
            row = await items_stock_repository.get_stock_and_price(order_item.item_id)

            if not row or row["is_active"] != 1:
                raise not_found_exception("Item not found")

            if int(row["stock"]) < order_item.quantity:
                raise conflict_exception("Not enough stock for purchase")

            await items_stock_repository.reduce_stock(
                order_item.item_id,
                order_item.quantity,
            )

        total = await order_items_repository.calc_total_price(order.id)
        await orders_repository.close_order(order.id, total)

    return {
        "order_id": order.id,
        "status": "CLOSE",
        "total_price": float(total),
    }