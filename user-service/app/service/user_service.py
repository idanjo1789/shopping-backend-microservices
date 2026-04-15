from passlib.context import CryptContext

from app.exceptions import (
    email_taken_exception,
    user_not_found_exception,
    username_taken_exception,
)
from app.model.user_request import UserRequest
from app.repository.user_repository import UserRepository
from app.service.store_service_client import delete_user_data_in_store_service


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, user_request: UserRequest) -> int:
        existing_user = await self.user_repository.get_user_by_username(user_request.username)
        if existing_user:
            raise username_taken_exception()

        existing_email = await self.user_repository.get_user_by_email(user_request.email)
        if existing_email:
            raise email_taken_exception()

        hashed_password = self.get_password_hash(user_request.password)

        user_id = await self.user_repository.create_user(user_request, hashed_password)
        return user_id

    async def get_users(self) -> list[dict]:
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> dict:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise user_not_found_exception()
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise user_not_found_exception()

        await delete_user_data_in_store_service(user_id)
        await self.user_repository.delete_user(user_id)