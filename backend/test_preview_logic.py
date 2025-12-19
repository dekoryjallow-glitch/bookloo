
import asyncio
import os
import sys
from pathlib import Path
import base64

# Add backend directory to python path
sys.path.append(str(Path(__file__).parent))

from app.config import get_settings
from app.services.firebase import initialize_firebase, StorageService
from app.engines.asset_generator import AssetGenerator
from google import genai
from google.genai import types

async def test_preview_logic():
    print("🚀 Starting Preview Logic Test (Imagen 3 via generate_content)")
    
    # 1. Initialize
    settings = get_settings()
    
    prompt = "A cute 3D pixar character of a child"
    
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # models/imagen-3.0-generate-001 was listed.
        model_name = "models/gemini-3-pro-image-preview"
        print(f"   Using model: {model_name}")
        
        try:
            print("   Attempting generate_content (Multimodal)...")
            from PIL import Image
            from io import BytesIO
            
            # 1x1 pixel red dot PNG
            minimal_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
            image_bytes = base64.b64decode(minimal_png_b64)
            input_image = Image.open(BytesIO(image_bytes))

            response = client.models.generate_content(
                model=model_name,
                contents=[input_image, prompt]
            )
            print("   Response received!")
            if response.candidates:
                for cand in response.candidates:
                    for part in cand.content.parts:
                        if part.inline_data:
                            print(f"   ✅ Got Image Data (inline)!")
                        else:
                            print(f"   Text/Other: {part.text}")
        except Exception as e:
            print(f"   generate_content failed: {e}")
            
    except Exception as e:
        print(f"❌ Test setup failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_preview_logic())
