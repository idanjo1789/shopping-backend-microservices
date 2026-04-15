from typing import Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Order(BaseModel):
    id: Optional[int] = None
    user_id: int

    status: str = "TEMP"  # "TEMP" | "CLOSE"
    total_price: Decimal = Decimal("0.00")

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None