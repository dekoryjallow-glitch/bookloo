"""
bookloo - FastAPI Application Entry Point
Personalized children's book generator
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import books, health, assets, payment, webhook
from app.services.firebase import initialize_firebase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    settings = get_settings()
    initialize_firebase(settings)
    print(f"🚀 {settings.app_name} starting up...")
    
    yield
    
    # Shutdown
    print(f"👋 {settings.app_name} shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="AI-powered personalized children's book generator",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # CORS Middleware - permissive for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
    app.include_router(books.router, prefix="/api/books", tags=["Books"])
    app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])
    app.include_router(webhook.router, prefix="/api/webhook", tags=["Webhook"])
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
