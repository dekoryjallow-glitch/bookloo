"""
Direct test of Cover Mockup with Style Reference
"""
import asyncio
from PIL import Image
from app.config import get_settings
from app.engines.ai_mockup_engine_v3 import AIMockupEngineV3

async def test_cover_with_style():
    settings = get_settings()
    engine = AIMockupEngineV3(settings)
    
    print("=" * 60)
    print("Testing Cover Mockup with Style Reference")
    print("=" * 60)
    
    # Check style refs
    print(f"\nCover refs dir: {engine.COVER_REFS_DIR}")
    print(f"Available refs: {list(engine.COVER_STYLE_REFS.keys())}")
    
    # Try to load a style ref
    style_ref = engine._get_cover_style_ref("space")
    if style_ref:
        print(f"✅ Style ref loaded: {style_ref.size}")
    else:
        print("❌ Style ref NOT loaded!")
        
    # Check the prompt
    prompt = engine._get_cover_prompt("Dekos Abenteuer", "Deko")
    print(f"\n--- PROMPT ---")
    print(prompt[:500])
    print("...")
    
    # Test with a sample scene image
    test_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=512"
    
    print(f"\n\nGenerating cover mockup with style reference...")
    result = await engine.create_mockup(
        scene_image_url=test_url,
        scene_number=0,
        book_title="Dekos Abenteuer",
        theme="space",
        child_name="Deko",
    )
    
    if result:
        output_path = "test_cover_with_style.jpg"
        with open(output_path, "wb") as f:
            f.write(result)
        print(f"\n✅ Cover saved to {output_path}")
        print(f"   Size: {len(result)} bytes")
    else:
        print("\n❌ Cover generation failed!")

if __name__ == "__main__":
    asyncio.run(test_cover_with_style())
