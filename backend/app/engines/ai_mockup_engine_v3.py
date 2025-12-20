"""
Storybook.ai - AI-Powered Mockup Generator V3
Uses Gemini 2.0 Flash (nano-banana-pro) with detailed prompts for each mockup type.
"""

import os
import base64
import tempfile
from pathlib import Path
from typing import Optional
from io import BytesIO

import httpx
from PIL import Image
from google import genai
from google.genai import types

from app.config import Settings, get_settings


class AIMockupEngineV3:
    """
    Creates photorealistic book mockups using Gemini 2.5 Flash AI.
    Uses detailed prompts for professional product photography quality.
    """
    
    ASSETS_DIR = Path(__file__).parent.parent.parent / "assets" / "mockups"
    COVER_REFS_DIR = Path(__file__).parent.parent.parent / "assets" / "cover_references"
    
    # Mockup templates for each scene type
    TEMPLATES = {
        0: "cover_template_v2.jpg",   # Cover scene -> closed book (User provided)
        1: "open_book_nursery.png",   # Scene 1 -> nursery setting
        7: "open_book_carpet.png",    # Scene 7 -> carpet setting  
        13: "open_book_clean.png",    # Scene 13 -> clean background
    }
    
    # Cover style references for different themes
    COVER_STYLE_REFS = {
        "pirates": "pirates.jpg",
        "princess": "princess.jpg",
        "dinos": "dinos.jpg",
        "underwater": "underwater.jpg",
        "forest": "forest.jpg",
        "space": "underwater.jpg",  # Use underwater as fallback for space
        "default": "forest.jpg",
    }
    
    # Inside page style references (nursery, carpet, clean)
    INSIDE_STYLE_REFS = {
        "nursery": "https://storage.googleapis.com/bookloo-assets/style_refs/inside_nursery_ref.jpg",
        "carpet": "https://storage.googleapis.com/bookloo-assets/style_refs/inside_carpet_ref.jpg",
        "clean": "https://storage.googleapis.com/bookloo-assets/style_refs/inside_clean_ref.jpg",
    }
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.api_key = self.settings.gemini_api_key
    
    def _get_cover_style_ref(self, theme: str = "") -> Optional[Image.Image]:
        """Load a cover style reference image based on theme."""
        ref_name = self.COVER_STYLE_REFS.get(theme.lower(), self.COVER_STYLE_REFS["default"])
        ref_path = self.COVER_REFS_DIR / ref_name
        if ref_path.exists():
            return Image.open(ref_path)
        return None
        
    def _get_style_ref_by_name(self, name: str) -> Optional[str]:
        """Get the URL for an inside page style reference."""
        return self.INSIDE_STYLE_REFS.get(name)
    
    def _get_cover_prompt(self, theme: str = "", book_title: str = "", child_name: str = "") -> str:
        """Professional product photography prompt for CLOSED BOOK with Title and immersive surroundings."""
        title_to_print = book_title or f"{child_name}s Abenteuer" if child_name else "Ein großes Abenteuer"
        return f"""ROLE: Professional Product Designer & Commercial Photographer
TASK: Design and photograph a personalized CLOSED HARDCOVER BOOK.

INPUTS:
- Image 1 (Template): A physical CLOSED white book on a wooden table.
- Image 2 (Artwork): High-resolution cover illustration.

EXECUTION:
1. TYPOGRAPHY (MANDATORY - TOP PRIORITY): 
   - Print the exact title "{title_to_print}" on the front cover.
   - POSITION: Top-center or Center, beautifully integrated into the artwork.
   - STYLE: Large, bold, readable children's book display font.
   - EFFECT: The text MUST look printed/embossed onto the physical book cover. 
   - NO PLACEHOLDERS: Ensure the actual name "{child_name}" is visible if it's part of the title.
2. ARTWORK APPLICATION:
   - Wrap Artwork (Image 2) edge-to-edge (FULL BLEED) onto the book in Image 1.
   - PERSPECTIVE: Match the 3D angle and volume of the book perfectly.
3. BLENDING: Maintain the realistic wooden table background and natural shadows.

STRICT CONSTRAINTS:
- YOU MUST PRINT THE TEXT "{title_to_print}" ON THE BOOK.
- THE BOOK MUST REMAIN CLOSED.
- NO WHITE MARGINS on the cover face.

OUTPUT: Ultra-high-end photorealistic result."""

    def _get_nursery_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK in NURSERY with AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
    def _get_nursery_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK in NURSERY with AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
        return f"""ROLE: Professional Product Photographer
TASK: Create a PHOTOREALISTIC PHOTO of an open children's book on a wooden table in a nursery.

INPUTS:
- Image 1 (Template): Photo of an open book in a nursery.
- Image 2 (Artwork): Illustration to be "printed" on the right page.

EXECUTION:
1. "PRINT" Image 2 onto the RIGHT PAGE of the book in Image 1.
   - FULL BLEED: The illustration must fill the ENTIRE right page, from the binding to the edges. NO WHITE BORDERS.
   - TEXTURE: The image must look like it is ink on paper. Match the paper grain, curve, and lighting of the real book.
   - SHADOWS: Preserve the shadow in the center fold (gutter) so it looks 3D.
2. TYPESETTING (Left Page):
   - "Print" the text content onto the LEFT PAGE.
   - Use a readable serif font (like 'Andika' or 'Garamond').
   - Text should follow the slight curve of the page.
{left_page_section}
LIGHTING: Soft, warm, cozy nursery lighting with bokeh in the background.

OUTPUT: A high-resolution PHOTO of the physical book. NOT a flat digital image."""

    def _get_carpet_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK on CARPET with AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
    def _get_carpet_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK on CARPET with AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
        return f"""ROLE: Lifestyle Photographer
TASK: Create a COZY OVERHEAD PHOTO of an open book lying on a textured carpet.

INPUTS:
- Image 1 (Template): Open book on a rug/carpet.
- Image 2 (Artwork): Illustration.

EXECUTION:
1. RIGHT PAGE INTEGRATION:
   - "Print" Image 2 onto the RIGHT PAGE.
   - FULL BLEED: Edge-to-edge coverage. The illustration must vanish into the binding fold.
   - REALISM: The image must interact with the paper texture and lighting. It should look like a printed page, not an overlay.
2. LEFT PAGE TEXT:
   - "Print" the text content clearly on the LEFT PAGE.
   - Ensure high contrast and readability.
{left_page_section}
LIGHTING: Warm, ambient indoor light. The paper should look slightly off-white/cream.

OUTPUT: A photorealistic lifestyle shot."""

    def _get_clean_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK with CLEAN background and AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
    def _get_clean_book_prompt(self, story_text: str = "") -> str:
        """Professional prompt for OPEN BOOK with CLEAN background and AGGRESSIVE Full Bleed."""
        left_page_section = self._get_left_page_section(story_text)
        return f"""ROLE: Commercial Product Photographer
TASK: Create a STUDIO PRO SHOT of an open book on a clean white surface.

INPUTS:
- Image 1 (Template): Open book on white/grey studio background.
- Image 2 (Artwork): Illustration.

EXECUTION:
1. PAGE COMPOSITION (Right Page):
   - Apply Image 2 to the RIGHT PAGE.
   - FULL BLEED: No margins. The image must go all the way to the edge.
   - PERSPECTIVE: Warp the image to match the book's 3D geometry perfectly.
   - SHADING: The center fold (gutter) must have a realistic shadow.
2. TYPOGRAPHY (Left Page):
   - professionally typeset the text on the LEFT PAGE.
   - Center alignment or justified.
{left_page_section}
LIGHTING: Bright, clean studio lighting. Soft shadows.

OUTPUT: A clean, commercial photorealistic book mockup."""

    def _get_left_page_section(self, story_text: str) -> str:
        """Professional typography requirements for the left page."""
        if not story_text:
            return ""
        return f"""
TYPOGRAPHY REQUIREMENTS (LEFT PAGE):
- TEXT CONTENT: "{story_text}"
- STYLE: Elegant, readable children's book typeface.
- PLACEMENT: Centered or slightly towards the outer margin.
- EFFECT: Text must follow the page's 3D warp and paper texture. No digital overlay look.
- CONTRAST: Ensure high readability against the paper color.
"""
    
    async def create_mockup(
        self,
        scene_image_url: str,
        scene_number: int,
        book_title: Optional[str] = None,
        story_text: Optional[str] = None,
        theme: Optional[str] = None,
        child_name: Optional[str] = None,
        character_reference_url: Optional[str] = None,
    ) -> Optional[bytes]:
        """
        Create a photorealistic mockup using Gemini 2.5 Flash.
        
        Args:
            scene_image_url: URL of the generated scene/cover image
            scene_number: Which scene (0=cover, 1/5/10=scenes)
            book_title: Optional title for cover mockup
            story_text: Optional story text for left page of open book mockups
            theme: Optional theme for cover style reference
            child_name: Optional child name for cover title
            
        Returns:
            JPEG bytes of the mockup image, or None if failed
        """
        import asyncio
        
        # Get template for this scene
        template_name = self.TEMPLATES.get(scene_number, "open_book_clean.png")
        template_path = self.ASSETS_DIR / template_name
        
        if not template_path.exists():
            print(f"   ⚠️ Template not found: {template_path}")
            return None
            
        print(f"🔍 DEBUG Mockup Engine: scene_number={scene_number}, template={template_name}")
        
        try:
            # 1. Download Scene/Cover Artwork
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.get(scene_image_url)
                if resp.status_code != 200:
                    print(f"   ⚠️ Failed to download scene image: {resp.status_code}")
                    return None
                scene_bytes = resp.content
                
            # 2. Load Images
            template_image = Image.open(template_path)
            scene_image = Image.open(BytesIO(scene_bytes))
            
            # 3. Handle Style References (Download if URL)
            style_ref_image = None
            if scene_number > 0:
                style_ref_name = "nursery" if template_name == "open_book_nursery.png" else \
                                 "carpet" if template_name == "open_book_carpet.png" else "clean"
                style_ref_url = self._get_style_ref_by_name(style_ref_name)
                
                if style_ref_url:
                    print(f"   🎨 Downloading style reference: {style_ref_name}")
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        s_resp = await client.get(style_ref_url)
                        if s_resp.status_code == 200:
                            style_ref_image = Image.open(BytesIO(s_resp.content))
            
            # 4. Determine Prompt & Style Reference
            if scene_number == 0:
                print(f"   📘 Using CLOSED BOOK cover logic for theme: {theme}")
                print(f"   ✍️ Printing Title: {book_title} (for {child_name})")
                prompt = self._get_cover_prompt(theme or "", book_title, child_name)
                # DISABLE style reference for cover as it might confuse Gemini regarding the name/title
                style_ref_image = None
            elif template_name == "open_book_nursery.png":
                print("   📖 Using OPEN BOOK (Nursery) logic")
                prompt = self._get_nursery_book_prompt(story_text or "")
            elif template_name == "open_book_carpet.png":
                print("   📖 Using OPEN BOOK (Carpet) logic")
                prompt = self._get_carpet_book_prompt(story_text or "")
            else:
                print("   📖 Using OPEN BOOK (Clean) logic")
                prompt = self._get_clean_book_prompt(story_text or "")
            
            # 5. Generate Mockup
            mockup_bytes = await self._call_gemini(
                template_image, 
                scene_image, 
                prompt,
                style_ref=style_ref_image,
                char_ref=None # Keeps it focused
            )
            
            return mockup_bytes
            
        except Exception as e:
            print(f"   ❌ Mockup creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _call_gemini(
        self,
        template_image: Image.Image,
        scene_image: Image.Image,
        prompt: str,
        style_ref: Optional[Image.Image] = None,
        char_ref: Optional[Image.Image] = None,
    ) -> Optional[bytes]:
        """Call Gemini 2.5 Flash to generate the mockup."""
        import asyncio
        
        loop = asyncio.get_event_loop()
        
        def run_sync():
            client = genai.Client(api_key=self.api_key)
            
            # Safety settings
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
            
            # Build contents list: template, scene, [style_ref if present], prompt
            contents = [template_image, scene_image]
            if style_ref is not None:
                contents.append(style_ref)
            if char_ref is not None:
                contents.append(char_ref)
            contents.append(prompt)
            
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash-image",
                    contents=contents,
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
                                    print(f"   ✅ AI Mockup generated successfully!")
                                    return image_data
                
                # Log if no image found
                print(f"   ⚠️ No image in Gemini response")
                if response.candidates:
                    for i, candidate in enumerate(response.candidates):
                        print(f"   Candidate {i}: finish_reason={candidate.finish_reason}")
                        if candidate.content:
                            for part in candidate.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    print(f"   Text response: {part.text[:200]}...")
                return None
                
            except Exception as e:
                print(f"   ❌ Gemini API error: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        return await loop.run_in_executor(None, run_sync)
