from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.core.auth import validate_user
from app.services.chat_service import process_query
from app.core.logging import get_logger

router = APIRouter(prefix="/chat", tags=["Chatbot"])
logger = get_logger("api.chat")


class ChatRequest(BaseModel):
    """
    Request model for chatbot queries.
    """
    user_id: str
    query: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        """
        Validate and normalize user_id input.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("user_id cannot be empty")
        if len(cleaned) > 100:
            raise ValueError("user_id is too long")
        return cleaned

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        """
        Validate and normalize query input.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("query cannot be empty")
        if len(cleaned) > 2000:
            raise ValueError("query is too long")
        return cleaned


class ChatResponse(BaseModel):
    """
    Response model returned by the chatbot API.
    """
    answer: str
    sql_used: str
    data: list


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that accepts natural language questions and user identity.
    """
    logger.info("Received chat request user_id=%s", request.user_id)

    user_division = validate_user(request.user_id)
    if not user_division:
        logger.warning("Authentication failed for user_id=%s", request.user_id)
        raise HTTPException(status_code=401, detail="Invalid user_id")

    try:
        answer, sql_used, data = process_query(
            user_id=request.user_id,
            user_division=user_division,
            question=request.query,
        )
    except Exception as exc:
        logger.exception("Error processing query for user_id=%s", request.user_id)
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    logger.info("Successfully processed chat for user_id=%s", request.user_id)

    return ChatResponse(
        answer=answer,
        sql_used=sql_used,
        data=data
    )