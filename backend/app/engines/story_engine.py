"""
Storybook.ai - Story Engine
Generates personalized children's stories with exactly 10 scenes (20 pages).
Uses OpenAI GPT-4o or Claude API with strict prompting for consistent JSON output.

NEW: Also supports loading predefined story templates for faster generation.
"""

import json
from typing import Optional, Literal
from dataclasses import dataclass
from openai import AsyncOpenAI

from app.config import Settings
from app.models.book import BookPage, BookTheme
from app.engines.story_templates import get_story_template, personalize_template, SceneTemplate


@dataclass
class Scene:
    """A single scene in the story (covers 2 pages)."""
    scene_number: int
    narration_text: str
    image_prompt: str


@dataclass
class StoryOutput:
    """Complete story output with 10 scenes."""
    title: str
    scenes: list[Scene]


# Strict system prompt for consistent output
SYSTEM_PROMPT = """Du bist ein Kinderbuchautor. Erstelle eine Geschichte mit genau 13 Szenen (für 26 Inhaltsseiten).

Für jede Szene brauche ich:
1. Den Vorlesetext (kindgerecht, reimend optional) - max 3-4 Sätze
2. Einen präzisen Bild-Prompt für die KI, der die Szene beschreibt, aber IMMER mit dem Platzhalter [CHARACTER] beginnt.

WICHTIGE REGELN:
- Genau 13 Szenen, nicht mehr, nicht weniger
- Jeder image_prompt MUSS mit "[CHARACTER]" beginnen
- Die Geschichte folgt der klassischen Heldenreise
- Kindgerechte Sprache für das angegebene Alter
- Positive, ermutigende Botschaft

Antworte NUR mit validem JSON im folgenden Format:
{
  "title": "Der Titel der Geschichte",
  "scenes": [
    {
      "scene_number": 1,
      "narration_text": "Der Vorlesetext für diese Szene...",
      "image_prompt": "[CHARACTER] steht in einem gemütlichen Kinderzimmer..."
    },
    ...
  ]
}"""


# Story arc structure based on Hero's Journey
STORY_ARC = """
Szene 1-2: Normale Welt & Ruf zum Abenteuer
Szene 3: Zögern/Zweifel
Szene 4: Mentor/Helfer erscheint
Szene 5-6: Aufbruch ins Abenteuer, erste Herausforderungen
Szene 7-8: Größte Prüfung, Tiefpunkt und Durchbruch
Szene 9: Sieg/Belohnung
Szene 10: Rückkehr & Happy End
"""


class StoryEngine:
    """Generates personalized children's stories using OpenAI GPT-4o."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        # OpenAI Client is initialized lazily if needed
        self.client = None
    
    async def generate_story(
        self,
        name: str,
        theme: str,
        age: int = 5,
        style: Literal["watercolor", "pixar_3d"] = "watercolor",
        character_description: str = "", 
    ) -> StoryOutput:
        """
        Generate a complete story using templates (V2).
        
        Args:
            name: Name of the child
            theme: Theme ID
            age: Child's age
            style: Illustration style
            character_description: Consistency string for image prompts
        """
        # NEW: use V2 Template System for supported themes
        if theme == "space":
            from app.themes.templates.space_story import SPACE_TEMPLATE
            from app.themes.compiler import compile_story
            
            print(f"🚀 Using V2 Template for theme: {theme}")
            compiled = compile_story(SPACE_TEMPLATE, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"], # Keep 0 for cover
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )
        
        # Dino Explorer Theme (V2)
        if theme in ["dino", "dinos", "dinosaur", "dino_explorer"]:
            from app.themes.templates.dino_story import DINO_THEME
            from app.themes.compiler import compile_story
            
            print(f"🦕 Using V2 Template for theme: {theme}")
            compiled = compile_story(DINO_THEME, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"],
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )

        # Pirate Adventure Theme (V2)
        if theme in ["pirate", "pirates", "pirate_adventure"]:
            from app.themes.templates.pirate_story import PIRATE_THEME
            from app.themes.compiler import compile_story
            
            print(f"🏴‍☠️ Using V2 Template for theme: {theme}")
            compiled = compile_story(PIRATE_THEME, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"],
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )

        # Princess Kingdom Theme (V2)
        if theme in ["princess", "princess_kingdom", "magic_kingdom"]:
            from app.themes.templates.princess_story import PRINCESS_THEME
            from app.themes.compiler import compile_story
            
            print(f"👑 Using V2 Template for theme: {theme}")
            compiled = compile_story(PRINCESS_THEME, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"],
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )

        # Magic Forest Theme (V2) - also handles "magic" and "fantasy" aliases
        if theme in ["forest", "magic_forest", "enchanted_forest", "magic", "fantasy"]:
            from app.themes.templates.forest_story import FOREST_THEME
            from app.themes.compiler import compile_story
            
            print(f"🌲 Using V2 Template for theme: {theme}")
            compiled = compile_story(FOREST_THEME, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"],
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )

        # Underwater Magic Theme (V2)
        if theme in ["underwater", "underwater_magic", "ocean_adventure"]:
            from app.themes.templates.underwater_story import UNDERWATER_THEME
            from app.themes.compiler import compile_story
            
            print(f"🌊 Using V2 Template for theme: {theme}")
            compiled = compile_story(UNDERWATER_THEME, name, character_description)
            
            scenes = []
            for s in compiled["scenes"]:
                scenes.append(Scene(
                    scene_number=s["id"],
                    narration_text=s["text"],
                    image_prompt=s["image_prompt"]
                ))
                
            return StoryOutput(
                title=compiled["title_pattern"],
                scenes=scenes
            )

        # Fallback for other themes (using old template system for now)
        return self.get_template_story(name, theme)
    
    def _get_language_guide(self, age: int) -> str:
        """Get age-appropriate language guidance."""
        if age <= 3:
            return "Sehr einfache Sätze, max 5-8 Wörter, viele Wiederholungen"
        elif age <= 5:
            return "Kurze Sätze, einfache Wörter, Reime sind toll"
        elif age <= 7:
            return "Etwas längere Sätze, einfache Adjektive, spannende Handlung"
        else:
            return "Komplexere Sätze erlaubt, reicherer Wortschatz, mehr Details"
    
    def get_template_story(self, name: str, theme: str) -> StoryOutput:
        """
        Get a predefined story template (much faster than GPT-4 generation).
        
        Args:
            name: Name of the child protagonist
            theme: Story theme (space, dinos, pirates, princess, magic, underwater)
        
        Returns:
            StoryOutput with title and scenes from template
        """
        print(f"📖 Loading story template for theme: {theme}")
        
        # Get and personalize template
        template = get_story_template(theme)
        personalized = personalize_template(template, name)
        
        # Convert template scenes to StoryOutput scenes
        scenes = []
        for scene_template in personalized.scenes:
            scenes.append(Scene(
                scene_number=scene_template.scene_number,
                narration_text=scene_template.text,
                image_prompt=scene_template.visual_prompt,
            ))
        
        print(f"   ✅ Loaded {len(scenes)} scenes for '{personalized.title}'")
        
        return StoryOutput(
            title=personalized.title,
            scenes=scenes,
        )
    
    def story_to_pages(self, story: StoryOutput) -> list[BookPage]:
        """
        Convert StoryOutput to list of BookPage objects.
        Each scene becomes 2 pages (left: image, right: text).
        
        Returns:
            List of 20 BookPage objects
        """
        pages = []
        
        for scene in story.scenes:
            # Page 1 of scene: primarily for image
            page_num_left = (scene.scene_number - 1) * 2 + 1
            # Page 2 of scene: primarily for text
            page_num_right = page_num_left + 1
            
            # Left page (image-focused)
            pages.append(BookPage(
                page_number=page_num_left,
                text="",  # Image page, text on right
                image_prompt=scene.image_prompt,
            ))
            
            # Right page (text-focused)
            pages.append(BookPage(
                page_number=page_num_right,
                text=scene.narration_text,
                image_prompt=None,  # No image on text page
            ))
        
        return pages
    
    def story_to_compact_pages(self, story: StoryOutput) -> list[BookPage]:
        """
        Convert StoryOutput to list of BookPage objects.
        Each scene becomes 2 pages with image AND text on each.
        
        Note: scene_number can start at 0 (for cover) or 1.
        """
        pages = []
        
        for i, scene in enumerate(story.scenes):
            # Use index instead of scene_number to avoid negative page numbers
            page_num_1 = i * 2 + 1
            page_num_2 = page_num_1 + 1
            
            # Split narration roughly in half
            words = scene.narration_text.split()
            mid = len(words) // 2
            text_part1 = " ".join(words[:mid]) if mid > 0 else scene.narration_text
            text_part2 = " ".join(words[mid:]) if mid > 0 else ""
            
            # Both pages get part of the scene
            pages.append(BookPage(
                page_number=page_num_1,
                text=text_part1,
                image_prompt=scene.image_prompt,
            ))
            
            pages.append(BookPage(
                page_number=page_num_2,
                text=text_part2 if text_part2 else text_part1,
                image_prompt=scene.image_prompt + " (continued)",
            ))
        
        return pages
