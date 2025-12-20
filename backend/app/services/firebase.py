"""
Storybook.ai - Firebase Service
Handles Firestore database and Cloud Storage operations.
"""

import json
from datetime import datetime
from typing import Optional
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore, storage

from app.config import Settings
from app.models.book import BookResponse, BookStatus, BookPage


# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None
_db: Optional[firestore.Client] = None
_bucket = None


def initialize_firebase(settings: Settings) -> None:
    """Initialize Firebase Admin SDK."""
    global _firebase_app, _db, _bucket
    
    if _firebase_app is not None:
        return
    
    # Load credentials
    cred_path = Path(settings.firebase_credentials_path)
    if cred_path.exists():
        cred = credentials.Certificate(str(cred_path))
    else:
        # Try to parse as JSON string (for Cloud Run secrets)
        try:
            cred_data = json.loads(settings.firebase_credentials_path)
            cred = credentials.Certificate(cred_data)
        except json.JSONDecodeError:
            print("Warning: Firebase credentials not found. Using mock mode.")
            return
    
    _firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': settings.firebase_storage_bucket
    })
    
    _db = firestore.client()
    _bucket = storage.bucket()
    
    print("Firebase initialized successfully")


def get_db() -> firestore.Client:
    """Get Firestore client. Auto-initializes Firebase if needed."""
    global _db
    if _db is None:
        # Try to auto-initialize
        from app.config import get_settings
        initialize_firebase(get_settings())
        if _db is None:
            raise RuntimeError("Firebase not initialized and auto-init failed.")
    return _db


def get_bucket():
    """Get Cloud Storage bucket. Auto-initializes Firebase if needed."""
    global _bucket
    if _bucket is None:
        # Try to auto-initialize
        from app.config import get_settings
        initialize_firebase(get_settings())
        if _bucket is None:
            raise RuntimeError("Firebase not initialized and auto-init failed.")
    return _bucket


class BookRepository:
    """Repository for book CRUD operations in Firestore."""
    
    COLLECTION = "books"
    
    def __init__(self):
        self.db = get_db()
        self.collection = self.db.collection(self.COLLECTION)
    
    async def create_book(
        self,
        child_name: str,
        theme: str,
        style: str,
        user_id: str,
        child_photo_url: str,
    ) -> str:
        """
        Create a new book document.
        
        Returns:
            The new book ID
        """
        now = datetime.utcnow()
        
        doc_ref = self.collection.document()
        doc_ref.set({
            "child_name": child_name,
            "theme": theme,
            "style": style,
            "user_id": user_id,
            "child_photo_url": child_photo_url,
            "status": BookStatus.CREATING_CHARACTER.value,
            "progress": 0,
            "pages": [],
            "pdf_url": None,
            "cover_image_url": None,
            "character_image_url": None, # Will be set by init task
            "preview_images": [], 
            "created_at": now,
            "updated_at": now,
        })
        
        return doc_ref.id
    
    async def get_book(self, book_id: str) -> Optional[BookResponse]:
        """Get a book by ID."""
        doc = self.collection.document(book_id).get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        
        return BookResponse(
            id=doc.id,
            user_id=data.get("user_id", "unknown"),
            child_name=data["child_name"],
            theme=data["theme"],
            style=data.get("style", "pixar_3d"),
            status=BookStatus(data["status"]),
            progress=data.get("progress", 0),
            pages=[BookPage(**p) for p in data.get("pages", [])],
            pdf_url=data.get("pdf_url"),
            cover_image_url=data.get("cover_image_url"),
            child_photo_url=data.get("child_photo_url"),
            character_image_url=data.get("character_image_url"),
            preview_images=data.get("preview_images", []),
            preview_scenes=data.get("preview_scenes", []),
            master_character_url=data.get("master_character_url"),
            consistency_string=data.get("consistency_string"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    async def get_user_books(self, user_id: str) -> list[BookResponse]:
        """Get all books for a specific user."""
        # Query by user_id and sort by created_at desc
        query = (
            self.collection
            .where("user_id", "==", user_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
        )
        docs = query.stream()
        
        books = []
        for doc in docs:
            data = doc.to_dict()
            # Safely create BookResponse (handling potential schema evolution issues if needed)
            try:
                books.append(BookResponse(
                    id=doc.id,
                    user_id=data.get("user_id", user_id),
                    child_name=data["child_name"],
                    theme=data["theme"],
                    style=data.get("style", "pixar_3d"),
                    status=BookStatus(data["status"]),
                    progress=data.get("progress", 0),
                    pages=[BookPage(**p) for p in data.get("pages", [])],
                    pdf_url=data.get("pdf_url"),
                    cover_image_url=data.get("cover_image_url"),
                    child_photo_url=data.get("child_photo_url"),
                    character_image_url=data.get("character_image_url"),
                    preview_images=data.get("preview_images", []),
                    preview_scenes=data.get("preview_scenes", []),
                    master_character_url=data.get("master_character_url"),
                    consistency_string=data.get("consistency_string"),
                    created_at=data["created_at"],
                    updated_at=data["updated_at"],
                ))
            except Exception as e:
                print(f"Skipping malformed book {doc.id}: {e}")
                continue
                
        return books
    
    async def update_character_data(
        self,
        book_id: str,
        master_url: str,
        consistency_str: str,
    ) -> None:
        """Update character reference data."""
        self.collection.document(book_id).update({
            "master_character_url": master_url,
            "consistency_string": consistency_str,
            "updated_at": datetime.utcnow(),
        })
    
    async def update_status(
        self,
        book_id: str,
        status: BookStatus,
        progress: int = 0,
        message: Optional[str] = None,
    ) -> None:
        """Update book generation status."""
        update_data = {
            "status": status.value,
            "progress": progress,
            "updated_at": datetime.utcnow(),
        }
        if message:
            update_data["status_message"] = message
        self.collection.document(book_id).update(update_data)
    
    async def update_pages(
        self,
        book_id: str,
        pages: list[BookPage],
    ) -> None:
        """Update book pages."""
        self.collection.document(book_id).update({
            "pages": [p.model_dump() for p in pages],
            "updated_at": datetime.utcnow(),
        })
    
    async def update_preview_images(
        self,
        book_id: str,
        preview_images: list[str],
    ) -> None:
        """Update preview image URLs."""
        self.collection.document(book_id).update({
            "preview_images": preview_images,
            "updated_at": datetime.utcnow(),
        })

    async def update_preview_scenes(
        self,
        book_id: str,
        preview_scenes: list,
        preview_images: list[str],
    ) -> None:
        """Update preview scenes structure and images list."""
        self.collection.document(book_id).update({
            "preview_scenes": preview_scenes,
            "preview_images": preview_images,
            "updated_at": datetime.utcnow(),
        })
    
    async def set_pdf_url(self, book_id: str, pdf_url: str) -> None:
        """Set the completed PDF URL."""
        self.collection.document(book_id).update({
            "pdf_url": pdf_url,
            "status": BookStatus.COMPLETED.value,
            "progress": 100,
            "updated_at": datetime.utcnow(),
        })


class StorageService:
    """Service for Firebase Cloud Storage operations."""
    
    def __init__(self):
        self.bucket = get_bucket()
    
    async def upload_child_photo(
        self,
        book_id: str,
        file_content: bytes,
        filename: str,
    ) -> str:
        """
        Upload a child's photo.
        
        Returns:
            Public URL of the uploaded image
        """
        blob_path = f"books/{book_id}/child_photo/{filename}"
        blob = self.bucket.blob(blob_path)
        
        # Determine content type
        content_type = "image/jpeg"
        if filename.lower().endswith(".png"):
            content_type = "image/png"
        elif filename.lower().endswith(".webp"):
            content_type = "image/webp"
        
        blob.upload_from_string(file_content, content_type=content_type)
        blob.make_public()
        
        return blob.public_url

    async def upload_image(
        self,
        book_id: str,
        file_content: bytes,
        filename: str,
        content_type: str = "image/jpeg",
    ) -> str:
        """
        Generic image upload for generated content/mockups.
        """
        blob_path = f"books/{book_id}/images/{filename}"
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(file_content, content_type=content_type)
        blob.make_public()
        return blob.public_url
    
    async def upload_pdf(
        self,
        book_id: str,
        pdf_content: bytes,
    ) -> str:
        """
        Upload the generated PDF.
        
        Returns:
            Public URL of the PDF
        """
        blob_path = f"books/{book_id}/book.pdf"
        blob = self.bucket.blob(blob_path)
        
        blob.upload_from_string(pdf_content, content_type="application/pdf")
        blob.make_public()
        
        return blob.public_url
