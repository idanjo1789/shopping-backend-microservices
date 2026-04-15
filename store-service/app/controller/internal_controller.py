from fastapi import APIRouter, Header, status

from app.config import settings
from app.exceptions import unauthorized
from app.service import user_cleanup_service

router = APIRouter(prefix="/internal", tags=["internal"])


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_data(
    user_id: int,
    x_internal_secret: str | None = Header(default=None),
):
    if x_internal_secret != settings.SECRET_KEY:
        raise unauthorized("Invalid internal secret")

    return await user_cleanup_service.delete_all_user_data(user_id)