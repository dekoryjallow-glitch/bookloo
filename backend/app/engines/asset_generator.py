"""
bookloo - Character Asset Generator
Creates a stylized Pixar character from a child's photo using nano-banana-pro (Google Gemini).

Step 1: nano-banana-pro → Creates Pixar portrait from photo
Step 2: FLUX Kontext → Uses portrait for scene generation (handled in image_engine.py)
"""

import asyncio
import base64
import httpx
from dataclasses import dataclass
from typing import Optional
from PIL import Image
from io import BytesIO

from app.config import Settings
from google import genai
from google.genai import types


@dataclass
class CharacterAsset:
    """A generated character asset with metadata."""
    image_urls: list[str]
    style: str
    prompt_used: str
    reference_photo_url: str


class AssetGenerator:
    """
    Generates Character Assets using nano-banana-pro (Google Gemini).
    
    nano-banana-pro is Google's state-of-the-art image generation model.
    Uses the Gemini API for image editing/generation.
    """
    
    # Pixar 3D style prompt for nano-banana
    PIXAR_STYLE_PROMPT = (
        "Transform this child into a 3D Pixar animated character. "
        "Disney concept art style, cute portrait, vibrant colors, smooth 3D render, "
        "subsurface scattering, big expressive eyes, cinematic lighting, 8k resolution. "
        "Keep the exact same facial features, skin tone, and ethnicity. "
        "Full body front view, clean white background, professional character concept art."
    )
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.gemini_api_key
        self.client = genai.Client(api_key=self.api_key)
    
    async def generate_character_asset(
        self,
        photo_url: str,
        style: str = "pixar_3d",
        child_age: int = 6,
        child_name: str = "child",
        num_poses: int = 1,
        features: Optional["CharacterTraits"] = None,
    ) -> CharacterAsset:
        """
        Generate a Pixar-style character from a child's photo using nano-banana-pro.
        
        Uses Google Gemini API with image editing capabilities.
        """
        print(f"🎭 Generating Pixar Character with nano-banana-pro...")
        print(f"   📷 Reference: {photo_url[:50]}...")
        if features:
            print(f"   📝 Using consistency string: {features.consistency_string}")
        
        image_urls = []
        
        try:
            # Download the reference image
            print(f"   📥 Downloading reference image...")
            image_bytes = await self._download_image(photo_url)
            
            # Build the prompt with features if available
            if features:
                prompt = (
                    f"Transform this child into a 3D Pixar animated character. "
                    f"The child has these features: {features.consistency_string}. "
                    f"CRITICAL: Keep the exact same facial features, skin tone ({features.skin_tone}), "
                    f"and ethnicity ({features.ethnicity}). "
                    f"Disney concept art style, cute portrait, vibrant colors, smooth 3D render, "
                    f"subsurface scattering, big expressive eyes, cinematic lighting, 8k resolution. "
                    f"Full body front view, clean white background, professional character concept art."
                )
            else:
                prompt = self.PIXAR_STYLE_PROMPT
            
            print(f"   🎨 Calling nano-banana-pro...")
            result_url = await self._run_nano_banana(image_bytes, prompt)
            
            if result_url:
                image_urls.append(result_url)
                print(f"   ✅ Character portrait generated!")
            else:
                print(f"   ❌ Failed to generate character portrait")
                
        except Exception as e:
            print(f"   ❌ nano-banana-pro error: {e}")
            import traceback
            traceback.print_exc()
        
        return CharacterAsset(
            image_urls=image_urls,
            style="pixar_3d",
            prompt_used=self.PIXAR_STYLE_PROMPT,
            reference_photo_url=photo_url,
        )
    
    async def _download_image(self, url: str) -> bytes:
        """Download an image from URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.content
    
    async def _run_nano_banana(self, image_bytes: bytes, prompt: str) -> Optional[str]:
        """
        Call nano-banana (Gemini 2.0 Flash) for image transformation.
        Uses multimodal input (image + text) to generate Pixar-style character.
        """
        loop = asyncio.get_event_loop()
        
        def run_sync():
            # Use pre-configured client
            client = self.client
            
            # Convert image bytes to PIL for processing
            input_image = Image.open(BytesIO(image_bytes))
            
            print(f"   📸 Calling nano-banana-pro (models/gemini-2.5-flash-image)...")
            
            # Configure safety to avoid blocking standard portraits
            safety_settings = [
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_ONLY_HIGH"
                ),
            ]
            
            # Use the correct nano-banana-pro model
            # The client handles PIL images directly in the contents list
            response = client.models.generate_content(
                model="models/gemini-2.5-flash-image",
                contents=[input_image, prompt],
                config=types.GenerateContentConfig(
                    safety_settings=safety_settings
                )
            )
            
            # Extract generated image from response
            if response.candidates:
                for i, candidate in enumerate(response.candidates):
                    # Log safety/finish reason
                    if candidate.finish_reason:
                        print(f"   ⚠️ Candidate {i} Finish Reason: {candidate.finish_reason}")
                        
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Got image data
                                image_data = part.inline_data.data
                                mime_type = part.inline_data.mime_type
                                
                                # Save to temp file
                                import tempfile
                                import os
                                
                                ext = "png" if "png" in mime_type else "jpg"
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"pixar_portrait_{os.urandom(4).hex()}.{ext}")
                                
                                # Decode and save
                                img_bytes = base64.b64decode(image_data) if isinstance(image_data, str) else image_data
                                with open(temp_path, 'wb') as f:
                                    f.write(img_bytes)
                                
                                print(f"   ✅ Image saved to: {temp_path}")
                                
                                # Upload to Firebase for public URL
                                # For now, return local path (will be handled in books.py)
                                return f"file://{temp_path}"
            
            print(f"   ⚠️ No image found in response. Candidates: {len(response.candidates or [])}")
            if response.candidates:
                 for i, c in enumerate(response.candidates):
                     if c.content and c.content.parts:
                         for part in c.content.parts:
                              if hasattr(part, 'text') and part.text:
                                  print(f"     Text: {part.text[:200]}")
            
            return None
        
        return await loop.run_in_executor(None, run_sync)
    
    def _extract_url(self, output) -> str:
        """Extract URL from Replicate output."""
        if isinstance(output, str):
            return output
        elif hasattr(output, 'url'):
            return output.url
        elif isinstance(output, list) and len(output) > 0:
            item = output[0]
            return str(item.url if hasattr(item, 'url') else item)
        else:
            # Try to iterate
            result = list(output)
            if result:
                item = result[0]
                return str(item.url if hasattr(item, 'url') else item)
            raise ValueError(f"Unexpected output: {type(output)}")
