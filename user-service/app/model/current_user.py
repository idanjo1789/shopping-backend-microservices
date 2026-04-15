from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    country: str
    city: str
    is_active: bool = True