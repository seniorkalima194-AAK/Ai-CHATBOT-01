"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat_routes, document_routes, health_routes
from app.core.config import settings
from app.core.logging import logger
from app.documents.watcher import start_document_watcher, stop_document_watcher


@asynccontextmanager
async def lifespan(_app: FastAPI):
    start_document_watcher()
    yield
    stop_document_watcher()


app = FastAPI(title="Offline AI-Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(
    document_routes.router, prefix="/api/v1/documents", tags=["documents"]
)

logger.info(
    "app_startup",
    environment=settings.environment,
    model=settings.ollama_model,
    chunk_size=settings.chunk_size,
    top_k=settings.top_k,
)


@app.get("/")
def root():
    return {"status": "ok", "environment": settings.environment}
