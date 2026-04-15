from pydantic import BaseModel


class ChatRequest(BaseModel):
    item_id: int
    message: str