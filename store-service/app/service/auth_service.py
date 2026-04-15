from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.exceptions import unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:

    def get_current_user_id(self, token: str = Depends(oauth2_scheme)) -> int:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

        except ExpiredSignatureError:
            unauthorized("Token expired")

        except JWTError:
            unauthorized("Invalid token")

        user_id = payload.get("user_id")

        if user_id is None:
            unauthorized("Invalid token payload")

        try:
            return int(user_id)

        except (TypeError, ValueError):
            unauthorized("Invalid user_id in token")


auth_service = AuthService()