"""
Health Check Endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run and monitoring."""
    return {
        "status": "ok",
        "service": "storybook-ai-backend",
        "version": "1.0.0"
    }
