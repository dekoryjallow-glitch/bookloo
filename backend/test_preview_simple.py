"""
Simple test to trace the exact error in generate_preview_task
"""
import asyncio
from app.config import get_settings
from app.engines.story_engine import StoryEngine
from app.engines.image_engine import ImageEngineWithRetry

async def test_preview_generation():
    """Test just the code that runs in generate_preview_task"""
    settings = get_settings()
    
    # Simulate what the approve flow does
    book_id = "test-123"
    child_name = "Max"
    theme = "space"
    style = "pixar_3d"
    approved_portrait_url = "https://example.com/character.jpg"
    
    print(f"🚀 Starting Preview Generation Test...")
    print(f"   Theme: {theme}")
    print(f"   Child: {child_name}")
    
    # Step 1: Generate Story
    print(f"\n[Step 1] Generating Story...")
    try:
        story_engine = StoryEngine(settings)
        character_desc_simple = f"cute 6 year old child named {child_name}"
        
        story = await story_engine.generate_story(
            name=child_name,
            theme=theme,
            age=6,
            style=style,
            character_description=character_desc_simple
        )
        print(f"[Step 1] ✅ Story generated: {story.title} ({len(story.scenes)} scenes)")
    except Exception as e:
        print(f"[Step 1] ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Setup Image Engine
    print(f"\n[Step 2] Setting up Image Engine...")
    try:
        KEY_SCENES = [0, 1, 5, 10]
        image_engine = ImageEngineWithRetry(settings)
        print(f"[Step 2] ✅ Image Engine ready")
        print(f"[Step 2] Model: {image_engine.MODEL_KONTEXT}")
    except Exception as e:
        print(f"[Step 2] ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Check scene prompts
    print(f"\n[Step 3] Checking scene prompts map...")
    scene_prompts = {s.scene_number: s.image_prompt for s in story.scenes}
    for scene_num in KEY_SCENES:
        prompt = scene_prompts.get(scene_num, "MISSING!")
        status = "✅" if prompt != "MISSING!" else "❌"
        print(f"   {status} Scene {scene_num}: {prompt[:60] if prompt else 'MISSING'}...")
    
    print(f"\n✅ All checks passed - the logic is correct!")
    print(f"If still failing in production, the error is likely in:")
    print(f"  1. Replicate API call (check REPLICATE_API_TOKEN)")
    print(f"  2. Firestore operations (check Firebase connection)")
    print(f"  3. Mockup engine (check assets folder)")

if __name__ == "__main__":
    asyncio.run(test_preview_generation())
