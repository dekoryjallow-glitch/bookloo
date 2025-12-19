"""
bookloo - Books API Routes
Endpoints for creating and managing personalized children's books.
Async Polling Architecture Refactor.
"""

import asyncio
import os
from typing import Optional, Literal
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.models.book import (
    BookCreateRequest,
    BookResponse,
    BookStatusResponse,
    BookStatus,
    BookTheme,
    BookPage,
    PreviewScene
)
from app.engines.story_engine import StoryEngine
from app.engines.image_engine import ImageEngineWithRetry
from app.engines.asset_generator import AssetGenerator
from app.engines.pdf_engine import PDFEngine
from app.services.firebase import BookRepository, StorageService


router = APIRouter()

# Number of preview images to generate
PREVIEW_IMAGE_COUNT = 4


# Use AssetGenerator directly since WithRetry might be legacy/broken for NanoBanana
# Use AssetGenerator directly since WithRetry might be legacy/broken for NanoBanana
async def generate_character_task(
    book_id: str,
    child_name: str,
    theme: str,
    style: str,
    child_photo_url: str,
    approved_character_url: Optional[str] = None, # NEW
):
    """
    Background Task 1: Generate Character Portrait from Photo.
    """
    settings = get_settings()
    repo = BookRepository()
    storage = StorageService()
    
    try:
        await repo.update_status(book_id, BookStatus.CREATING_CHARACTER, 10)
        print(f"🚀 [Book {book_id}] Starting Character Generation...")
        print(f"   📝 child_name: {child_name}")
        print(f"   📝 theme: {theme}")
        print(f"   📝 style: {style}")
        print(f"   📝 child_photo_url: {child_photo_url[:50] if child_photo_url else 'None'}...")
        print(f"   📝 approved_character_url: {approved_character_url[:50] if approved_character_url else 'None'}...")
        
        final_char_url = None

        # OPTIMIZED FLOW: Use pre-generated character if available
        if approved_character_url:
             print(f"   ⏩ Using pre-approved character: {approved_character_url[:50]}...")
             
             # Re-upload to books/ folder to ensure consistent public access
             # The previews/ URL might have caching or ACL issues with Replicate
             import httpx
             try:
                 async with httpx.AsyncClient(timeout=30.0) as client:
                     resp = await client.get(approved_character_url)
                     if resp.status_code == 200:
                         file_content = resp.content
                         filename = f"character_portrait_{book_id}.png"
                         final_char_url = await storage.upload_image(book_id, file_content, filename, content_type="image/png")
                         print(f"   📤 Re-uploaded to books/ folder: {final_char_url}")
                     else:
                         print(f"   ⚠️ Failed to download approved char ({resp.status_code}), using original URL")
                         final_char_url = approved_character_url
             except Exception as e:
                 print(f"   ⚠️ Re-upload failed: {e}, using original URL")
                 final_char_url = approved_character_url
             
        else:
            # STANDARD FLOW: Generate now
            asset_gen = AssetGenerator(settings)
            
            # Generate Character Asset (Step 1)
            asset = await asset_gen.generate_character_asset(
                photo_url=child_photo_url,
                child_name=child_name,
                style=style
            )
            
            if not asset or not asset.image_urls:
                raise Exception("Failed to generate character asset")

            # The generator returns a local file path (file://...) for NanoBanana
            local_url = asset.image_urls[0]
            final_char_url = local_url
            
            # If it's a local file, we MUST upload it to Storage to make it accessible to Frontend
            if local_url.startswith("file://"):
                local_path = local_url.replace("file://", "")
                print(f"   📤 Uploading character to Storage: {local_path}")
                
                with open(local_path, "rb") as f:
                    file_content = f.read()
                    
                filename = f"character_portrait_{book_id}.jpg"
                final_char_url = await storage.upload_image(book_id, file_content, filename)
                
                # Clean up temp file
                try:
                    os.remove(local_path)
                except:
                    pass

        # NEW: Character Analysis for consistency string
        consistency_str = f"child named {child_name}"
        try:
             from app.engines.character_analyzer import CharacterAnalyzer
             analyzer = CharacterAnalyzer(settings)
             # Use the final public URL for analysis
             traits = await analyzer.analyze_photo(final_char_url)
             consistency_str = traits.consistency_string
             print(f"   🧬 Consistency String extracted: {consistency_str}")
        except Exception as e:
             print(f"   ⚠️ Analysis failed, using fallback: {e}")

        # Update DB with the public URL and the REAL consistency string
        await repo.update_character_data(book_id, master_url=final_char_url, consistency_str=consistency_str)
        
        # Explicitly update character_image_url field for the frontend
        repo.db.collection("books").document(book_id).update({
            "character_image_url": final_char_url,
            "master_character_url": final_char_url
        })

        if approved_character_url:
            # AUTO-APPROVE if we already had a preview the user liked in the wizard
            print(f"✅ Auto-approving character and starting preview... {final_char_url}")
            await generate_preview_task(
                book_id=book_id,
                child_name=child_name,
                theme=theme,
                style=style,
                approved_portrait_url=final_char_url
            )
        else:
            await repo.update_status(book_id, BookStatus.WAITING_FOR_APPROVAL, 50)
            print(f"✅ Character Ready for Approval (Manual): {final_char_url}")

    except Exception as e:
        print(f"❌ Error generating character {book_id}: {e}")
        import traceback
        traceback.print_exc()
        await repo.update_status(book_id, BookStatus.FAILED, 0)


async def generate_preview_task(
    book_id: str,
    child_name: str,
    theme: str,
    style: str,
    approved_portrait_url: str,
):
    """
    Background Task 2: Generate Optimized Story Preview (4 Scenes + Mockups).
    """
    settings = get_settings()
    repo = BookRepository()
    storage = StorageService()
    
    try:
        await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, 60)
        print(f"🚀 [Book {book_id}] Starting Preview Generation (Phase 2)...")
        print(f"   📝 Child: {child_name}, Theme: {theme}, Style: {style}")
        print(f"   📷 Character URL: {approved_portrait_url[:50]}...")
        
        # 1. Generate Story
        print(f"   [Step 1/4] Generating Story...")
        await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, 15, message="Erdenke Abenteuer... ✍️")
        story_engine = StoryEngine(settings)
        
        # Fetch book to get consistency string
        book = await repo.get_book(book_id)
        character_desc_simple = book.consistency_string or f"cute 6 year old child named {child_name}"
        
        # Assuming minimal implementation of story generation
        story = await story_engine.generate_story(
            name=child_name,
            theme=theme,
            age=6, # Default
            style=style,
            character_description=character_desc_simple
        )
        print(f"   [Step 1/4] ✅ Story generated: {story.title} ({len(story.scenes)} scenes)")
        await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, 30, message="Schreibe die Geschichte... 📖")
        
        # Save pages
        print(f"   [Step 2/4] Saving pages...")
        pages = story_engine.story_to_compact_pages(story)
        await repo.update_pages(book_id, pages)
        print(f"   [Step 2/4] ✅ {len(pages)} pages saved")
        
        # 2. Generate Key Scenes
        KEY_SCENES = [0, 1, 7, 13]
        print(f"   [Step 3/4] Initializing Image Engine...")
        image_engine = ImageEngineWithRetry(settings)
        
        # Use AI-powered mockup engine with detailed prompts
        from app.engines.ai_mockup_engine_v3 import AIMockupEngineV3
        mockup_engine = AIMockupEngineV3(settings)
        
        print(f"   [Step 3/4] 🎨 Generating {len(KEY_SCENES)} KEY scenes with FLUX...")
        await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, 35, message="Skizziere Szenen... 🎨")
        
        generated_images = await image_engine.generate_scenes_with_character_asset(
            story=story,
            character_asset_url=approved_portrait_url,
            child_name=child_name,
            theme=theme,
            scene_numbers=KEY_SCENES,
            features_description=character_desc_simple,
        )
        print(f"   [Step 3/4] ✅ Generated {len(generated_images)} images")
        await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, 45, message="Male Illustrationen... 🖌️")
        
        # 3. Create AI-Powered Mockups
        print(f"   [Step 4/4] 📖 Creating AI-powered mockups...")
        preview_scenes = []
        preview_image_urls = []
        
        raw_image_map = {img.scene_number: img.image_url for img in generated_images}
        
        for i in range(14): # 0 (Cover) + 13 Story Scenes
            is_key = i in KEY_SCENES
            status = "unlocked" if is_key else "locked"
            mockup_url = None
            
            if is_key and i in raw_image_map and raw_image_map[i]:
                raw_url = raw_image_map[i]
                print(f"   🖼️ Creating AI Mockup for Scene {i}...")
                if i == 0:
                    print(f"   📚 COVER: theme={theme}, child_name={child_name}, title={story.title}")
                
                # Get story text for this scene (for left page)
                scene_text = ""
                if i > 0:  # Not cover
                    scene_data = next((s for s in story.scenes if s.scene_number == i), None)
                    if scene_data:
                        scene_text = scene_data.narration_text or ""
                
                try:
                    # Use AI mockup engine with story text and style reference
                    mockup_bytes = await mockup_engine.create_mockup(
                        scene_image_url=raw_url,
                        scene_number=i,
                        book_title=story.title if i == 0 else None,
                        story_text=scene_text if i > 0 else None,
                        theme=theme if i == 0 else None,
                        child_name=child_name if i == 0 else None,
                        character_reference_url=approved_portrait_url if i == 0 else None,
                    )
                    
                    if mockup_bytes:
                        filename = f"mockup_scene_{i}.jpg"
                        mockup_url = await storage.upload_image(book_id, mockup_bytes, filename, content_type="image/jpeg")
                        preview_image_urls.append(mockup_url)
                        print(f"   ✅ Mockup {i} uploaded")
                    else:
                        # Fallback to raw image if mockup fails
                        mockup_url = raw_url
                        preview_image_urls.append(raw_url)
                        print(f"   ⚠️ Using raw image as fallback for scene {i}")
                    
                except Exception as e:
                    print(f"   ⚠️ Mockup failed for scene {i}: {e}")
                    mockup_url = raw_url
                    preview_image_urls.append(raw_url)

                # Increment progress per finished preview image (4 key scenes)
                current_progress = 45 + (len(preview_image_urls) * 12) # ~45 + 48 = 93%
                await repo.update_status(book_id, BookStatus.GENERATING_PREVIEW, min(current_progress, 95), message=f"Vorschau {len(preview_image_urls)}/4 bereit... ✨")
            
            preview_scenes.append(PreviewScene(
                scene_id=i,
                status=status,
                image_url=mockup_url,
                thumbnail_url=mockup_url 
            ))

        await repo.update_preview_scenes(
            book_id=book_id,
            preview_scenes=[s.dict() for s in preview_scenes],
            preview_images=preview_image_urls
        )
        
        await repo.update_status(book_id, BookStatus.READY_FOR_PURCHASE, 100)
        print(f"🎉 Preview Ready for Purchase!")
        
    except Exception as e:
        print(f"❌ Error generating preview {book_id}: {e}")
        import traceback
        traceback.print_exc()
        await repo.update_status(book_id, BookStatus.FAILED, 0)


async def complete_book_task(book_id: str):
    """
    Background Task 3: Complete Book (Remaining Scenes + PDF).
    """
    settings = get_settings()
    repo = BookRepository()
    storage = StorageService()
    
    try:
        book = await repo.get_book(book_id)
        if not book: return
        
        await repo.update_status(book_id, BookStatus.PAID_PROCESSING_FULL, 10)
        
        story_engine = StoryEngine(settings)
        image_engine = ImageEngineWithRetry(settings)
        
        # Re-generate story object from engine (or we could store it in DB as JSON)
        story = await story_engine.generate_story(
            name=book.child_name, 
            theme=book.theme, 
            age=6, 
            style=book.style,
            character_description=book.consistency_string or f"child named {book.child_name}"
        )
        
        # Original logic: Sc 0, 1, 7, 13 done.
        remaining_scenes = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        
        generated_images = await image_engine.generate_scenes_with_character_asset(
            story=story,
            character_asset_url=book.character_image_url or book.master_character_url,
            child_name=book.child_name,
            theme=book.theme,
            scene_numbers=remaining_scenes,
            features_description=book.consistency_string or f"child named {book.child_name}",
        )
        
        image_map = {img.scene_number: img.image_url for img in generated_images}
        pages = book.pages
        
        for page in pages:
            # Simple mapping: Page 1,2 -> Scene 1. Page 3,4 -> Scene 2.
            scene_num = (page.page_number + 1) // 2
            if scene_num in image_map and image_map[scene_num]:
                page.image_url = image_map[scene_num]
        
        await repo.update_pages(book_id, pages)
        
        # Create PDF
        pdf_engine = PDFEngine()
        pdf_content = await pdf_engine.generate_inner_pdf(
            story.scenes, 
            book.child_name, 
            story.title
        )
        pdf_url = await storage.upload_pdf(book_id, pdf_content)
        await repo.set_pdf_url(book_id, pdf_url)
        
        await repo.update_status(book_id, BookStatus.COMPLETED, 100)
        print(f"✅ Book {book_id} Completed!")

    except Exception as e:
        print(f"❌ Error completing book {book_id}: {e}")
        await repo.update_status(book_id, BookStatus.FAILED, 0)


# ================= API ENDPOINTS =================

@router.post("/init", response_model=BookStatusResponse)
async def init_book(
    request: BookCreateRequest,
    background_tasks: BackgroundTasks,
):
    """
    Step 1: Initialize Book & Start Character Generation.
    Takes Photo + Name + Theme.
    Returns Queryable Book ID.
    """
    repo = BookRepository()
    
    # Create DB Entry
    book_id = await repo.create_book(
        child_name=request.child_name,
        theme=request.theme,
        style=request.style or "pixar_3d",
        user_id=request.user_id,
        child_photo_url=request.child_photo_url,
    )
    
    # Start Background Task 1: Generate Character
    background_tasks.add_task(
        generate_character_task,
        book_id=book_id,
        child_name=request.child_name,
        theme=request.theme,
        style=request.style or "pixar_3d",
        child_photo_url=request.child_photo_url,
        approved_character_url=request.approved_character_url, # Pass pre-approved URL
    )
    
    return BookStatusResponse(
        id=book_id,
        status=BookStatus.CREATING_CHARACTER,
        progress=0,
        message="Zaubere Charakter... ✨"
    )

@router.post("/{book_id}/approve", response_model=BookStatusResponse)
async def approve_book(book_id: str, background_tasks: BackgroundTasks):
    """
    Step 2: Approve Character & Start Preview Generation.
    """
    repo = BookRepository()
    book = await repo.get_book(book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    if book.status != BookStatus.WAITING_FOR_APPROVAL:
         # Tolerance for re-clicks
         if book.status in [BookStatus.GENERATING_PREVIEW, BookStatus.READY_FOR_PURCHASE]:
             return BookStatusResponse(id=book_id, status=book.status, progress=book.progress, message="Bereits genehmigt.")
         # If simpler status mismatch
         if book.status == BookStatus.CREATING_CHARACTER:
              raise HTTPException(status_code=400, detail="Character still generating")
         # If already failed
         if book.status == BookStatus.FAILED:
              raise HTTPException(status_code=400, detail="Book creation failed. Please start over.")
         # Unknown or unexpected status - reject approval
         raise HTTPException(status_code=400, detail=f"Cannot approve book with status: {book.status}")
         
    # Start Task 2: Preview
    char_url = book.character_image_url or book.master_character_url
    if not char_url:
        raise HTTPException(status_code=500, detail="Character URL missing")
        
    background_tasks.add_task(
        generate_preview_task,
        book_id=book_id,
        child_name=book.child_name,
        theme=book.theme,
        style=book.style,
        approved_portrait_url=char_url
    )
    
    return BookStatusResponse(
        id=book_id,
        status=BookStatus.GENERATING_PREVIEW,
        progress=0,
        message="Erstelle Vorschau-Szenen... 📚"
    )

@router.post("/{book_id}/regenerate", response_model=BookStatusResponse)
async def regenerate_character(book_id: str, background_tasks: BackgroundTasks):
    """
    Step 2 (Alternative): Reject current character and regenerate a new one.
    Resets the book status and starts character generation again.
    """
    repo = BookRepository()
    book = await repo.get_book(book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Only allow regeneration if waiting for approval or failed
    if book.status not in [BookStatus.WAITING_FOR_APPROVAL, BookStatus.FAILED]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot regenerate character in status: {book.status}"
        )
    
    # Reset status to creating character
    await repo.update_status(book_id, BookStatus.CREATING_CHARACTER, 0)
    
    # Start character generation again
    background_tasks.add_task(
        generate_character_task,
        book_id=book_id,
        child_name=book.child_name,
        theme=book.theme,
        style=book.style,
        child_photo_url=book.child_photo_url if hasattr(book, 'child_photo_url') and book.child_photo_url else "",
        approved_character_url=None,  # Force regeneration
    )
    
    return BookStatusResponse(
        id=book_id,
        status=BookStatus.CREATING_CHARACTER,
        progress=0,
        message="Generiere neuen Charakter... ✨"
    )

@router.get("/my-books", response_model=list[BookResponse])
async def get_my_books(user_id: str):
    """List all books for a user."""
    repo = BookRepository()
    books = await repo.get_user_books(user_id)
    return books

@router.get("/{book_id}/status", response_model=BookStatusResponse)
async def get_book_status(book_id: str):
    """Get status."""
    repo = BookRepository()
    book = await repo.get_book(book_id)
    if not book: raise HTTPException(status_code=404)
    
    msg_map = {
        BookStatus.CREATING_CHARACTER: "Zaubere Charakter... ✨",
        BookStatus.WAITING_FOR_APPROVAL: "Bitte Charakter prüfen! 👀",
        BookStatus.GENERATING_PREVIEW: "Erstelle Vorschau... 🎨",
        BookStatus.READY_FOR_PURCHASE: "Vorschau bereit! 🔓",
        BookStatus.PAID_PROCESSING_FULL: "Erstelle ganzes Buch... 📖",
        BookStatus.COMPLETED: "Fertig! 🎉",
        BookStatus.FAILED: "Fehler aufgetreten."
    }
    
    return BookStatusResponse(
        id=book_id,
        status=book.status,
        progress=book.progress,
        message=msg_map.get(book.status, "Lade..."),
        character_image_url=book.character_image_url,
        preview_scenes=book.preview_scenes,
        preview_images=book.preview_images,
        pdf_url=book.pdf_url
    )

@router.post("/{book_id}/purchase")
async def purchase_book(book_id: str, background_tasks: BackgroundTasks):
    """Complete purchase."""
    repo = BookRepository()
    book = await repo.get_book(book_id)
    if not book: raise HTTPException(404)
    
    if book.status != BookStatus.READY_FOR_PURCHASE:
         if book.status == BookStatus.COMPLETED:
             return {"message": "Bereits fertig."}
         raise HTTPException(400, f"Not ready. Status: {book.status}")
    
    background_tasks.add_task(complete_book_task, book_id=book_id)
    return {"message": "Zahlung erfolgreich. Buch wird generiert."}
    
@router.get("/{book_id}", response_model=BookResponse)
async def get_book_details(book_id: str):
    repo = BookRepository()
    book = await repo.get_book(book_id)
    if not book: raise HTTPException(404)
    return book

@router.get("/user/{user_id}", response_model=list[BookResponse])
async def get_user_books(user_id: str):
    """
    Get all books for a specific user.
    """
    repo = BookRepository()
    books = await repo.get_user_books(user_id)
    return books

@router.get("/{book_id}/download")
async def download_book(book_id: str):
    repo = BookRepository()
    book = await repo.get_book(book_id)
    if not book or not book.pdf_url: raise HTTPException(404)
    return JSONResponse({"download_url": book.pdf_url, "filename": f"{book.child_name}.pdf"})
