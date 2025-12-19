"""
Test the approve flow - simulates what happens when user clicks "Buch erstellen"
"""
import asyncio
from app.config import get_settings
from app.models.book import BookStatus
from app.services.firebase import BookRepository
from app.api.routes.books import generate_preview_task

# Test with a real book ID - you need to replace this with an actual book_id from your test
TEST_BOOK_ID = None  # Will be created

async def create_test_book():
    """Create a test book entry to simulate the flow"""
    repo = BookRepository()
    
    # Create test book
    book_id = await repo.create_book(
        child_name="Max",
        theme="space",  # Using space theme
        style="pixar_3d",
        user_id="test-user-123",
        child_photo_url="https://example.com/test.jpg",
    )
    print(f"✅ Created test book: {book_id}")
    
    # Simulate character generation complete - set to WAITING_FOR_APPROVAL
    await repo.update_character_data(
        book_id, 
        master_url="https://firebasestorage.googleapis.com/test-character.jpg",
        consistency_str="cute child Max"
    )
    await repo.db.collection("books").document(book_id).update({
        "character_image_url": "https://firebasestorage.googleapis.com/test-character.jpg",
        "master_character_url": "https://firebasestorage.googleapis.com/test-character.jpg"
    })
    await repo.update_status(book_id, BookStatus.WAITING_FOR_APPROVAL, 50)
    print(f"✅ Set status to WAITING_FOR_APPROVAL")
    
    return book_id

async def test_approve_flow(book_id: str):
    """Test what happens when approve is called"""
    repo = BookRepository()
    
    # Get book
    book = await repo.get_book(book_id)
    print(f"\n📖 Book Details:")
    print(f"   ID: {book.id}")
    print(f"   Child: {book.child_name}")
    print(f"   Theme: {book.theme}")
    print(f"   Status: {book.status}")
    print(f"   Character URL: {book.character_image_url}")
    
    if book.status != BookStatus.WAITING_FOR_APPROVAL:
        print(f"⚠️ Status is not WAITING_FOR_APPROVAL, it's {book.status}")
        return
    
    # Try to run the preview task directly
    print(f"\n🚀 Running generate_preview_task...")
    try:
        await generate_preview_task(
            book_id=book_id,
            child_name=book.child_name,
            theme=book.theme,
            style=book.style,
            approved_portrait_url=book.character_image_url,
        )
        print(f"✅ Preview task completed!")
    except Exception as e:
        print(f"❌ Preview task FAILED: {e}")
        import traceback
        traceback.print_exc()

async def main():
    # Create a test book
    book_id = await create_test_book()
    
    # Test the approve flow
    await test_approve_flow(book_id)

if __name__ == "__main__":
    asyncio.run(main())
