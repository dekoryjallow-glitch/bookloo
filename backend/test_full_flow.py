"""
Test script to debug the full generation flow.
"""
import asyncio
from app.config import get_settings
from app.engines.story_engine import StoryEngine
from app.engines.image_engine import ImageEngineWithRetry

async def test_full_flow():
    settings = get_settings()
    
    # 1. Test Story Generation
    print("=" * 50)
    print("1. Testing Story Generation...")
    story_engine = StoryEngine(settings)
    
    try:
        story = await story_engine.generate_story(
            name="Max",
            theme="space",
            age=6,
            style="pixar_3d",
            character_description="cute child"
        )
        print(f"   ✅ Story Generated: {story.title}")
        print(f"   Scenes: {len(story.scenes)}")
        for s in story.scenes[:3]:
            print(f"      Scene {s.scene_number}: {s.image_prompt[:60]}...")
    except Exception as e:
        print(f"   ❌ Story Generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 2. Test Image Engine (without actually calling Replicate)
    print("\n" + "=" * 50)
    print("2. Testing Image Engine Setup...")
    
    try:
        image_engine = ImageEngineWithRetry(settings)
        print(f"   ✅ Image Engine initialized")
        print(f"   Model: {image_engine.MODEL_KONTEXT}")
        
        # Build scene prompt map
        scene_prompts = {s.scene_number: s.image_prompt for s in story.scenes}
        KEY_SCENES = [0, 1, 5, 10]
        
        print(f"\n   Key Scenes to generate: {KEY_SCENES}")
        for scene_num in KEY_SCENES:
            prompt = scene_prompts.get(scene_num, "MISSING")
            print(f"      Scene {scene_num}: {prompt[:60]}...")
            
    except Exception as e:
        print(f"   ❌ Image Engine FAILED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 50)
    print("✅ All checks passed! The flow should work.")
    print("If still failing, check Replicate API token and network.")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
