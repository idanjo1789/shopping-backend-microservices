from fastapi import APIRouter, Depends, status

from app.model.current_user import CurrentUser
from app.model.user_request import UserRequest
from app.model.user_response import UserResponse
from app.service.auth_service import auth_service
from app.service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    user_id = await user_service.create_user(user_request)
    return {"user_id": user_id}


@router.get("", response_model=list[UserResponse])
async def get_users(current_user: CurrentUser = Depends(auth_service.validate_user)):
    users = await user_service.get_users()
    return [UserResponse(**user) for user in users]


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser = Depends(auth_service.validate_user)):
    return UserResponse(**current_user.dict())


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: CurrentUser = Depends(auth_service.validate_user)
):
    user = await user_service.get_user_by_id(user_id)
    return UserResponse(**user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: CurrentUser = Depends(auth_service.validate_user)
):
    await user_service.delete_user(user_id)
    return None