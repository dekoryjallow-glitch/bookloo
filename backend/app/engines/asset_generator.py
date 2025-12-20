"""
bookloo - Character Asset Generator
Creates a stylized Pixar character from a child's photo using nano-banana-pro (Google Gemini).

Step 1: nano-banana-pro → Creates Pixar portrait from photo
Step 2: FLUX Kontext → Uses portrait for scene generation (handled in image_engine.py)
"""

import asyncio
import base64
import httpx
import tempfile
import os
from dataclasses import dataclass
from typing import Optional
from PIL import Image
from io import BytesIO
import pillow_heif

# Register HEIF opener for Pillow
pillow_heif.register_heif_opener()

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
        """
        print(f"🎭 Generating Pixar Character with nano-banana-pro...")
        
        image_urls = []
        
        try:
            # Download the reference image
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
            
            print(f"   🎨 Calling nano-banana-pro (Gemini 2.5 Flash Image)...")
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
        Call Gemini 2.5 Flash Image for image transformation.
        """
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # PIL processing
                input_image = Image.open(BytesIO(image_bytes)).convert("RGB")
                
                # Resize if too large
                if max(input_image.size) > 1024:
                    input_image.thumbnail((1024, 1024), Image.LANCZOS)
                
                # Gemini call (Sync) -> but we'll run it in executor to avoid blocking
                def call_gemini(current_prompt):
                    # Use BLOCK_NONE to avoid safety false positives
                    safety_settings = [
                        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    ]
                    
                    return self.client.models.generate_content(
                        model="models/gemini-2.5-flash-image",
                        contents=[input_image, current_prompt],
                        config=types.GenerateContentConfig(
                            safety_settings=safety_settings
                        )
                    )

                # Fallback Prompt Logic: If first attempt fails, try a softer prompt
                current_prompt = prompt
                if attempt > 0:
                    print(f"   ⚠️ Switching to fallback prompt for attempt {attempt+1}...")
                    # Simpler prompt, removing specific style constraints that might trigger filters
                    current_prompt = (
                        "Transform this person into a 3D animated character. "
                        "Cartoon style, cute portrait, vibrant colors, smooth 3D render. "
                        "Keep the facial features and skin tone. "
                        "Clean white background."
                    )

                print(f"   📸 Attempt {attempt+1}/{max_attempts} with prompt: {current_prompt[:50]}...")
                response = await asyncio.get_event_loop().run_in_executor(None, lambda: call_gemini(current_prompt))
                
                # Extract image
                if response.candidates:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                data = part.inline_data.data
                                mime = part.inline_data.mime_type
                                
                                ext = "png" if "png" in mime else "jpg"
                                t_path = os.path.join(tempfile.gettempdir(), f"pixar_{os.urandom(4).hex()}.{ext}")
                                
                                img_bytes = base64.b64decode(data) if isinstance(data, str) else data
                                with open(t_path, 'wb') as f:
                                    f.write(img_bytes)
                                
                                return f"file://{t_path}"
                
                print(f"   ⚠️ No image in response (Attempt {attempt+1})")
                
                # Check for safety finish reason
                if response.candidates and response.candidates[0].finish_reason:
                     reason = response.candidates[0].finish_reason
                     print(f"   🛑 Finish Reason: {reason}")
                
                if attempt < max_attempts - 1:
                    await asyncio.sleep(2 * (attempt + 1))
                    
            except Exception as e:
                print(f"   ❌ Attempt {attempt+1} failed: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(2 * (attempt + 1))
                else:
                    return None
                    
        return None

    def _extract_url(self, output) -> str:
        """Extract URL from Replicate output (fallback)."""
        if isinstance(output, str):
            return output
        elif hasattr(output, 'url'):
            return output.url
        elif isinstance(output, list) and len(output) > 0:
            item = output[0]
            return str(item.url if hasattr(item, 'url') else item)
        else:
            result = list(output)
            if result:
                item = result[0]
                return str(item.url if hasattr(item, 'url') else item)
            raise ValueError(f"Unexpected output: {type(output)}")
