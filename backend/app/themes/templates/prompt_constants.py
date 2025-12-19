# backend/app/themes/templates/prompt_constants.py
"""
Shared prompt constants for all story templates.
Quality boosters and common prompt patterns.
"""

# Global quality booster - appended to ALL image prompts
QUALITY_BOOSTER = (
    "Octane render, Unreal Engine 5 style, volumetric lighting, "
    "subsurface scattering (skin texture), cinematic composition, "
    "depth of field, 8k resolution, magical atmosphere, highly detailed textures."
)

# Lighting presets for different scenes
LIGHTING = {
    "golden_hour": "Golden hour warm backlight, sun rays, lens flare",
    "moonlight": "Soft blue moonlight, ethereal glow, starlight",
    "bioluminescent": "Bioluminescent glow, magical particles, underwater caustics",
    "dramatic": "Dramatic rim lighting, volumetric fog, cinematic shadows",
    "cozy": "Warm lamp lighting, soft ambient glow, comfortable atmosphere",
    "sunset": "Sunset warm orange and pink hues, silhouette rim light",
    "underwater": "Dappled underwater light rays, caustic patterns, blue-green ambient",
}

# Expression replacements for more vivid prompts
EXPRESSIONS = {
    "smiling": "expressive happy emotion, sparkling eyes, genuine joy",
    "standing": "dynamic pose, interacting with environment",
    "looking": "gazing with wonder, expressive eyes",
    "happy": "radiating pure happiness, bright expressive face",
}


def enhance_prompt(prompt: str, lighting_key: str = None) -> str:
    """
    Enhance a base prompt with quality booster and optional lighting.
    Also replaces generic expressions with vivid ones.
    """
    enhanced = prompt
    
    # Replace generic expressions
    for old, new in EXPRESSIONS.items():
        enhanced = enhanced.replace(old, new)
    
    # Add lighting if specified
    if lighting_key and lighting_key in LIGHTING:
        enhanced = f"{enhanced} {LIGHTING[lighting_key]}"
    
    # Always add quality booster
    enhanced = f"{enhanced} {QUALITY_BOOSTER}"
    
    return enhanced
