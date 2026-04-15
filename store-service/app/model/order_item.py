from typing import Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    id: Optional[int] = None
    order_id: int
    item_id: int

    quantity: int = Field(ge=1)
    unit_price: Decimal

    created_at: Optional[datetime] = None