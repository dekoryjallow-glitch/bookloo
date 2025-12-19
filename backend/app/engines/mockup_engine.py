"""
Storybook.ai - Mockup Engine
Transforms flat AI images into photorealistic book mockups.

Quality Features:
- Super-sampling (2x resolution for anti-aliasing)
- Improved text rendering (#222222, 90% opacity)
- Image sharpening after perspective warp
"""

import os
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import httpx
from app.config import get_settings

# Text color for realistic "printed" look
TEXT_COLOR = (34, 34, 34, 230)  # #222222 with 90% opacity

class MockupEngine:
    def __init__(self):
        self.settings = get_settings()
        self.assets_dir = os.path.join(os.getcwd(), "assets")
        self.font_path = os.path.join(os.getcwd(), "assets", "fonts", "Andika-Regular.ttf")
        
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
        Uses super-sampling for crisp text and sharp images.
        """
        # 1. Load Template
        template_path = os.path.join(self.assets_dir, "mockup_open.png")
        if not os.path.exists(template_path):
             print(f"⚠️ Mockup template not found at {template_path}")
             async with httpx.AsyncClient() as client:
                resp = await client.get(scene_image_url)
                return resp.content

        template_orig = Image.open(template_path).convert("RGBA")
        orig_width, orig_height = template_orig.size
        
        # === SUPER-SAMPLING: Work at 2x resolution ===
        scale = 2
        width, height = orig_width * scale, orig_height * scale
        template = template_orig.resize((width, height), Image.LANCZOS)
        
        # 2. Load Scene Image
        async with httpx.AsyncClient() as client:
            resp = await client.get(scene_image_url)
            scene_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            
        # 3. Apply Perspective Transform for Right Page
        right_page_coeffs = [
            (width*0.52, height*0.15), 
            (width*0.52, height*0.85), 
            (width*0.92, height*0.80), 
            (width*0.92, height*0.20)
        ]
        
        # Warp Image
        scene_img_warped = self._warp_image(scene_img, right_page_coeffs, (width, height))
        
        # === SHARPEN the warped image to recover detail ===
        scene_img_warped = scene_img_warped.filter(ImageFilter.SHARPEN)
        
        # 4. Create Text Image (Left Page) - at 2x resolution
        text_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_img)
        
        # Font size scaled for 2x resolution
        font_size = 80  # 40 * 2
        try:
            if os.path.exists(self.font_path):
                font = ImageFont.truetype(self.font_path, font_size)
            else:
                font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
              
        # Simple text wrapping
        import textwrap
        lines = textwrap.wrap(story_text, width=30)
        y_text = int(height * 0.25)  # Start at 25% from top
        line_spacing = int(font_size * 1.3)
        
        for line in lines:
            # Calculate x position for centered text on left page
            x_text = int(width * 0.15)
            draw.text((x_text, y_text), line, font=font, fill=TEXT_COLOR)
            y_text += line_spacing
            
        # Warp Text
        left_page_coeffs = [
            (width*0.08, height*0.20), 
            (width*0.08, height*0.80), 
            (width*0.48, height*0.85), 
            (width*0.48, height*0.15)
        ]
        text_img_warped = self._warp_image(text_img, left_page_coeffs, (width, height))
        
        # 5. Composite
        final = Image.alpha_composite(template, scene_img_warped)
        final = Image.alpha_composite(final, text_img_warped)
        
        # === DOWNSAMPLE back to original size for anti-aliasing ===
        final = final.resize((orig_width, orig_height), Image.LANCZOS)
        
        # Return bytes
        output = BytesIO()
        final.convert("RGB").save(output, format="JPEG", quality=92)
        return output.getvalue()

    async def create_cover_mockup(self, cover_image_url: str, title: str) -> bytes:
        """
        Creates a hardcover mockup.
        Uses super-sampling for crisp output.
        """
        template_path = os.path.join(self.assets_dir, "mockup_cover.jpg")
        if not os.path.exists(template_path):
             template_path = os.path.join(self.assets_dir, "mockup_cover.png")
             
        if not os.path.exists(template_path):
             async with httpx.AsyncClient() as client:
                resp = await client.get(cover_image_url)
                return resp.content
        
        template_orig = Image.open(template_path).convert("RGBA")
        orig_width, orig_height = template_orig.size
        
        # === SUPER-SAMPLING: Work at 2x resolution ===
        scale = 2
        width, height = orig_width * scale, orig_height * scale
        template = template_orig.resize((width, height), Image.LANCZOS)
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(cover_image_url)
            cover_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            
        # Cover area coordinates (Center book) - scaled to 2x
        cover_coeffs = [
            (width*0.25, height*0.15), 
            (width*0.25, height*0.85), 
            (width*0.75, height*0.85), 
            (width*0.75, height*0.15)
        ]
        
        cover_warped = self._warp_image(cover_img, cover_coeffs, (width, height))
        
        # === SHARPEN the warped cover image ===
        cover_warped = cover_warped.filter(ImageFilter.SHARPEN)
        
        final = Image.alpha_composite(template, cover_warped)
        
        # === DOWNSAMPLE back to original size for anti-aliasing ===
        final = final.resize((orig_width, orig_height), Image.LANCZOS)
        
        output = BytesIO()
        final.convert("RGB").save(output, format="JPEG", quality=92)
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
