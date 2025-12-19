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
        0: "cover_template.jpg",      # Cover scene -> closed book
        1: "open_book_nursery.png",   # Scene 1 -> nursery setting
        5: "open_book_carpet.png",    # Scene 2 -> carpet setting  
        10: "open_book_clean.png",    # Scene 3 -> clean background
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
    
    def _get_cover_prompt(self, book_title: str = "", child_name: str = "") -> str:
        """Detailed prompt for cover mockup generation with style references."""
        title_text = book_title if book_title else f"{child_name}s Abenteuer"
        
        return f"""Create a beautiful children's book cover in the EXACT SAME STYLE as the reference cover image (third image).

You are provided with:
1. The mockup template (closed hardcover book on wooden floor) - FIRST image
2. The scene illustration with the personalized character - SECOND image  
3. A STYLE REFERENCE cover showing the exact design style to follow - THIRD image

YOUR TASK: Create a new cover that:
- Uses the EXACT CHILD CHARACTER FACE from the FOURTH image (portrait reference) and the SCENE ELEMENTS from the second image. 
- The face must be perfectly consistent with the child in the fourth image.
- Follows the EXACT DESIGN STYLE (typography, layout, colors) of the third reference image.
- Gets placed onto the book mockup from the first image.

CRITICAL STYLE REQUIREMENTS:
NO BRANDING:
- DO NOT add any logo, "bookloo" or "Storybook.ai" text to the cover.
- The entire cover should be free of any company branding, logos, or platform names.
- Even if the reference image (image 3) has a logo, DO NOT copy it.

TITLE DESIGN:
- Title: "{title_text}"
- Font: Warm golden/cream color with subtle dark outline (matches reference)
- Position: Top area of cover, very large, bold and prominent
- Style: Playful, child-friendly typography

ILLUSTRATION STYLE:
- 3D Pixar/Disney-quality character rendering
- Rich, vibrant, magical color palette
- The child character must be the central focus
- Magical/adventure elements matching the theme
- Dreamy, fantastical background with depth

OUTPUT: A complete book cover design on the mockup template, matching the premium quality and style of the reference image (without any logos or branding), featuring the personalized character."""

    def _get_nursery_book_prompt(self, story_text: str = "") -> str:
        """Prompt for open book with toys in background (Scene 1)."""
        left_page_section = self._get_left_page_section(story_text)
        
        return f"""Integrate the scene illustration onto the right page of an open children's book mockup with toys in the background.

You are provided with:
1. An open blank book mockup with colorful toys blurred in the background - this is the first image
2. A Pixar-style scene illustration (AI-generated, square format) - this is the second image

Your task: Seamlessly place the scene illustration on the RIGHT PAGE of the open book.

REQUIREMENTS:

Page Integration:
- Place the illustration on the right page only
- Match the page's perspective (book is lying flat, slight viewing angle from above)
- Apply realistic paper texture to make illustration look printed on the page
- Respect the natural page curve near the spine binding
- Ensure illustration fits within page margins (small white border around edges)

Lighting & Shadows:
- Match the warm children's room lighting from the mockup
- Add subtle shadows from page curvature onto the illustration
- Apply soft lighting consistent with the toy room ambiance
- Maintain the bokeh effect of the toy-filled background (keep it blurred)

Physical Accuracy:
- Simulate how ink looks on book paper (slight matte finish)
- Add paper grain texture overlay
- Respect the book's binding shadow running down the center
- Maintain all original background elements (toys, wooden floor, lighting)

Depth & Realism:
- The illustration should look flat on the page (not floating)
- Add subtle depth where the page meets the spine
- Apply realistic color bleeding (ink on paper effect)
- Ensure sharp focus on the book, blurred toys in background
{left_page_section}
OUTPUT: A photorealistic composite showing the scene illustration printed on the right page of an open children's book, with story text on the left page, and toys visible but blurred in the background."""

    def _get_carpet_book_prompt(self, story_text: str = "") -> str:
        """Prompt for open book on carpet (Scene 5)."""
        left_page_section = self._get_left_page_section(story_text)
        
        return f"""Integrate the scene illustration onto the right page of an open children's book mockup lying on a cozy carpet.

You are provided with:
1. An open blank book mockup on a textured carpet/rug with warm lighting - this is the first image
2. A Pixar-style scene illustration (AI-generated) - this is the second image

Your task: Seamlessly place the scene illustration on the RIGHT PAGE of the open book.

REQUIREMENTS:

Page Integration:
- Place the illustration on the right page only
- Match the page's perspective and natural curve
- Apply realistic paper texture
- Respect the book's binding and page margins

Lighting & Shadows:
- Match the warm, cozy lighting from the carpet setting
- Add natural shadows from page curvature
- Maintain the soft ambient lighting of the scene

Physical Accuracy:
- Simulate printed ink on book paper
- Keep the carpet texture visible and unchanged
- Maintain the book's natural appearance on the soft surface
{left_page_section}
OUTPUT: A photorealistic composite showing the scene illustration printed on the right page of an open book lying on a carpet, with story text on the left page."""

    def _get_clean_book_prompt(self, story_text: str = "") -> str:
        """Prompt for open book with clean background (Scene 10)."""
        left_page_section = self._get_left_page_section(story_text)
        
        return f"""Integrate the scene illustration onto the right page of an open children's book mockup with a clean white background.

You are provided with:
1. An open blank book mockup with a minimal, clean white background - this is the first image
2. A Pixar-style scene illustration (AI-generated) - this is the second image

Your task: Seamlessly place the scene illustration on the RIGHT PAGE of the open book.

REQUIREMENTS:

Page Integration:
- Place the illustration on the right page only
- Match the page's perspective perfectly
- Apply realistic paper texture
- Respect the book's straight-on viewing angle

Lighting & Shadows:
- Match the even, studio-style lighting
- Add subtle shadows in the binding area
- Maintain clean, professional product photography look

Physical Accuracy:
- Simulate high-quality book printing
- Keep the clean white background pristine
- Show the book's thickness and binding clearly
{left_page_section}
OUTPUT: A photorealistic composite showing the scene illustration printed on the right page of an open book with a clean, minimal background, and story text on the left page."""

    def _get_left_page_section(self, story_text: str) -> str:
        """Generate the left page text section for open book prompts."""
        if not story_text:
            return ""
        
        return f"""
LEFT PAGE (Text Page):
Display this story text matching to the picture: "{story_text}"

Formatting rules:
- Font: Child-friendly sans-serif (Andika/Comic Sans style)
- Font size: 18-22pt (readable for parents)
- Text color: Warm dark gray (#3A3A3A)
- Alignment: Left-aligned, 2-3cm margins
- Line spacing: 1.5x - 2x (generous)
- Text must look PRINTED on paper (not floating)
- Apply subtle paper texture beneath text
- No text cutoff or distortion
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
            
        print(f"   📖 Creating AI mockup for scene {scene_number} using {template_name}...")
        
        try:
            # Download the scene image
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.get(scene_image_url)
                if resp.status_code != 200:
                    print(f"   ⚠️ Failed to download scene image: {resp.status_code}")
                    return None
                scene_bytes = resp.content
                
            # Load images
            template_image = Image.open(template_path)
            scene_image = Image.open(BytesIO(scene_bytes))
            
            # For cover: load style reference image and optional character reference
            style_ref_image = None
            char_ref_image = None
            if scene_number == 0:
                style_ref_image = self._get_cover_style_ref(theme or "default")
                if style_ref_image:
                    print(f"   🎨 Using style reference for theme: {theme or 'default'}")
                
                if character_reference_url:
                    print(f"   👤 Using character reference portrait for cover...")
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        cref_resp = await client.get(character_reference_url)
                        if cref_resp.status_code == 200:
                            char_ref_image = Image.open(BytesIO(cref_resp.content))
            
            # Select appropriate prompt based on scene/template
            if scene_number == 0:
                prompt = self._get_cover_prompt(book_title or "", child_name or "")
            elif template_name == "open_book_nursery.png":
                prompt = self._get_nursery_book_prompt(story_text or "")
            elif template_name == "open_book_carpet.png":
                prompt = self._get_carpet_book_prompt(story_text or "")
            else:
                prompt = self._get_clean_book_prompt(story_text or "")
            
            # Generate mockup with AI
            mockup_bytes = await self._call_gemini(
                template_image, 
                scene_image, 
                prompt,
                style_ref=style_ref_image,
                char_ref=char_ref_image
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
