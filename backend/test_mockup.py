"""
Test the AI Mockup Engine directly
"""
import asyncio
from app.config import get_settings
from app.engines.ai_mockup_engine import AIMockupEngine

async def test_mockup():
    settings = get_settings()
    engine = AIMockupEngine(settings)
    
    print("Testing AI Mockup Engine...")
    print(f"Assets dir: {engine.ASSETS_DIR}")
    print(f"Templates: {list(engine.TEMPLATES.items())}")
    
    # Check if template files exist
    for scene_num, template_name in engine.TEMPLATES.items():
        template_path = engine.ASSETS_DIR / template_name
        exists = template_path.exists()
        print(f"  Scene {scene_num}: {template_name} - {'✅ EXISTS' if exists else '❌ MISSING'}")
        
    # Test with a sample image URL
    test_url = "https://firebasestorage.googleapis.com/v0/b/storybookai-3d5fa.appspot.com/o/books%2FKJsZNNHTWYEBnvOVCu3H%2Fscene_0.jpg?alt=media"
    
    print(f"\nTrying to create mockup for scene 0...")
    try:
        result = await engine.create_mockup(
            scene_image_url=test_url,
            scene_number=0,
            book_title="Test Book"
        )
        if result:
            print(f"✅ Mockup created! Size: {len(result)} bytes")
        else:
            print("❌ Mockup returned None")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mockup())
