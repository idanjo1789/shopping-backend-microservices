from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.service.auth_service import auth_service
from app.service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatAskRequest(BaseModel):
    message: str


@router.post("/ask", status_code=status.HTTP_200_OK)
async def ask_chat(
    request: ChatAskRequest,
    user_id: int = Depends(auth_service.get_current_user_id),
):
    return await chat_service.ask_store_question(
        user_id=user_id,
        message=request.message,
    )