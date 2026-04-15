from starlette import status
from fastapi import APIRouter, Depends, Path

from app.model.order_item_request import AddOrderItemRequest
from app.service import orders_service
from app.service.auth_service import auth_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/temp", status_code=status.HTTP_201_CREATED)
async def create_or_get_temp_order(
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.create_or_get_temp_order(user_id)


@router.get("/temp", status_code=status.HTTP_200_OK)
async def get_temp_order(
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.get_temp_order(user_id)


@router.get("/history", status_code=status.HTTP_200_OK)
async def get_orders_history(
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.get_orders_history(user_id)


@router.post("/temp/items", status_code=status.HTTP_200_OK)
async def add_item(
    req: AddOrderItemRequest,
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.add_item_to_temp_order(user_id, req)


@router.post("/temp/items/update", status_code=status.HTTP_200_OK)
async def update_item_quantity(
    req: AddOrderItemRequest,
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.update_item_quantity_in_temp_order(user_id, req)


@router.delete("/temp/items/{item_id}", status_code=status.HTTP_200_OK)
async def remove_item(
    item_id: int = Path(gt=0),
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.remove_item_from_temp_order(user_id, item_id)


@router.post("/temp/close", status_code=status.HTTP_200_OK)
async def close_order(
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await orders_service.close_temp_order(user_id)