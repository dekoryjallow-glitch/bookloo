"""
Test AIMockupEngineV3 - Cover Mockup Generation
"""
import asyncio
from app.config import get_settings
from app.engines.ai_mockup_engine_v3 import AIMockupEngineV3

async def test_cover_mockup():
    settings = get_settings()
    engine = AIMockupEngineV3(settings)
    
    print("=" * 60)
    print("Testing Cover Mockup Generation")
    print("=" * 60)
    
    # Use a sample scene image URL (replace with actual generated scene)
    # This is just a placeholder - in production, this would be the generated cover art
    test_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=512"
    
    print(f"Template: {engine.TEMPLATES[0]}")
    print(f"Scene URL: {test_url}")
    print()
    
    result = await engine.create_mockup(
        scene_image_url=test_url,
        scene_number=0,
        book_title="Test Cover"
    )
    
    if result:
        # Save result
        output_path = "test_ai_cover_mockup.jpg"
        with open(output_path, "wb") as f:
            f.write(result)
        print(f"\n✅ Cover mockup saved to {output_path}")
        print(f"   Size: {len(result)} bytes")
    else:
        print("\n❌ Cover mockup generation failed!")

if __name__ == "__main__":
    asyncio.run(test_cover_mockup())
