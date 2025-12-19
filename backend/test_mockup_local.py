"""
Test the MockupEngineV2 with local files
"""
import asyncio
from pathlib import Path
from PIL import Image
from io import BytesIO

# Simulate the mockup engine locally
ASSETS_DIR = Path("assets/mockups")

def test_composite():
    """Test compositing with local files"""
    
    # Create a test scene image (simple colored square)
    scene = Image.new("RGBA", (512, 512), color=(100, 150, 200, 255))
    
    # Load cover template
    template_path = ASSETS_DIR / "cover_template.jpg"
    template = Image.open(template_path).convert("RGBA")
    
    print(f"Template size: {template.size}")
    print(f"Scene size: {scene.size}")
    
    # Placement for cover
    x, y, w, h = 270, 200, 485, 600
    
    # Resize scene
    scene_resized = scene.resize((w, h), Image.Resampling.LANCZOS)
    print(f"Scene resized: {scene_resized.size}")
    
    # Composite
    result = template.copy()
    result.paste(scene_resized, (x, y))
    
    # Save result
    output_path = "test_mockup_result.jpg"
    result.convert("RGB").save(output_path, quality=92)
    print(f"✅ Saved to {output_path}")
    
    # Also test open book
    template2_path = ASSETS_DIR / "open_book_nursery.png"
    template2 = Image.open(template2_path).convert("RGBA")
    print(f"\nOpen book template size: {template2.size}")
    
    right_x, right_y, right_w, right_h = 530, 50, 440, 470
    scene2 = Image.new("RGBA", (512, 512), color=(200, 100, 150, 255))
    scene2_resized = scene2.resize((right_w, right_h), Image.Resampling.LANCZOS)
    
    result2 = template2.copy()
    result2.paste(scene2_resized, (right_x, right_y))
    
    output2_path = "test_mockup_openbook.jpg"
    result2.convert("RGB").save(output2_path, quality=92)
    print(f"✅ Saved to {output2_path}")

if __name__ == "__main__":
    test_composite()
