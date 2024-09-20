from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.chat import ChatMessage, ChatResponse
from app.services import ai_service

router = APIRouter()


@router.post('/', response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    if current_user.id != message.user_id:
        raise HTTPException(
            status_code=403, detail='Not authorized to access this chat'
        )
    ai_response = await ai_service.process_chat_message(
        message.user_id, message.bot_id, message.message
    )
    return ChatResponse(response=ai_response)
