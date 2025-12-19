"""
Storybook.ai - Asset Generation Routes
Endpoints for generating individual assets (character portraits) on demand.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Literal

from app.config import get_settings
from app.engines.asset_generator import AssetGenerator

router = APIRouter()

@router.post("/generate-character-preview")
async def generate_character_preview(
    file: UploadFile = File(...),
    gender: str = Form(...),
    name: str = Form(...),
):
    """
    Generate a single character portrait preview from an uploaded photo.
    This uses nano-banana-pro (Gemini) for fast, high-quality generation.
    Returns public URLs for both the original upload and the generated result.
    """
    import uuid
    from app.services.firebase import StorageService
    
    settings = get_settings()
    generator = AssetGenerator(settings)
    storage = StorageService()
    
    # Generate a temporary ID for this preview session
    preview_id = str(uuid.uuid4())
    
    # 1. Read and Upload Original File
    try:
        image_bytes = await file.read()
        original_filename = f"original_{file.filename}"
        
        # Use a 'previews' folder in storage
        # We need to manually construct the blob path or add a method to StorageService
        # For quickness, we access bucket directly or mock book_id structure
        # Let's use "previews" as a pseudo book_id for organization, or just use the preview_id
        
        # Using the existing upload_child_photo strictly requires a book_id path structure? 
        # Checking code: blob_path = f"books/{book_id}/child_photo/{filename}"
        # We can pass "previews/{preview_id}" as book_id to hack it, or just use the bucket directly here.
        
        # Be clean: Access bucket directly here since StorageService is tied to books structure
        bucket = storage.bucket
        blob_path = f"previews/{preview_id}/original.jpg"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(image_bytes, content_type=file.content_type or "image/jpeg")
        blob.make_public()
        original_url = blob.public_url
        
        print(f"   ✅ Original uploaded: {original_url}")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process original image: {e}")
    
    # 2. Generate Character
    # "Junge" / "Mädchen" -> "boy" / "girl" for the prompt
    gender_en = "boy" if gender.lower() in ["junge", "boy"] else "girl"
    if gender.lower() in ["neutral", "other"]:
        gender_en = "child"
        
    print(f"🎨 Generating Preview for {name} ({gender_en})...")
    
    prompt = (
        f"Transform this {gender_en} into a 3D Pixar animated character. "
        f"Disney concept art style, cute portrait, vibrant colors, smooth 3D render, "
        "subsurface scattering, big expressive eyes, cinematic lighting, 8k resolution. "
        "Keep the exact same facial features, skin tone, and ethnicity. "
        "Full body front view, clean white background, professional character concept art."
    )
    
    try:
        # Call generator -> returns local file path "file://..."
        local_url = await generator._run_nano_banana(image_bytes, prompt)
        
        if not local_url or not local_url.startswith("file://"):
            # Fallback check if it returned a regular URL or failed
            if not local_url:
                raise HTTPException(status_code=500, detail="Failed to generate image (invalid result)")
            
        local_path = local_url.replace("file://", "")
        
        # 3. Upload Generated File
        with open(local_path, "rb") as f:
            gen_bytes = f.read()
            
        gen_blob_path = f"previews/{preview_id}/generated.png"
        gen_blob = bucket.blob(gen_blob_path)
        gen_blob.upload_from_string(gen_bytes, content_type="image/png")
        gen_blob.make_public()
        generated_url = gen_blob.public_url
        
        print(f"   ✅ Generated uploaded: {generated_url}")
        
        return {
            "original_url": original_url,
            "generated_url": generated_url
        }
        
    except Exception as e:
        print(f"❌ Preview Generation Failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...)
):
    """
    Generic image upload endpoint.
    Returns: {"url": "..."}
    """
    import uuid
    from app.services.firebase import StorageService
    
    storage = StorageService()
    
    try:
        content = await file.read()
        filename = f"upload_{uuid.uuid4()}_{file.filename}"
        
        # Use a 'uploads' folder
        bucket = storage.bucket
        blob_path = f"uploads/{filename}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(content, content_type=file.content_type or "image/jpeg")
        blob.make_public()
        
        return {"url": blob.public_url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
