# Placeholder: FastAPI application entry point.


# Import order matters: config first, so a bad .env crashes here —
# at import time, before uvicorn even finishes booting the app.
from app.core.config import settings
from app.core.logging import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat_routes

app = FastAPI(title="Offline AI-Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Register the chat API routes (POST "/" -> chat_endpoints) .

app.include_router(chat_routes.router)

logger.info(
    "app_startup",
    environment=settings.environment,
    model=settings.llm_model_name,
    chunk_size=settings.chunk_size,
    top_k=settings.top_k,
)


@app.get("/")
def root():
    return {"status": "ok", "environment": settings.environment}