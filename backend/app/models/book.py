"""
Storybook.ai - Book Models
Pydantic models for book data structures
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field


class BookStatus(str, Enum):
    """Book generation status."""
    CREATING_CHARACTER = "creating_character"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    GENERATING_PREVIEW = "generating_preview"
    READY_FOR_PURCHASE = "ready_for_purchase"
    PAID_PROCESSING_FULL = "paid_processing_full"
    COMPLETED = "completed"
    FAILED = "failed"


class BookTheme(str, Enum):
    """Available book themes."""
    ADVENTURE = "adventure"
    FRIENDSHIP = "friendship"
    MAGIC = "magic"
    NATURE = "nature"
    SPACE = "space"
    UNDERWATER = "underwater"
    CUSTOM = "custom"


class BookPage(BaseModel):
    """Single page in the book."""
    page_number: int
    text: str
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None


class BookCreateRequest(BaseModel):
    """Request to create a new book."""
    child_name: str = Field(..., min_length=1, max_length=50)
    theme: str = "space"  # Changed from BookTheme enum to string
    child_photo_url: str # Raw uploaded photo URL
    approved_character_url: Optional[str] = None # Pre-generated/Approved via Wizard
    user_id: str # Session ID or Auth ID
    
    additional_details: Optional[str] = Field(None, max_length=500)
    custom_theme: Optional[str] = None 
    style: Optional[str] = "pixar_3d"


class PreviewScene(BaseModel):
    """A single preview scene (mockup or locked)."""
    scene_id: int
    status: Literal["locked", "unlocked", "generating"]
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class BookResponse(BaseModel):
    """Book response model."""
    id: str
    user_id: str # NEW
    child_name: str
    theme: str
    style: str
    status: BookStatus
    progress: int = Field(default=0, ge=0, le=100)
    pages: list[BookPage] = []
    pdf_url: Optional[str] = None
    
    # Child photo (original upload) for regeneration
    child_photo_url: Optional[str] = None
    
    # Check these field names against the new flow
    character_image_url: Optional[str] = None # The generated character sheet/portrait
    master_character_url: Optional[str] = None # Same as character_image_url (legacy)
    
    cover_image_url: Optional[str] = None
    preview_images: list[str] = [] # Array of URLs (Cover + 3 Mockups)
    preview_scenes: list[PreviewScene] = [] 
    
    consistency_string: Optional[str] = None
    created_at: datetime
    updated_at: datetime



class BookStatusResponse(BaseModel):
    """Minimal status response for polling."""
    id: str
    status: BookStatus
    progress: int
    message: str
    character_image_url: Optional[str] = None # NEW: To show during approval
    pdf_url: Optional[str] = None
    preview_images: Optional[list[str]] = None
    preview_scenes: Optional[list[PreviewScene]] = None

