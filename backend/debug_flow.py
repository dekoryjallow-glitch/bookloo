"""
Test script to debug generation flow
Run with: python debug_flow.py
"""
import asyncio
from dotenv import load_dotenv
load_dotenv(".env")

from app.config import get_settings
from app.engines.story_engine import StoryEngine
from app.engines.image_engine import ImageEngineWithRetry

async def test_story_generation():
    print("="*50)
    print("STEP 1: Testing Story Generation")
    print("="*50)
    settings = get_settings()
    engine = StoryEngine(settings)
    
    try:
        story = await engine.generate_story(
            name="TestKind",
            theme="magic",  # The theme user is using
            age=6,
            style="pixar_3d",
            character_description="cute 6 year old child named TestKind"
        )
        print(f"✅ Story generated: {story.title}")
        print(f"   Scenes: {len(story.scenes)}")
        for s in story.scenes[:3]:
            print(f"   - Scene {s.scene_number}: {s.narration_text[:50]}...")
        return story
    except Exception as e:
        print(f"❌ Story generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_image_generation():
    print("\n" + "="*50)
    print("STEP 2: Testing Image Generation (Flux)")
    print("="*50)
    settings = get_settings()
    engine = ImageEngineWithRetry(settings)
    
    # Use a test image URL (public image)
    test_char_url = "https://storage.googleapis.com/storybookai-3d5fa.firebasestorage.app/previews/6f23a0d1-1ac2-481c-8dbb-a9a9c1e3b77f/generated.png"
    
    try:
        result = await engine._run_kontext(
            image_url=test_char_url,
            prompt="3D Pixar style, a cute child exploring a magical forest with glowing mushrooms"
        )
        print(f"✅ Image generated: {result}")
        return result
    except Exception as e:
        print(f"❌ Image generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_mockup_generation():
    print("\n" + "="*50)
    print("STEP 3: Testing Mockup Generation (Gemini)")
    print("="*50)
    settings = get_settings()
    
    from app.engines.ai_mockup_engine_v3 import AIMockupEngineV3
    engine = AIMockupEngineV3(settings)
    
    # Use a test scene URL
    test_scene_url = "https://replicate.delivery/czjl/YP5z5VJdHfevhYbL5mD3l2byhw6KhGhFvG1xKPAzOz5MaZdoA/out-0.webp"
    
    try:
        result = await engine.create_mockup(
            scene_image_url=test_scene_url,
            scene_number=1,  # Open book mockup
            story_text="Es war einmal ein Kind namens Test..."
        )
        if result:
            print(f"✅ Mockup generated: {len(result)} bytes")
        else:
            print("⚠️ Mockup returned None (using fallback)")
        return result
    except Exception as e:
        print(f"❌ Mockup generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    print("🔍 DEBUGGING GENERATION FLOW")
    print("="*50)
    
    story = await test_story_generation()
    if not story:
        print("\n⛔ STOPPED: Story generation failed")
        return
    
    image = await test_image_generation()
    if not image:
        print("\n⛔ STOPPED: Image generation failed")
        return
    
    mockup = await test_mockup_generation()
    
    print("\n" + "="*50)
    print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
