"""
Storybook.ai - Image Engine
Generates children's book illustrations using FLUX Kontext.

Optimized for:
- Character consistency (uses Character Asset as reference)
- Fast generation (reduced wait times)
- Pixar 3D style
"""

import asyncio
from typing import Optional, Literal, TYPE_CHECKING
from dataclasses import dataclass
import replicate

from app.config import Settings
from app.engines.story_engine import StoryOutput, Scene

if TYPE_CHECKING:
    from app.engines.character_analyzer import CharacterSheet


@dataclass
class GeneratedImage:
    """A generated image with its metadata."""
    scene_number: int
    image_url: str
    prompt_used: str


class ImageEngine:
    """
    Generates children's book illustrations using FLUX Kontext Pro.
    
    Uses Character Asset as reference for all scene variations.
    """
    
    # Flux Kontext Fast - For image-to-image with character preservation
    MODEL_KONTEXT = "prunaai/flux-kontext-fast"
    # Flux Pro fallback
    MODEL_FLUX = "black-forest-labs/flux-1.1-pro"
    
    # Theme-specific scene settings (legacy - now using theme templates)
    THEME_SCENES = {
        "space": [
            "floating in zero gravity among colorful planets and stars",
            "standing on the moon looking at Earth",
            "flying in a sleek orange spaceship through a nebula",
            "meeting a friendly green alien on a purple planet",
        ],
        "dinos": [
            "riding on the back of a friendly green brachiosaurus",
            "playing hide and seek with baby dinosaurs in a jungle",
            "discovering colorful dinosaur eggs in a volcanic cave",
            "having a picnic with a family of triceratops",
        ],
        "princess": [
            "dancing in a grand ballroom with sparkling chandeliers",
            "riding a white unicorn through an enchanted garden",
            "receiving a magical crown from a fairy godmother",
            "having tea party in a pink crystal tower",
        ],
        "pirates": [
            "standing at the helm of a pirate ship under full sail",
            "discovering a treasure chest on a tropical beach",
            "sailing through stormy seas with friendly dolphins",
            "unfurling a treasure map in the captain's cabin",
        ],
        "underwater": [
            "becoming a mermaid/merman swimming with colorful tropical fish in a coral reef",
            "exploring an underwater crystal cave with friendly dolphins",
            "playing with a family of sea turtles near a magical sunken castle",
            "finding a sparkling pearl in a giant clam with octopus friends",
        ],
        "magic": [
            "casting sparkly spells with a glowing wand in an enchanted forest",
            "having a tea party with a friendly fox and a tiny fairy",
            "befriending a baby unicorn with a glittering mane",
            "opening a magical books that creates a path of glowing flowers",
        ],
    }
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = replicate.Client(api_token=settings.replicate_api_token)
    
    async def generate_scenes_with_character_asset(
        self,
        story: StoryOutput,
        character_asset_url: str,
        child_name: str,
        theme: str,
        scene_numbers: Optional[list[int]] = None,
        features_description: Optional[str] = None,
    ) -> list[GeneratedImage]:
        """
        Generate scene variations using Character Asset as reference.
        
        Uses FLUX Kontext for each scene, keeping the character consistent.
        Uses the story's scene image_prompt for detailed, theme-specific prompts.
        """
        scenes_to_generate = scene_numbers or [1, 2, 3, 4]
        
        # Build a map of scene_number -> image_prompt from the story
        scene_prompts = {s.scene_number: s.image_prompt for s in story.scenes}
        
        print(f"🎬 Generating {len(scenes_to_generate)} scenes using FLUX Kontext Dev...")
        print(f"   Character Asset: {character_asset_url[:50]}...")
        
        images = []
        
        # Prepare tasks
        tasks = []
        for scene_num in scenes_to_generate:
            # Get the image prompt from the story template
            prompt = scene_prompts.get(scene_num, f"3D Pixar style, {child_name} on an adventure.")
            
            print(f"   🎨 queueing scene {scene_num}: {prompt[:50]}...")
            
            if scene_num == 0:
                # Use specialized high-quality cover generation for Scene 0
                tasks.append(
                    self.generate_cover_image(
                        character_asset_url=character_asset_url,
                        cover_prompt=prompt
                    )
                )
            else:
                tasks.append(
                    self._run_kontext(
                        image_url=character_asset_url, 
                        prompt=prompt
                    )
                )

        print(f"   🚀 Running {len(tasks)} scene generations SEQUENTIALLY (Rate Limit Safe)...")
        
        # Run sequentially
        for i, task_coro in enumerate(tasks):
            scene_num = scenes_to_generate[i]
            try:
                print(f"   ⏳ Starting scene {scene_num}...")
                res = await task_coro
                images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url=res,
                    prompt_used="sequential_gen",
                ))
                print(f"   ✅ Scene {scene_num} done!")
                if i < len(tasks) - 1:
                    await asyncio.sleep(2)
            except Exception as e:
                 print(f"   ❌ Scene {scene_num} failed: {e}")
                 images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url="",
                    prompt_used=f"Failed: {e}",
                ))

        # results no longer needed
        results = []
            
        # Process results
        for i, res in enumerate(results):
            scene_num = scenes_to_generate[i]
            if isinstance(res, Exception):
                print(f"   ❌ Scene {scene_num} failed: {res}")
                images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url="",
                    prompt_used=f"Failed: {res}",
                ))
            elif res:
                images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url=res,
                    prompt_used="parallel_gen",
                ))
                print(f"   ✅ Scene {scene_num} done!")
        
        return sorted(images, key=lambda x: x.scene_number)
    
    async def _run_kontext(self, image_url: str, prompt: str) -> str:
        """Run FLUX for image-to-image generation with character preservation."""
        loop = asyncio.get_event_loop()
        
        # Validate URL before calling API
        if not image_url or not image_url.startswith("http"):
            print(f"   ❌ Invalid image URL for Flux: {image_url}")
            raise ValueError(f"Invalid image URL: {image_url}")
        
        def run_sync():
            print(f"   📸 Calling FLUX Kontext Fast...")
            print(f"   📝 Prompt: {prompt[:100]}...")
            print(f"   🖼️ Image URL: {image_url[:80]}...")
            
            try:
                output = self.client.run(
                    self.MODEL_KONTEXT,
                    input={
                        "prompt": prompt,
                        "img_cond_path": image_url,  # Reference character image
                        "guidance": 2.5,
                        "speed_mode": "Real Time",
                    }
                )
                result_url = self._extract_url(output)
                print(f"   ✅ Flux Success: {result_url[:50]}...")
                return result_url
            except Exception as e:
                print(f"   ❌ Flux API Error: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        return await loop.run_in_executor(None, run_sync)
    
    # === COVER-SPECIFIC GENERATION ===
    # Quality string for cover images
    COVER_QUALITY_BOOST = (
        "Detailed texture, 8k, sharp focus on eyes, masterpiece, "
        "professional photography lighting, cinematic portrait."
    )
    
    async def generate_cover_image(
        self,
        character_asset_url: str,
        cover_prompt: str,
    ) -> str:
        """
        Generate cover image with maximum character consistency.
        
        Uses lower guidance and higher quality settings to preserve
        facial features from the character asset.
        """
        # Strict validation - cover MUST have character reference
        if not character_asset_url or not character_asset_url.startswith("http"):
            raise ValueError(
                "Character asset URL is REQUIRED for cover generation! "
                f"Got: {character_asset_url}"
            )
        
        # Inject quality boost and background replacement instruction
        bg_instruction = "CRITICAL: Replace the clean white background from the reference image with the environment described in the prompt. "
        enhanced_prompt = f"{bg_instruction} {cover_prompt} {self.COVER_QUALITY_BOOST}"
        
        print(f"🎨 Generating COVER image...")
        print(f"   📝 Enhanced Prompt: {enhanced_prompt[:100]}...")
        print(f"   🖼️ Character Asset: {character_asset_url[:80]}...")
        
        loop = asyncio.get_event_loop()
        
        def run_sync():
            try:
                output = self.client.run(
                    self.MODEL_KONTEXT,
                    input={
                        "prompt": enhanced_prompt,
                        "img_cond_path": character_asset_url,
                        "guidance": 3.5,  # Increased to allow background replacement
                        "speed_mode": "Real Time",
                    }
                )
                result_url = self._extract_url(output)
                print(f"   ✅ Cover generated: {result_url[:50]}...")
                return result_url
            except Exception as e:
                print(f"   ❌ Cover generation failed: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        return await loop.run_in_executor(None, run_sync)
    
    async def generate_scene_images(
        self,
        story: StoryOutput,
        reference_image_url: Optional[str] = None,
        style: Literal["watercolor", "pixar_3d", "pencil", "cartoon", "storybook"] = "watercolor",
        character_description: str = "a cheerful child",
        scene_numbers: Optional[list[int]] = None,
        gender: str = "neutral",
        theme: str = "adventure",
    ) -> list[GeneratedImage]:
        """Fallback: Generate scenes without Character Asset."""
        scenes_to_generate = scene_numbers or [1, 2, 3, 4]
        theme_scenes = self.THEME_SCENES.get(theme, [])
        
        print(f"🎬 Generating {len(scenes_to_generate)} scenes (no character asset)...")
        
        images = []
        
        for i, scene_num in enumerate(scenes_to_generate):
            scene_idx = (scene_num - 1) % max(len(theme_scenes), 1)
            scene_action = theme_scenes[scene_idx] if theme_scenes else "on an adventure"
            
            prompt = (
                f"3D Pixar Disney style, {character_description}, "
                f"{scene_action}, vibrant colors, full body, "
                f"children's storybook illustration, cute cartoon."
            )
            
            print(f"\n🎨 Scene {scene_num}...")
            
            try:
                image_url = await self._run_flux(prompt)
                images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url=image_url,
                    prompt_used=prompt,
                ))
                print(f"   ✅ Done!")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                images.append(GeneratedImage(
                    scene_number=scene_num,
                    image_url="",
                    prompt_used=f"Failed: {e}",
                ))
            
            if i < len(scenes_to_generate) - 1:
                await asyncio.sleep(5)
        
        return sorted(images, key=lambda x: x.scene_number)
    
    async def _run_flux(self, prompt: str) -> str:
        """Run Flux Pro for text-to-image."""
        loop = asyncio.get_event_loop()
        
        def run_sync():
            output = self.client.run(
                self.MODEL_FLUX,
                input={
                    "prompt": prompt,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "output_quality": 90,
                    "safety_tolerance": 2,
                }
            )
            return self._extract_url(output)
        
        return await loop.run_in_executor(None, run_sync)
    
    def _extract_url(self, output) -> str:
        """Extract URL from Replicate output."""
        if isinstance(output, str):
            return output
        elif hasattr(output, 'url'):
            return output.url
        elif isinstance(output, list) and len(output) > 0:
            item = output[0]
            return str(item.url if hasattr(item, 'url') else item)
        else:
            result = list(output)
            if result:
                item = result[0]
                return str(item.url if hasattr(item, 'url') else item)
            raise ValueError(f"Unexpected output: {type(output)}")


class ImageEngineWithRetry(ImageEngine):
    """Extended ImageEngine with retry logic."""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 10
    
    async def _run_kontext(self, image_url: str, prompt: str) -> str:
        """Run with retry logic."""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                return await super()._run_kontext(image_url, prompt)
            except Exception as e:
                last_error = e
                error_str = str(e)
                print(f"   ⚠️ Attempt {attempt + 1} failed: {error_str[:50]}")
                
                if "429" in error_str:
                    wait_time = self.RETRY_DELAY * (attempt + 2)
                    print(f"   ⏳ Rate limited, waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                elif attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY)
        
        raise last_error or Exception("Unknown error after retries")
    
    async def _run_flux(self, prompt: str) -> str:
        """Run with retry logic."""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                return await super()._run_flux(prompt)
            except Exception as e:
                last_error = e
                print(f"   ⚠️ Attempt {attempt + 1} failed")
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY)
        
        raise last_error or Exception("Unknown error after retries")
