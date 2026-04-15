from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.service.auth_service import auth_service
from app.repository.favorites_repository import FavoritesRepository

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteRequest(BaseModel):
    item_id: int


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    request: FavoriteRequest,
    user_id: int = Depends(auth_service.get_current_user_id)
):
    await FavoritesRepository.add_favorite(user_id, request.item_id)
    return {"message": "Added to favorites"}


@router.get("")
async def get_favorites(
    user_id: int = Depends(auth_service.get_current_user_id)
):
    return await FavoritesRepository.list_favorites(user_id)


@router.delete("/{item_id}")
async def remove_favorite(
    item_id: int,
    user_id: int = Depends(auth_service.get_current_user_id)
):
    await FavoritesRepository.remove_favorite(user_id, item_id)
    return {"message": "Removed from favorites"}