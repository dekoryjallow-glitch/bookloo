"""
Storybook.ai - Character Analyzer
Uses GPT-4o Vision to extract detailed character features from an uploaded photo.
These features are then used to maintain consistency across all generated images.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

from app.config import Settings


class CharacterTraits(BaseModel):
    """
    Structured character features for strict consistency in Flux generation.
    """
    gender: Literal['boy', 'girl', 'child']
    age_prompt: str = Field(description="Visual age description, e.g. '5-year-old toddler'")
    hair_prompt: str = Field(description="Precise hair description, e.g. 'short curly blonde hair'")
    eye_prompt: str = Field(description="Precise eye description, e.g. 'bright green eyes'")
    skin_tone: str = Field(description="Visual skin tone description. CRITICAL: Do NOT whitewash. Identify the actual skin tone (e.g., 'dark brown', 'black', 'fair', 'olive'). Ignore bright lighting.")
    ethnicity: str = Field(description="Visual ethnicity description, e.g. 'Black', 'Asian', 'Caucasian', 'Hispanic'")
    clothing: str = Field(description="Simple clothing description, e.g. 'red hoodie'")
    distinctive_features: str = Field(description="Glasses, freckles, dimples - or empty string if none")
    consistency_string: str = Field(description="A comma-separated summary. MUST include: Age, Gender, Ethnicity, Skin Tone, Hair, Eyes.")


# System prompt for GPT-4o Vision analysis
FEATURE_EXTRACTION_PROMPT = """
Du bist ein technischer Bild-Analyst für Stable Diffusion Modelle.
Deine wichtigste Aufgabe ist die **korrekte Erkennung von Hautfarbe und Ethnie**.
Vermeide "Whitewashing". Wenn eine Person dunkelhäutig ist, beschreibe sie als "dark skin", "black skin" oder "dark brown skin".
Ignoriere helle Studiobeleuchtung, die die Haut heller wirken lässt. Suche nach den dunkelsten Hautpartien im Schatten.

Dein Ziel ist es, ein JSON-Objekt zu erstellen:
- gender: 'boy', 'girl' oder 'child'
- age_prompt: Visuelle Altersbeschreibung (z.B. "5-year-old toddler")
- hair_prompt: Präzise Haarbeschreibung (z.B. "short curly black hair")
- eye_prompt: Präzise Augenbeschreibung (z.B. "dark brown eyes")
- skin_tone: Exakter Hautton. Wähle aus: "pale", "fair", "medium", "olive", "light brown", "brown", "dark brown", "black", "very dark".
- ethnicity: Ethnie (z.B. "Black", "Afro-American", "Caucasian", "Asian", "Hispanic")
- clothing: Einfache Kleidung (z.B. "red hoodie")
- distinctive_features: Besondere Merkmale (z.B. "freckles", "glasses") oder leerer String
- consistency_string: Fasse alle visuellen Merkmale zusammen. WICHTIG: Nenne Ethnie und Hautfarbe ZUERST (z.B. "Black child, dark skin, curly hair...").

WICHTIG: Wenn das Bild unscharf oder das Gesicht verdeckt ist, beschreibe so gut es geht.
"""


class CharacterAnalyzer:
    """
    Analyzes uploaded child photos using GPT-4o Vision with Structured Outputs.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None
    
    async def analyze_photo(self, photo_url: str) -> CharacterTraits:
        """
        Analyze a child's photo and extract visual features using Pydantic validation.
        """
        print(f"🔍 Analyzing photo for character features (Structured)...")
        print(f"📷 Photo URL: {photo_url[:60]}...")
        
        try:
            # Lazy init client
            if not self.client:
                self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": FEATURE_EXTRACTION_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": photo_url,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.0, # Zero temp for strict JSON
                response_format={"type": "json_object"},
            )
            
            result_text = response.choices[0].message.content
            print(f"📝 Raw analysis result: {result_text[:200]}...")
            
            # Parse and Validate with Pydantic
            traits = CharacterTraits.model_validate_json(result_text)
            
            print(f"✅ Character analysis complete!")
            print(f"   Consistency String: {traits.consistency_string}")
            
            return traits
            
        except Exception as e:
            print(f"❌ Error analyzing photo: {e}")
            # Return fallback features
            return self._get_default_features()
    
    def _get_default_features(self) -> CharacterTraits:
        """Return default features when analysis fails."""
        return CharacterTraits(
            gender="child",
            age_prompt="5-year-old child",
            hair_prompt="short brown hair",
            eye_prompt="brown eyes",
            skin_tone="medium skin tone",
            ethnicity="diverse",
            clothing="colorful t-shirt",
            distinctive_features="friendly smile",
            consistency_string="5-year-old child, short brown hair, brown eyes, medium skin tone, colorful t-shirt"
        )


# Legacy alias for compatibility if needed
CharacterFeatures = CharacterTraits


class CharacterSheet(BaseModel):
    """
    Complete character data for consistent image generation.
    Combines the original photo URL with extracted features.
    """
    
    # Original photo
    original_photo_url: str
    
    # Extracted features (now Pydantic model)
    features: CharacterTraits
    
    # Child info from user input
    child_name: str
    child_age: int
    
    # Style info
    style: str  # watercolor, pixar_3d, cartoon, storybook
    theme: str  # space, magic, adventure, princess
    
    def get_scene_prompt(self, scene_action: str, scene_environment: str) -> str:
        """
        Build a complete scene prompt with embedded character features.
        """
        # Style prefixes (same as before)
        style_prefixes = {
            "watercolor": "professional children's book illustration, whimsical watercolor painting style, soft pastel colors, dreamy magical atmosphere, gentle brush strokes, artistic",
            "pixar_3d": "professional 3D animated children's book illustration, Pixar Disney style, vibrant saturated colors, expressive cartoon character, soft cinematic lighting, cute adorable, 3D render",
            "pencil": "professional children's book illustration, hand-drawn colored pencil style, warm crayon colors, textured paper look, nostalgic childhood drawing feel, artistic sketchy lines",
            "cartoon": "professional children's book illustration, colorful 2D cartoon style, bold clean outlines, bright cheerful colors, whimsical fun",
            "storybook": "professional children's book illustration, classic fairytale storybook style, warm golden colors, nostalgic magical feel",
        }
        
        theme_outfits = {
            "space": "wearing a bright colorful child-sized astronaut spacesuit with fun patches and a clear helmet visor, floating in space with stars",
            "dinos": "wearing safari explorer clothes with a pith helmet and binoculars around neck, surrounded by friendly dinosaurs",
            "princess": "wearing a beautiful flowing pink princess ball gown with a sparkling tiara crown, in a magical castle",
            "pirates": "wearing a red and white striped pirate shirt, bandana headband, and a fun eyepatch, on a treasure ship",
            "underwater": "wearing a bright blue diving suit with an orange snorkel and swimming goggles, swimming with colorful fish",
            "magic": "wearing a sparkly purple wizard robe with golden stars and a pointy wizard hat, in an enchanted forest",
            "custom": "wearing colorful adventure clothes suitable for the story theme",
            "adventure": "wearing khaki explorer shorts, a safari vest with pockets, and a small adventure backpack",
            "dinosaurs": "wearing safari explorer clothes with a pith helmet and binoculars around neck",
            "fairy": "wearing a sparkly pastel fairy dress with delicate translucent butterfly wings",
        }
        
        # Age-appropriate body descriptions
        age = self.child_age
        if age <= 4:
            body_desc = "toddler body proportions, chubby cheeks, short limbs, big head relative to body"
        elif age <= 6:
            body_desc = "young child body proportions, slightly chubby, small and cute"
        elif age <= 9:
            body_desc = "elementary school age child body, active playful posture"
        else:
            body_desc = "pre-teen child body proportions, growing and confident"
        
        style_prefix = style_prefixes.get(self.style, style_prefixes["pixar_3d"])
        outfit = theme_outfits.get(self.theme, "wearing colorful adventure clothes")
        
        # USE CONSISTENCY STRING FROM TRAITS
        trait_string = self.features.consistency_string
        
        # Build the complete prompt with explicit instructions
        prompt = (
            f"{style_prefix}. "
            f"Character: {trait_string}. "
            f"Body type: {body_desc}. "
            f"Scene: The child is {scene_action}. {scene_environment}. {outfit}. "
            f"IMPORTANT: Preserve exact facial features: {self.features.eye_prompt}, {self.features.hair_prompt}. "
            f"Single character, full body visible, center composition, masterpiece, 8k."
        )
        
        return prompt
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "original_photo_url": self.original_photo_url,
            "features": self.features.model_dump(), # Pydantic method
            "child_name": self.child_name,
            "child_age": self.child_age,
            "style": self.style,
            "theme": self.theme,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CharacterSheet":
        """Create from dictionary."""
        features = CharacterTraits(**data["features"])
        return cls(
            original_photo_url=data["original_photo_url"],
            features=features,
            child_name=data["child_name"],
            child_age=data["child_age"],
            style=data["style"],
            theme=data["theme"],
        )
