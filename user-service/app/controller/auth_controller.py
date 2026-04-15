from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.model.auth_response import AuthResponse
from app.model.current_user import CurrentUser
from app.service.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(
        form_data.username,
        form_data.password
    )

    access_token = auth_service.create_access_token(user)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/me", response_model=CurrentUser)
async def get_me(current_user: CurrentUser = Depends(auth_service.validate_user)):
    return current_user