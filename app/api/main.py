from fastapi import FastAPI
from app.api.routes_chat import router as chat_router


def create_app() -> FastAPI:
    """
    Initialize the FastAPI application.
    """
    app = FastAPI(
        title="HR Analytics Chatbot API",
        version="1.0.0"
    )
    app.include_router(chat_router)
    return app


app = create_app()