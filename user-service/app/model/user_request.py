from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    country: str
    city: str
    password: str