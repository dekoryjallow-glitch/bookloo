"""
Storybook.ai - Mockup Generator V2
Uses PIL to composite generated illustrations onto book mockup templates.
Faster and more reliable than AI-based compositing.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional
from io import BytesIO

import httpx
from PIL import Image

from app.config import Settings, get_settings


class MockupEngineV2:
    """
    Creates photorealistic book mockups using PIL image compositing.
    
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
    
    # Placement coordinates for each template
    # Cover template is 1024x1024, book is centered
    # Open book templates are 1024x571, pages are left/right halves
    PLACEMENTS = {
        # Cover: illustration fills the book cover area (centered, square aspect)
        "cover_template.jpg": {
            "type": "cover",
            "x": 270,  # Center horizontally on cover
            "y": 200,  # Top of cover
            "width": 485,  # Cover width
            "height": 600,  # Cover height
        },
        # Open books: illustration on the right page (each page ~45% of width)
        "open_book_nursery.png": {
            "type": "open_book",
            "left_x": 50, "left_y": 50, "left_w": 440, "left_h": 470,  # Left page
            "right_x": 530, "right_y": 50, "right_w": 440, "right_h": 470,  # Right page
        },
        "open_book_carpet.png": {
            "type": "open_book",
            "left_x": 55, "left_y": 40, "left_w": 430, "left_h": 480,
            "right_x": 535, "right_y": 40, "right_w": 430, "right_h": 480,
        },
        "open_book_clean.png": {
            "type": "open_book",
            "left_x": 32, "left_y": 25, "left_w": 450, "left_h": 520,
            "right_x": 540, "right_y": 25, "right_w": 450, "right_h": 520,
        },
    }
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        
    async def create_mockup(
        self,
        scene_image_url: str,
        scene_number: int,
        book_title: Optional[str] = None,
    ) -> Optional[bytes]:
        """
        Create a mockup by compositing the scene image onto a template.
        
        Args:
            scene_image_url: URL of the generated scene/cover image
            scene_number: Which scene (0=cover, 1/5/10=scenes)
            book_title: Optional title for cover mockup
            
        Returns:
            JPEG bytes of the mockup image, or None if failed
        """
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
            template = Image.open(template_path).convert("RGBA")
            scene = Image.open(BytesIO(scene_bytes)).convert("RGBA")
            
            # Get placement info
            placement = self.PLACEMENTS.get(template_name)
            if not placement:
                print(f"   ⚠️ No placement info for {template_name}")
                return None
            
            # Composite based on type
            if placement["type"] == "cover":
                result = self._composite_cover(template, scene, placement)
            else:
                result = self._composite_open_book(template, scene, placement)
            
            # Convert to JPEG bytes
            output = BytesIO()
            result_rgb = result.convert("RGB")
            result_rgb.save(output, format="JPEG", quality=92)
            output.seek(0)
            
            print(f"   ✅ Mockup created successfully!")
            return output.read()
            
        except Exception as e:
            print(f"   ❌ Mockup creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _composite_cover(self, template: Image.Image, scene: Image.Image, placement: dict) -> Image.Image:
        """Composite illustration onto closed book cover."""
        # Resize scene to fit cover area
        scene_resized = scene.resize((placement["width"], placement["height"]), Image.Resampling.LANCZOS)
        
        # Create a copy of template
        result = template.copy()
        
        # Paste scene onto cover
        result.paste(scene_resized, (placement["x"], placement["y"]), scene_resized if scene_resized.mode == 'RGBA' else None)
        
        return result
    
    def _composite_open_book(self, template: Image.Image, scene: Image.Image, placement: dict) -> Image.Image:
        """Composite illustration onto right page of open book."""
        # Resize scene to fit right page
        scene_resized = scene.resize(
            (placement["right_w"], placement["right_h"]), 
            Image.Resampling.LANCZOS
        )
        
        # Create a copy of template
        result = template.copy()
        
        # Paste scene onto right page
        result.paste(
            scene_resized, 
            (placement["right_x"], placement["right_y"]), 
            scene_resized if scene_resized.mode == 'RGBA' else None
        )
        
        return result
