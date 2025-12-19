"""
Storybook.ai - Story Compiler
Replaces placeholders in story templates with personalized data.
"""

from typing import Dict, Any, Optional

def compile_story(template: Dict[str, Any], child_name: str, character_desc: str) -> Dict[str, Any]:
    """
    Compiles a story template by substituting placeholders.
    
    Args:
        template: The raw template dictionary (e.g. SPACE_TEMPLATE).
        child_name: The name of the child (replacing {name}).
        character_desc: The consistency string (replacing {character_desc}).
        
    Returns:
        A new dictionary with strings replaced.
    """
    # Deep copy to avoid modifying the global template
    import copy
    compiled = copy.deepcopy(template)
    
    # 1. Compile Global Fields
    compiled["title_pattern"] = compiled["title_pattern"].replace("{name}", child_name)
    
    default_outfit = compiled.get("default_outfit_prompt", "")
    
    # 2. Compile Scenes
    for scene in compiled["scenes"]:
        # Text Replacement (Name only)
        if "text" in scene:
            scene["text"] = scene["text"].replace("{name}", child_name)
            
        # Image Prompt Replacement
        if "image_prompt" in scene:
            prompt = scene["image_prompt"]
            
            # {name}
            prompt = prompt.replace("{name}", child_name)
            
            # {character_desc}
            prompt = prompt.replace("{character_desc}", character_desc)
            
            # {outfit}
            # Logic: If {outfit} is in prompt, replace with default_outfit.
            # If NOT in prompt, do nothing (keep pajamas/default implied by context).
            if "{outfit}" in prompt:
                prompt = prompt.replace("{outfit}", default_outfit)
            
            scene["image_prompt"] = prompt
            
    return compiled
