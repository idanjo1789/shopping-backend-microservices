from typing import List, Optional

from fastapi import APIRouter, Path, Query
from starlette import status

from app.model.item import Item
from app.service import items_service

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Item])
async def get_items():
    return await items_service.get_items()


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[Item])
async def search_items(
    name: Optional[str] = Query(default=None),
    price_op: Optional[str] = Query(default=None),
    price_value: Optional[float] = Query(default=None),
    stock_op: Optional[str] = Query(default=None),
    stock_value: Optional[int] = Query(default=None),
):
    return await items_service.search_items(
        name=name,
        price_op=price_op,
        price_value=price_value,
        stock_op=stock_op,
        stock_value=stock_value,
    )


@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=Item)
async def get_item_by_id(item_id: int = Path(gt=0)):
    return await items_service.get_item_by_id(item_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return await items_service.create_item(item)


@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item: Item, item_id: int = Path(gt=0)):
    return await items_service.update_item(item_id, item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int = Path(gt=0)):
    return await items_service.delete_item(item_id)