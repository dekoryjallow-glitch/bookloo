
import asyncio
import os
from app.config import get_settings
from app.engines.asset_generator import AssetGenerator

async def test_asset_generator():
    settings = get_settings()
    generator = AssetGenerator(settings)
    
    print("=" * 60)
    print("Testing AssetGenerator (Gemini)")
    print("=" * 60)
    
    # Use a dummy image or download one
    image_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=512"
    
    try:
        asset = await generator.generate_character_asset(
            photo_url=image_url,
            child_name="TestChild",
            style="pixar_3d"
        )
        
        if asset and asset.image_urls:
            print(f"\n✅ Asset generated successfully!")
            print(f"   URL: {asset.image_urls[0]}")
        else:
            print("\n❌ Asset generation failed (no URLs).")
            
    except Exception as e:
        print(f"\n❌ Exception during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_asset_generator())
