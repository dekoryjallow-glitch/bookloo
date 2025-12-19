"""
Storybook.ai - PDF Engine
Creates high-quality, print-ready PDFs optimized for Gelato (Hardcover 20x20).
Specs: 32 pages, 210x210mm Netto, specific page layout.
"""

import io
from typing import Optional, List
from pathlib import Path
import httpx
from PIL import Image as PILImage

from reportlab.lib.units import mm
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Frame, PageTemplate, BaseDocTemplate
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Gelato Specs for photobooks-hardcover_pf_200x200
PAGE_WIDTH = 210 * mm
PAGE_HEIGHT = 210 * mm
TARGET_DPI = 300

# Colors
PRIMARY_COLOR = HexColor("#2D3436")
SECONDARY_COLOR = HexColor("#636E72")

class PDFEngine:
    def __init__(self):
        self._register_fonts()
        self.main_font = "Helvetica"
        self.bold_font = "Helvetica-Bold"

    def _register_fonts(self):
        # Fallback to Helvetica for now, can be extended
        pass

    def _get_styles(self):
        return {
            "title": ParagraphStyle(
                name="Title",
                fontName="Helvetica-Bold",
                fontSize=28,
                alignment=1, # Center
                leading=34
            ),
            "story_text": ParagraphStyle(
                name="StoryText",
                fontName="Helvetica",
                fontSize=18,
                alignment=0, # Left
                leading=24
            ),
            "dedication": ParagraphStyle(
                name="Dedication",
                fontName="Helvetica",
                fontSize=20,
                alignment=1, # Center
                leading=26
            ),
            "credits": ParagraphStyle(
                name="Credits",
                fontName="Helvetica",
                fontSize=14,
                alignment=1, # Center
                leading=18
            )
        }

    async def generate_inner_pdf(self, scenes: List[any], child_name: str, book_title: str) -> bytes:
        """
        Generates the 32-page inner PDF content for Gelato.
        """
        buffer = io.BytesIO()
        doc = BaseDocTemplate(
            buffer,
            pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
            leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0
        )
        
        styles = self._get_styles()
        elements = []

        # --- Page 1: LEER (Weiß) ---
        elements.append(Spacer(1, PAGE_HEIGHT))
        elements.append(PageBreak())

        # --- Seite 2: Schmutztitel ---
        elements.append(Spacer(1, 80 * mm))
        elements.append(Paragraph(f"{book_title}", styles["title"]))
        elements.append(Spacer(1, 20 * mm))
        elements.append(Paragraph("Ein echtes bookloo Buch | bookloo.xyz", styles["credits"]))
        elements.append(PageBreak())

        # --- Seite 3: Widmung / Impressum ---
        elements.append(Spacer(1, 60 * mm))
        elements.append(Paragraph(f"Für {child_name}", styles["dedication"]))
        elements.append(PageBreak())

        # --- Seite 4 - 29 (13 Szenen) ---
        # Gerade: Text links. Ungerade: Bild rechts.
        for i in range(13):
            # Fallback if we have fewer than 13 scenes
            scene = scenes[i] if i < len(scenes) else None
            text = scene.narration_text if scene else ""
            img_url = scene.image_url if scene else None

            # Left Page (Text)
            elements.append(Spacer(1, 60 * mm))
            elements.append(Paragraph(text, styles["story_text"]))
            elements.append(PageBreak())

            # Right Page (Image)
            if img_url:
                img_data = await self._load_image(img_url)
                if img_data:
                    img = Image(img_data, width=PAGE_WIDTH, height=PAGE_HEIGHT)
                    elements.append(img)
                else:
                    elements.append(Spacer(1, PAGE_HEIGHT))
            else:
                elements.append(Spacer(1, PAGE_HEIGHT))
            elements.append(PageBreak())

        # --- Seite 30: Outro / Logo ---
        elements.append(Spacer(1, 80 * mm))
        elements.append(Paragraph("ENDE", styles["title"]))
        elements.append(PageBreak())

        # --- Seite 31: LEER ---
        elements.append(Spacer(1, PAGE_HEIGHT))
        elements.append(PageBreak())

        # --- Seite 32: Impressum ---
        elements.append(Spacer(1, 100 * mm))
        elements.append(Paragraph("Ein echtes bookloo Buch | bookloo.xyz", styles["credits"]))
        elements.append(Spacer(1, 10 * mm))
        elements.append(Paragraph("© 2024 bookloo AI", styles["credits"]))
        
        # Simple Frame for all pages
        frame = Frame(20*mm, 20*mm, PAGE_WIDTH-40*mm, PAGE_HEIGHT-40*mm, id='normal')
        # Background template for image pages could be added here
        template = PageTemplate(id='main', frames=[frame])
        # BUT: Image pages need full bleed (no padding). 
        # BaseDocTemplate can handle multiple templates, but for now we'll use one and adjust Spacer/Image widths.
        
        doc.addPageTemplates([template])
        doc.build(elements)
        
        return buffer.getvalue()

    async def generate_cover_pdf(self, cover_image_url: str, title: str, child_name: str, spine_width_mm: float) -> bytes:
        """
        Generates the cover PDF with dynamic spine width.
        """
        # Cover consists of Front (210) + Spine (X) + Back (210) + potential bleeds
        total_width = (210 + spine_width_mm + 210) * mm
        total_height = 210 * mm # (Simplified, actual Gelato cover includes wrap-around/bleed)
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(total_width, total_height))
        
        # Draw Front Cover (Right Side)
        front_x = (210 + spine_width_mm) * mm
        if cover_image_url:
            img_data = await self._load_image(cover_image_url)
            if img_data:
                c.drawImage(img_data, front_x, 0, width=210*mm, height=210*mm)
        
        # Draw Title on Front
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(front_x + 105*mm, 150*mm, title)
        c.setFont("Helvetica", 16)
        c.drawCentredString(front_x + 105*mm, 40*mm, f"Für {child_name}")

        # Draw Spine
        c.setFillColor(black)
        c.rect(210*mm, 0, spine_width_mm*mm, 210*mm, fill=1)
        c.saveState()
        c.translate((210 + spine_width_mm/2)*mm, 105*mm)
        c.rotate(90)
        c.setFillColor(white)
        c.setFont("Helvetica", 10)
        c.drawCentredString(0, 0, f"{title} — {child_name}")
        c.restoreState()

        # Draw Back Cover (Left Side)
        c.setFillColor(HexColor("#eeeeee"))
        c.rect(0, 0, 210*mm, 210*mm, fill=1)
        
        c.showPage()
        c.save()
        return buffer.getvalue()

    async def _load_image(self, url: str) -> Optional[io.BytesIO]:
        if not url: return None
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return io.BytesIO(response.content)
            except Exception as e:
                print(f"Error loading image {url}: {e}")
        return None
