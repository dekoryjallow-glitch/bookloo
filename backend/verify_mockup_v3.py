import asyncio
import os
from app.config import get_settings
from app.engines.ai_mockup_engine_v3 import AIMockupEngineV3

async def verify_mockups():
    print("🚀 Starting AIMockupEngineV3 Verification...")
    settings = get_settings()
    engine = AIMockupEngineV3(settings)
    
    # Placeholder image for artwork (a generic illustration)
    test_artwork_url = "https://images.unsplash.com/photo-1618331835717-801e976710b2?w=1024"
    
    # 1. Test Cover (Scene 0)
    print("\n📘 Testing Cover Mockup (Scene 0)...")
    cover = await engine.create_mockup(
        scene_image_url=test_artwork_url,
        scene_number=0,
        book_title="Kapitän Deko und der Schatz",
        child_name="Deko",
        theme="pirates"
    )
    if cover:
        with open("verify_v3_cover.jpg", "wb") as f:
            f.write(cover)
        print("✅ Cover saved to 'verify_v3_cover.jpg'")
    else:
        print("❌ Cover generation failed")

    # 2. Test Nursery Open Book (Scene 1)
    print("\n🧸 Testing Nursery Mockup (Scene 1)...")
    nursery = await engine.create_mockup(
        scene_image_url=test_artwork_url,
        scene_number=1,
        story_text="Es war einmal ein kleiner Bär, der wollte unbedingt das Meer sehen. Er packte seinen Koffer."
    )
    if nursery:
        with open("verify_v3_nursery.jpg", "wb") as f:
            f.write(nursery)
        print("✅ Nursery saved to 'verify_v3_nursery.jpg'")
    else:
        print("❌ Nursery generation failed")

    # 3. Test Carpet Open Book (Scene 7)
    print("\n🧶 Testing Carpet Mockup (Scene 7)...")
    carpet = await engine.create_mockup(
        scene_image_url=test_artwork_url,
        scene_number=7,
        story_text="Plötzlich fand er eine geheimnisvolle Karte auf dem Boden."
    )
    if carpet:
        with open("verify_v3_carpet.jpg", "wb") as f:
            f.write(carpet)
        print("✅ Carpet saved to 'verify_v3_carpet.jpg'")
    else:
        print("❌ Carpet generation failed")

if __name__ == "__main__":
    asyncio.run(verify_mockups())
