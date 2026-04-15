from app.model.user_request import UserRequest
from app.repository.database import database


class UserRepository:
    async def get_users(self) -> list[dict]:
        query = """
        SELECT id, username, email, first_name, last_name, phone, country, city, is_active
        FROM users
        ORDER BY id
        """
        return await database.fetch_all(query)

    async def get_user_by_id(self, user_id: int) -> dict | None:
        query = """
        SELECT id, username, email, first_name, last_name, phone, country, city, hashed_password, is_active
        FROM users
        WHERE id = :user_id
        """
        return await database.fetch_one(query, {"user_id": user_id})

    async def get_user_by_username(self, username: str) -> dict | None:
        query = """
        SELECT id, username, email, first_name, last_name, phone, country, city, hashed_password, is_active
        FROM users
        WHERE username = :username
        """
        return await database.fetch_one(query, {"username": username})

    async def get_user_by_email(self, email: str) -> dict | None:
        query = """
        SELECT id, username, email, first_name, last_name, phone, country, city, hashed_password, is_active
        FROM users
        WHERE email = :email
        """
        return await database.fetch_one(query, {"email": email})

    async def create_user(self, user_req: UserRequest, hashed_password: str) -> int:
        query = """
        INSERT INTO users (
            username,
            email,
            first_name,
            last_name,
            phone,
            country,
            city,
            hashed_password,
            is_active
        )
        VALUES (
            :username,
            :email,
            :first_name,
            :last_name,
            :phone,
            :country,
            :city,
            :hashed_password,
            :is_active
        )
        """
        values = {
            "username": user_req.username,
            "email": user_req.email,
            "first_name": user_req.first_name,
            "last_name": user_req.last_name,
            "phone": user_req.phone,
            "country": user_req.country,
            "city": user_req.city,
            "hashed_password": hashed_password,
            "is_active": True,
        }
        return await database.execute(query, values)

    async def delete_user(self, user_id: int) -> None:
        query = "DELETE FROM users WHERE id = :user_id"
        await database.execute(query, {"user_id": user_id})