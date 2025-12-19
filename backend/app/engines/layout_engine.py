"""
Storybook.ai - Layout Engine
Creates print-ready PDF books using ReportLab.

Specifications:
- Format: Square 21x21cm + 3mm bleed on all sides
- Resolution: Images placed at 300 DPI
- Structure:
  - Page 1: Cover (Title + Large Image + "Für [Name]")
  - Pages 2-21: Story (Left=Text, Right=Full Bleed Image)
  - Final Page: "Erstellt mit Storybook.ai"
"""

import io
from typing import Optional
from pathlib import Path
import httpx
from PIL import Image as PILImage

from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, 
    Paragraph, 
    Spacer, 
    Image, 
    PageBreak,
    Frame,
    PageTemplate,
    BaseDocTemplate,
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.config import Settings
from app.models.book import BookPage


# ============== Page Dimensions ==============
# 21cm x 21cm + 3mm bleed on all sides
PAGE_SIZE_CM = 21  # cm
BLEED_MM = 3  # mm

# Final page size including bleed
PAGE_WIDTH = (PAGE_SIZE_CM * 10 + BLEED_MM * 2) * mm  # 216mm
PAGE_HEIGHT = (PAGE_SIZE_CM * 10 + BLEED_MM * 2) * mm  # 216mm

# Safe area (inside bleed)
SAFE_MARGIN = BLEED_MM * mm + 10 * mm  # 13mm from edge

# DPI for image placement
TARGET_DPI = 300


# ============== Colors ==============
PRIMARY_COLOR = HexColor("#2D3436")
SECONDARY_COLOR = HexColor("#636E72")
ACCENT_COLOR = HexColor("#6C5CE7")
CREAM_BG = HexColor("#FDF6E3")


class LayoutEngine:
    """Creates print-ready PDF children's books."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._register_fonts()
    
    def _register_fonts(self):
        """Register custom fonts for children's book typography."""
        # Try to register Comic Neue or fallback to Helvetica
        # In production, you'd include the font files
        try:
            # Check if fonts exist in a fonts directory
            fonts_dir = Path(__file__).parent.parent / "fonts"
            
            if (fonts_dir / "ComicNeue-Regular.ttf").exists():
                pdfmetrics.registerFont(TTFont('ComicNeue', str(fonts_dir / "ComicNeue-Regular.ttf")))
                pdfmetrics.registerFont(TTFont('ComicNeue-Bold', str(fonts_dir / "ComicNeue-Bold.ttf")))
                self.main_font = "ComicNeue"
                self.bold_font = "ComicNeue-Bold"
            elif (fonts_dir / "Andika-Regular.ttf").exists():
                pdfmetrics.registerFont(TTFont('Andika', str(fonts_dir / "Andika-Regular.ttf")))
                pdfmetrics.registerFont(TTFont('Andika-Bold', str(fonts_dir / "Andika-Bold.ttf")))
                self.main_font = "Andika"
                self.bold_font = "Andika-Bold"
            else:
                # Fallback to built-in fonts
                self.main_font = "Helvetica"
                self.bold_font = "Helvetica-Bold"
        except Exception:
            self.main_font = "Helvetica"
            self.bold_font = "Helvetica-Bold"
    
    def _get_styles(self) -> dict:
        """Create paragraph styles for the book."""
        return {
            "title": ParagraphStyle(
                name="Title",
                fontName=self.bold_font,
                fontSize=48,
                leading=56,
                textColor=PRIMARY_COLOR,
                alignment=TA_CENTER,
            ),
            "dedication": ParagraphStyle(
                name="Dedication",
                fontName=self.main_font,
                fontSize=24,
                leading=30,
                textColor=SECONDARY_COLOR,
                alignment=TA_CENTER,
            ),
            "story_text": ParagraphStyle(
                name="StoryText",
                fontName=self.main_font,
                fontSize=22,
                leading=32,
                textColor=PRIMARY_COLOR,
                alignment=TA_LEFT,
            ),
            "page_number": ParagraphStyle(
                name="PageNumber",
                fontName=self.main_font,
                fontSize=12,
                textColor=SECONDARY_COLOR,
                alignment=TA_CENTER,
            ),
            "footer": ParagraphStyle(
                name="Footer",
                fontName=self.main_font,
                fontSize=18,
                leading=24,
                textColor=SECONDARY_COLOR,
                alignment=TA_CENTER,
            ),
        }
    
    async def create_pdf(
        self,
        pages: list[BookPage],
        child_name: str,
        book_title: Optional[str] = None,
    ) -> bytes:
        """
        Create a complete print-ready PDF book.
        
        Args:
            pages: List of BookPage objects (20 pages from 10 scenes)
            child_name: Name of the child (for dedication)
            book_title: Title of the book
        
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        
        # Create custom document
        doc = BaseDocTemplate(
            buffer,
            pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
            leftMargin=0,
            rightMargin=0,
            topMargin=0,
            bottomMargin=0,
        )
        
        styles = self._get_styles()
        story_elements = []
        
        # ====== Page 1: Cover ======
        cover_elements = await self._create_cover_page(
            title=book_title or f"{child_name}s Abenteuer",
            child_name=child_name,
            cover_image_url=pages[0].image_url if pages else None,
            styles=styles,
        )
        story_elements.extend(cover_elements)
        story_elements.append(PageBreak())
        
        # ====== Pages 2-21: Story Pages ======
        # We have 10 scenes, each with 2 pages (left=text, right=image)
        # Get unique scenes (every other page has the image)
        scenes = []
        for i in range(0, len(pages), 2):
            if i + 1 < len(pages):
                # Combine text from both pages of scene
                text = pages[i].text or pages[i + 1].text or ""
                image_url = pages[i].image_url or pages[i + 1].image_url
                scenes.append((text, image_url))
            elif pages[i].text or pages[i].image_url:
                scenes.append((pages[i].text or "", pages[i].image_url))
        
        for scene_num, (text, image_url) in enumerate(scenes, 1):
            # Left page: Text
            text_page = await self._create_text_page(
                text=text,
                page_number=scene_num * 2,
                styles=styles,
            )
            story_elements.extend(text_page)
            story_elements.append(PageBreak())
            
            # Right page: Full bleed image
            image_page = await self._create_image_page(
                image_url=image_url,
                page_number=scene_num * 2 + 1,
            )
            story_elements.extend(image_page)
            story_elements.append(PageBreak())
        
        # ====== Final Page: Credits ======
        credits_page = self._create_credits_page(child_name, styles)
        story_elements.extend(credits_page)
        
        # Build PDF with custom page template
        frame = Frame(
            0, 0, PAGE_WIDTH, PAGE_HEIGHT,
            leftPadding=0, rightPadding=0,
            topPadding=0, bottomPadding=0,
        )
        template = PageTemplate(id='main', frames=[frame])
        doc.addPageTemplates([template])
        
        doc.build(story_elements)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    async def _create_cover_page(
        self,
        title: str,
        child_name: str,
        cover_image_url: Optional[str],
        styles: dict,
    ) -> list:
        """Create the cover page."""
        elements = []
        
        # Background color frame (would be done with canvas in production)
        elements.append(Spacer(1, 40 * mm))
        
        # Title
        elements.append(Paragraph(title, styles["title"]))
        elements.append(Spacer(1, 20 * mm))
        
        # Cover image (centered, not full bleed)
        if cover_image_url:
            try:
                img_buffer = await self._load_image(cover_image_url)
                if img_buffer:
                    # Size image to fit with margins
                    img_size = 140 * mm  # Leave margins
                    img = Image(img_buffer, width=img_size, height=img_size)
                    img.hAlign = 'CENTER'
                    elements.append(img)
            except Exception as e:
                print(f"Error loading cover image: {e}")
        
        elements.append(Spacer(1, 20 * mm))
        
        # Dedication
        elements.append(Paragraph(f"Für {child_name}", styles["dedication"]))
        
        return elements
    
    async def _create_text_page(
        self,
        text: str,
        page_number: int,
        styles: dict,
    ) -> list:
        """Create a text page (left side of spread)."""
        elements = []
        
        # Cream/warm background would be added via canvas
        # Add padding from bleed area
        elements.append(Spacer(1, SAFE_MARGIN + 30 * mm))
        
        # Create a frame for the text with proper margins
        # The text should be well-padded from edges
        
        # Story text - wrapped in a container with margins
        text_with_margins = f'<para leftIndent="{int(SAFE_MARGIN)}" rightIndent="{int(SAFE_MARGIN)}">{text}</para>'
        
        # Use a padded paragraph
        padded_style = ParagraphStyle(
            name="PaddedText",
            parent=styles["story_text"],
            leftIndent=SAFE_MARGIN + 10 * mm,
            rightIndent=SAFE_MARGIN + 10 * mm,
        )
        
        elements.append(Paragraph(text, padded_style))
        
        # Page number at bottom
        elements.append(Spacer(1, 40 * mm))
        elements.append(Paragraph(f"— {page_number} —", styles["page_number"]))
        
        return elements
    
    async def _create_image_page(
        self,
        image_url: Optional[str],
        page_number: int,
    ) -> list:
        """Create a full-bleed image page (right side of spread)."""
        elements = []
        
        if image_url:
            try:
                img_buffer = await self._load_image(image_url)
                if img_buffer:
                    # Full bleed - image fills entire page including bleed area
                    img = Image(
                        img_buffer,
                        width=PAGE_WIDTH,
                        height=PAGE_HEIGHT,
                    )
                    img.hAlign = 'CENTER'
                    elements.append(img)
            except Exception as e:
                print(f"Error loading image for page {page_number}: {e}")
                # Add placeholder
                elements.append(Spacer(1, PAGE_HEIGHT))
        else:
            # Empty page placeholder
            elements.append(Spacer(1, PAGE_HEIGHT))
        
        return elements
    
    def _create_credits_page(
        self,
        child_name: str,
        styles: dict,
    ) -> list:
        """Create the final credits page."""
        elements = []
        
        elements.append(Spacer(1, 80 * mm))
        
        # "The End" or "Ende"
        end_style = ParagraphStyle(
            name="TheEnd",
            parent=styles["title"],
            fontSize=36,
        )
        elements.append(Paragraph("Ende", end_style))
        elements.append(Spacer(1, 30 * mm))
        
        # Dedication repeat
        elements.append(Paragraph(
            f"Diese Geschichte wurde speziell für {child_name} erstellt.",
            styles["footer"]
        ))
        elements.append(Spacer(1, 20 * mm))
        
        # Storybook.ai branding
        elements.append(Paragraph(
            "✨ Erstellt mit Storybook.ai ✨",
            styles["footer"]
        ))
        elements.append(Spacer(1, 10 * mm))
        elements.append(Paragraph(
            "Wo jedes Kind zum Helden wird.",
            styles["footer"]
        ))
        
        return elements
    
    async def _load_image(self, url: str) -> Optional[io.BytesIO]:
        """
        Download and prepare image for PDF insertion.
        Optimizes for 300 DPI output.
        """
        if not url:
            return None
            
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                img_buffer = io.BytesIO(response.content)
                
                # Open and optimize image
                img = PILImage.open(img_buffer)
                img = img.convert("RGB")
                
                # Calculate target size for 300 DPI
                # Full bleed page is 216mm x 216mm
                # At 300 DPI: 216mm = 8.5 inches = 2551 pixels
                target_pixels = int(216 / 25.4 * TARGET_DPI)  # ~2551
                
                # Resize if image is smaller (upscale for quality)
                # or much larger (downscale to save space)
                current_max = max(img.size)
                if current_max < target_pixels * 0.8 or current_max > target_pixels * 1.5:
                    # Calculate new size maintaining aspect ratio
                    ratio = target_pixels / current_max
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, PILImage.Resampling.LANCZOS)
                
                # Set DPI metadata
                output = io.BytesIO()
                img.save(output, format="JPEG", quality=95, dpi=(TARGET_DPI, TARGET_DPI))
                output.seek(0)
                
                return output
        
        return None


class LayoutEngineAdvanced(LayoutEngine):
    """
    Advanced layout engine with custom canvas drawing.
    Provides more control over backgrounds and visual elements.
    """
    
    async def create_pdf(
        self,
        pages: list[BookPage],
        child_name: str,
        book_title: Optional[str] = None,
    ) -> bytes:
        """Create PDF with custom canvas backgrounds."""
        buffer = io.BytesIO()
        
        c = canvas.Canvas(buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        styles = self._get_styles()
        
        # ====== Page 1: Cover ======
        await self._draw_cover(c, book_title or f"{child_name}s Abenteuer", 
                               child_name, pages[0].image_url if pages else None, styles)
        c.showPage()
        
        # ====== Story Pages ======
        scenes = []
        for i in range(0, len(pages), 2):
            if i + 1 < len(pages):
                text = pages[i].text or pages[i + 1].text or ""
                image_url = pages[i].image_url or pages[i + 1].image_url
                scenes.append((text, image_url))
        
        for scene_num, (text, image_url) in enumerate(scenes, 1):
            # Left page (text)
            await self._draw_text_page(c, text, scene_num * 2, styles)
            c.showPage()
            
            # Right page (image)
            await self._draw_image_page(c, image_url)
            c.showPage()
        
        # ====== Credits Page ======
        self._draw_credits(c, child_name, styles)
        c.showPage()
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    async def _draw_cover(self, c: canvas.Canvas, title: str, child_name: str,
                          image_url: Optional[str], styles: dict):
        """Draw cover page with custom canvas."""
        # Cream background
        c.setFillColor(CREAM_BG)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True)
        
        # Title
        c.setFillColor(PRIMARY_COLOR)
        c.setFont(self.bold_font, 42)
        title_y = PAGE_HEIGHT - 50 * mm
        
        # Center title (simple approach)
        text_width = c.stringWidth(title, self.bold_font, 42)
        x = (PAGE_WIDTH - text_width) / 2
        c.drawString(x, title_y, title)
        
        # Cover image
        if image_url:
            try:
                img_buffer = await self._load_image(image_url)
                if img_buffer:
                    img_size = 130 * mm
                    img_x = (PAGE_WIDTH - img_size) / 2
                    img_y = (PAGE_HEIGHT - img_size) / 2 - 10 * mm
                    c.drawImage(
                        img_buffer, img_x, img_y,
                        width=img_size, height=img_size,
                        preserveAspectRatio=True,
                    )
            except Exception as e:
                print(f"Cover image error: {e}")
        
        # Dedication
        c.setFont(self.main_font, 22)
        c.setFillColor(SECONDARY_COLOR)
        dedication = f"Für {child_name}"
        dec_width = c.stringWidth(dedication, self.main_font, 22)
        c.drawString((PAGE_WIDTH - dec_width) / 2, 35 * mm, dedication)
    
    async def _draw_text_page(self, c: canvas.Canvas, text: str, 
                               page_num: int, styles: dict):
        """Draw text page with warm background."""
        # Warm background
        c.setFillColor(CREAM_BG)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True)
        
        # Text area
        c.setFillColor(PRIMARY_COLOR)
        c.setFont(self.main_font, 20)
        
        # Wrap and draw text
        text_x = SAFE_MARGIN + 15 * mm
        text_y = PAGE_HEIGHT - SAFE_MARGIN - 40 * mm
        max_width = PAGE_WIDTH - 2 * (SAFE_MARGIN + 15 * mm)
        
        # Simple text wrapping
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, self.main_font, 20) < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        line_height = 30
        for i, line in enumerate(lines):
            c.drawString(text_x, text_y - i * line_height, line)
        
        # Page number
        c.setFont(self.main_font, 12)
        c.setFillColor(SECONDARY_COLOR)
        pn = f"— {page_num} —"
        pn_width = c.stringWidth(pn, self.main_font, 12)
        c.drawString((PAGE_WIDTH - pn_width) / 2, SAFE_MARGIN + 10 * mm, pn)
    
    async def _draw_image_page(self, c: canvas.Canvas, image_url: Optional[str]):
        """Draw full-bleed image page."""
        if image_url:
            try:
                img_buffer = await self._load_image(image_url)
                if img_buffer:
                    # Full bleed - cover entire page
                    c.drawImage(
                        img_buffer, 0, 0,
                        width=PAGE_WIDTH, height=PAGE_HEIGHT,
                        preserveAspectRatio=False,  # Fill entire page
                    )
            except Exception as e:
                print(f"Image page error: {e}")
                # White fallback
                c.setFillColor(white)
                c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True)
        else:
            c.setFillColor(white)
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True)
    
    def _draw_credits(self, c: canvas.Canvas, child_name: str, styles: dict):
        """Draw credits page."""
        # Cream background
        c.setFillColor(CREAM_BG)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True)
        
        # "Ende"
        c.setFillColor(PRIMARY_COLOR)
        c.setFont(self.bold_font, 36)
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 30 * mm, "Ende")
        
        # Credits text
        c.setFont(self.main_font, 16)
        c.setFillColor(SECONDARY_COLOR)
        
        line1 = f"Diese Geschichte wurde speziell für {child_name} erstellt."
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 10 * mm, line1)
        
        c.setFont(self.main_font, 18)
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 40 * mm, "✨ Erstellt mit Storybook.ai ✨")
        
        c.setFont(self.main_font, 14)
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 60 * mm, "Wo jedes Kind zum Helden wird.")
