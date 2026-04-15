from fastapi import APIRouter, Depends

from app.service.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(user_id: int = Depends(auth_service.get_current_user_id)):
    return {"user_id": user_id}