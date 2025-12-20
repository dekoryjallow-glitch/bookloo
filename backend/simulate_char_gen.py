import asyncio
import os
from app.config import get_settings
from app.engines.asset_generator import AssetGenerator
from dotenv import load_dotenv

async def simulate_character_gen():
    load_dotenv()
    settings = get_settings()
    generator = AssetGenerator(settings)
    
    # Use a real photo of a person (public URL)
    test_photo_url = "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800"
    
    print("🚀 Simulating Character Generation...")
    try:
        asset = await generator.generate_character_asset(test_photo_url, child_name="Test")
        if asset.image_urls:
            print(f"✅ Success! Generated URL: {asset.image_urls[0]}")
        else:
            print("❌ Failed (No URLs)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_character_gen())
