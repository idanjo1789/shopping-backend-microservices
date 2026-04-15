from datetime import datetime, timedelta, UTC

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import unauthorized
from app.model.current_user import CurrentUser
from app.repository.user_repository import UserRepository
from app.service.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.user_service = UserService()

    async def authenticate_user(self, username: str, password: str) -> dict:
        user = await self.user_repository.get_user_by_username(username)

        if not user:
            raise unauthorized("Invalid username or password")

        if not self.user_service.verify_password(password, user["hashed_password"]):
            raise unauthorized("Invalid username or password")

        if not user["is_active"]:
            raise unauthorized("User is inactive")

        return user

    def create_access_token(self, user: dict) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=settings.TOKEN_EXPIRY_TIME)

        payload = {
            "user_id": user["id"],
            "sub": user["username"],
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def get_current_user_id(self, token: str = Depends(oauth2_scheme)) -> int:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id = payload.get("user_id")
            if user_id is None:
                raise unauthorized("Invalid token")

            return int(user_id)

        except JWTError:
            raise unauthorized("Invalid token")

    async def validate_user(self, token: str = Depends(oauth2_scheme)) -> CurrentUser:
        user_id = self.get_current_user_id(token)

        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise unauthorized("User not found")

        return CurrentUser(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            phone=user["phone"],
            country=user["country"],
            city=user["city"],
            is_active=bool(user["is_active"]),
        )


auth_service = AuthService()