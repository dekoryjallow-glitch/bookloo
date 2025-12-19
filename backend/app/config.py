"""
bookloo - Application Configuration
Centralized settings management using Pydantic
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "bookloo"
    app_env: str = "development"
    app_debug: bool = True
    frontend_url: str = "http://localhost:3000"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Gemini (Google)
    gemini_api_key: str = ""
    
    # Replicate (Flux Model)
    replicate_api_token: str = ""
    
    # Firebase
    firebase_project_id: str = ""
    firebase_storage_bucket: str = ""
    firebase_credentials_path: str = "./firebase-service-account.json"
    
    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_price_id: str = ""
    stripe_webhook_secret: str = ""
    
    # Gelato (Print on Demand)
    gelato_api_key: str = ""
    
    # Book Generation Settings
    book_pages: int = 32
    image_style: str = "whimsical children's book illustration, watercolor style, warm colors, friendly characters"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
