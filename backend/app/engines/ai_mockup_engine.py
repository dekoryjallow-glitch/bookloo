"""
Storybook.ai - AI-Powered Mockup Generator
Uses Gemini 2.5 Flash (Nano-Banana-Pro) to create photorealistic book mockups
by compositing generated illustrations onto mockup templates.
"""

import os
import base64
import tempfile
from pathlib import Path
from typing import Optional
from io import BytesIO

from PIL import Image
from google import genai
from google.genai import types

from app.config import Settings, get_settings


class AIMockupEngine:
    """
    Creates photorealistic book mockups using AI image editing.
    
    Templates:
    - cover_template.jpg: Closed book lying on wooden floor
    - open_book_nursery.png: Open book in children's room with teddy bears
    - open_book_carpet.png: Open book on carpet/rug
    - open_book_clean.png: Open book with clean white background
    """
    
    ASSETS_DIR = Path(__file__).parent.parent.parent / "assets" / "mockups"
    
    # Template assignments for each preview scene
    TEMPLATES = {
        0: "cover_template.jpg",      # Cover scene -> closed book
        1: "open_book_nursery.png",   # Scene 1 -> nursery setting
        5: "open_book_carpet.png",    # Scene 2 -> carpet setting  
        10: "open_book_clean.png",    # Scene 3 -> clean background
    }
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.api_key = self.settings.gemini_api_key
        
    async def create_mockup(
        self,
        scene_image_url: str,
        scene_number: int,
        book_title: Optional[str] = None,
    ) -> Optional[bytes]:
        """
        Create a photorealistic mockup by compositing the scene image onto a template.
        
        Args:
            scene_image_url: URL of the generated scene/cover image
            scene_number: Which scene (0=cover, 1/5/10=scenes)
            book_title: Optional title for cover mockup
            
        Returns:
            JPEG bytes of the mockup image, or None if failed
        """
        import httpx
        import asyncio
        
        # Get template for this scene
        template_name = self.TEMPLATES.get(scene_number, "open_book_clean.png")
        template_path = self.ASSETS_DIR / template_name
        
        if not template_path.exists():
            print(f"   ⚠️ Template not found: {template_path}")
            return None
            
        print(f"   📖 Creating mockup for scene {scene_number} using {template_name}...")
        
        try:
            # Download the scene image
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(scene_image_url)
                if resp.status_code != 200:
                    print(f"   ⚠️ Failed to download scene image: {resp.status_code}")
                    return None
                scene_bytes = resp.content
                
            # Load both images
            template_image = Image.open(template_path)
            scene_image = Image.open(BytesIO(scene_bytes))
            
            # Create the mockup using Nano-Banana-Pro
            mockup_bytes = await self._generate_mockup_with_ai(
                template_image=template_image,
                scene_image=scene_image,
                is_cover=(scene_number == 0),
                book_title=book_title,
            )
            
            return mockup_bytes
            
        except Exception as e:
            print(f"   ❌ Mockup creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _generate_mockup_with_ai(
        self,
        template_image: Image.Image,
        scene_image: Image.Image,
        is_cover: bool = False,
        book_title: Optional[str] = None,
    ) -> Optional[bytes]:
        """
        Use Gemini 2.5 Flash to composite the scene onto the template.
        """
        import asyncio
        
        loop = asyncio.get_event_loop()
        
        def run_sync():
            client = genai.Client(api_key=self.api_key)
            
            # Create the prompt based on mockup type
            if is_cover:
                prompt = (
                    f"Edit this image: Take the book illustration from the second image "
                    f"and place it as the cover artwork on the closed book in the first image. "
                    f"Make it look like a real printed hardcover book with the illustration as the cover. "
                    f"Keep the wooden floor background. Make it photorealistic. "
                    f"The result should look like a professional product photo of a children's book."
                )
            else:
                prompt = (
                    f"Edit this image: Take the illustration from the second image "
                    f"and place it on the right page of the open book in the first image. "
                    f"The left page should remain blank or have subtle text lines. "
                    f"Make it look like a real printed children's book with the illustration on the page. "
                    f"Keep the background setting (toys, carpet, etc). Make it photorealistic. "
                    f"The result should look like a professional product photo."
                )
            
            # Safety settings to allow children's content
            safety_settings = [
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
            ]
            
            print(f"   🎨 Calling Gemini 2.5 Flash for mockup generation...")
            
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash-image",
                    contents=[template_image, scene_image, prompt],
                    config=types.GenerateContentConfig(
                        safety_settings=safety_settings,
                        response_modalities=["image", "text"],
                    )
                )
                
                # Extract image from response
                if response.candidates:
                    for candidate in response.candidates:
                        if candidate.content and candidate.content.parts:
                            for part in candidate.content.parts:
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    image_data = part.inline_data.data
                                    if isinstance(image_data, str):
                                        image_data = base64.b64decode(image_data)
                                    print(f"   ✅ Mockup generated successfully!")
                                    return image_data
                
                print(f"   ⚠️ No image in response")
                return None
                
            except Exception as e:
                print(f"   ❌ Gemini API error: {e}")
                return None
        
        return await loop.run_in_executor(None, run_sync)
    
    async def create_all_mockups(
        self,
        scene_images: dict[int, str],  # scene_number -> image_url
        book_title: str,
    ) -> dict[int, Optional[bytes]]:
        """
        Create mockups for all provided scenes.
        
        Returns dict of scene_number -> mockup_bytes
        """
        import asyncio
        
        results = {}
        
        for scene_num, image_url in scene_images.items():
            mockup = await self.create_mockup(
                scene_image_url=image_url,
                scene_number=scene_num,
                book_title=book_title if scene_num == 0 else None,
            )
            results[scene_num] = mockup
            
        return results
