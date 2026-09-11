# Placeholder: health check endpoints for the backend service.
# Health check endpoints for the backend service.

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    """Return the health status of the backend."""

    return {
        "status": "ok"
    }