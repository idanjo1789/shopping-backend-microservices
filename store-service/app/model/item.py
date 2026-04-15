from typing import Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: Optional[int] = None

    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None

    price: Decimal
    stock: int = Field(ge=0)

    is_active: bool = True

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None   