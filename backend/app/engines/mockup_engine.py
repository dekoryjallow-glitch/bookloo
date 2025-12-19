"""
Storybook.ai - Mockup Engine
Transforms flat AI images into photorealistic book mockups.
"""

import os
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import httpx
from app.config import get_settings

class MockupEngine:
    def __init__(self):
        self.settings = get_settings()
        self.assets_dir = os.path.join(os.getcwd(), "assets")
        self.font_path = os.path.join(os.getcwd(), "assets", "fonts", "Andika-Regular.ttf") # Fallback needed if missing
        
        # Define Coordinates for Perspective Transform
        # Top-Left, Top-Right, Bottom-Right, Bottom-Left
        
        # 1. Open Book - Right Page (Image)
        self.OPEN_RIGHT_COORDS = [(650, 50), (1200, 80), (1150, 850), (650, 800)] 
        # Fine-tune these based on the actual PNG template
        # Need to be precise. 
        # Assumption for generic open book:
        # Template size: ~1200x900? 
        # I'll implement a generic perspective warp function.
        
        # Let's use simpler logic first if coordinates are unknown.
        # But user asked for "perspective transformation".
        
    def find_coeffs(self, source_coords, target_coords):
        matrix = []
        for s, t in zip(source_coords, target_coords):
            matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
            matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
        A = np.matrix(matrix, dtype=float)
        B = np.array(source_coords).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

    async def create_open_book_mockup(self, scene_image_url: str, story_text: str) -> bytes:
        """
        Creates a mockup of an open book with text on left, image on right.
        """
        # 1. Load Template
        template_path = os.path.join(self.assets_dir, "mockup_open.png")
        if not os.path.exists(template_path):
             print(f"⚠️ Mockup template not found at {template_path}")
             # Return original image bytes if template missing
             async with httpx.AsyncClient() as client:
                resp = await client.get(scene_image_url)
                return resp.content

        template = Image.open(template_path).convert("RGBA")
        width, height = template.size
        
        # 2. Load Scene Image
        async with httpx.AsyncClient() as client:
            resp = await client.get(scene_image_url)
            scene_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            
        # 3. Apply Perspective Transform for Right Page
        # Target coordinates on the template (approximate, user should fine tune)
        # Let's assume the Right Page is roughly the right half
        # Format: Top-Left, Bottom-Left, Bottom-Right, Top-Right (Standard PIL Quad)
        # Wait, PIL transform uses specific order.
        
        # Coordinates for "Right Page" in `mockup_open.png`
        # These need to be calibrated. I will use safe estimates.
        # Assuming 1000x1000 template check? No, likely rectangular.
        
        # Using a standard perspective warp logic
        # For now, simply resizing to fit right half to maintain speed if perspective is complex without precise coords.
        # BUT user asked for perspective.
        
        # Let's define reasonable coordinates for a "standard" open book view
        # TL, BL, BR, TR
        right_page_coeffs = [(width*0.52, height*0.15), (width*0.52, height*0.85), (width*0.92, height*0.80), (width*0.92, height*0.20)]
        
        # Warp Image
        scene_img_warped = self._warp_image(scene_img, right_page_coeffs, (width, height))
        
        # 4. Create Text Image (Left Page)
        text_img = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0)) # Transparent
        draw = ImageDraw.Draw(text_img)
        
        # Try to load font
        try:
             font = ImageFont.truetype("arial.ttf", 40)
        except:
             font = ImageFont.load_default()
             
        # Simple text wrapping
        import textwrap
        lines = textwrap.wrap(story_text, width=30)
        y_text = 200
        for line in lines:
            draw.text((100, y_text), line, font=font, fill="black")
            y_text += 50
            
        # Warp Text
        left_page_coeffs = [(width*0.08, height*0.20), (width*0.08, height*0.80), (width*0.48, height*0.85), (width*0.48, height*0.15)]
        text_img_warped = self._warp_image(text_img, left_page_coeffs, (width, height))
        
        # 5. Composite
        # Multiply blend for shadows?
        # Standard paste for now, alpha composite
        final = Image.alpha_composite(template, scene_img_warped)
        final = Image.alpha_composite(final, text_img_warped)
        
        # Return bytes
        output = BytesIO()
        final.convert("RGB").save(output, format="JPEG", quality=90)
        return output.getvalue()

    async def create_cover_mockup(self, cover_image_url: str, title: str) -> bytes:
        """
        Creates a hardcover mockup.
        """
        template_path = os.path.join(self.assets_dir, "mockup_cover.jpg")
        # Note: user might have provided jpg.
        if not os.path.exists(template_path):
             template_path = os.path.join(self.assets_dir, "mockup_cover.png")
             
        if not os.path.exists(template_path):
             async with httpx.AsyncClient() as client:
                resp = await client.get(cover_image_url)
                return resp.content
                
        template = Image.open(template_path).convert("RGBA")
        width, height = template.size
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(cover_image_url)
            cover_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            
        # Cover area coordinates (Center book)
        # TL, BL, BR, TR
        cover_coeffs = [(width*0.25, height*0.15), (width*0.25, height*0.85), (width*0.75, height*0.85), (width*0.75, height*0.15)]
        # This is a flat lay assumption.
        
        cover_warped = self._warp_image(cover_img, cover_coeffs, (width, height))
        
        final = Image.alpha_composite(template, cover_warped)
        
        output = BytesIO()
        final.convert("RGB").save(output, format="JPEG", quality=90)
        return output.getvalue()
        
    def _warp_image(self, img, coords, size):
        """
        Warp img to the generic quad coords [(x,y)...] within size (w,h).
        Uses simple perspective transform.
        """
        target_w, target_h = size
        
        # Source points (full image)
        w, h = img.size
        src = np.array([0, 0, 0, h, w, h, w, 0], dtype=np.float32).reshape(4, 2)
        
        # Destination points
        # PIL wants flattened quad for 'transform' method, 
        # BUT Image.PERSPECTIVE requires the 8-coefficient matrix inverse.
        
        # Simplify: Use finding coefficients logic
        dst = np.array([c for c in coords], dtype=np.float32)
        
        # Calculate coefficients
        matrix = self._calculate_perspective_coeffs(src, dst)
        
        return img.transform(size, Image.PERSPECTIVE, matrix, Image.BICUBIC)

    def _calculate_perspective_coeffs(self, src, dst):
        """
        Calculate the 8 coefficients for PIL's Perspective Transform.
        Logic: Use linear algebra to map src rect to dst quad.
        """
        matrix = []
        for s, d in zip(src, dst):
            matrix.append([s[0], s[1], 1, 0, 0, 0, -s[0]*d[0], -s[0]*d[1]])
            matrix.append([0, 0, 0, s[0], s[1], 1, -s[1]*d[0], -s[1]*d[1]])

        A = np.matrix(matrix, dtype=float)
        B = np.array(dst).reshape(8)
        
        # Solve
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8).tolist()
