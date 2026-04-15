from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CustomerFavoriteItem(BaseModel):
    id: Optional[int] = None
    user_id: int = Field(gt=0)
    item_id: int = Field(gt=0)
    created_at: Optional[datetime] = None