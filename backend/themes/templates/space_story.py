# backend/themes/templates/space_story.py
"""
Space Adventure Theme for Storybook.ai
Uses Flux Kontext for scene generation with character preservation.
"""

SPACE_TEMPLATE = {
    "id": "space_adventure",
    "title_pattern": "{name} greift nach den Sternen",
    "default_outfit_prompt": "wearing a sparkly orange astronaut suit with a helmet under arm",
    # Flux Kontext uses the reference image directly,
    # so we describe the scene and action, not detailed character features.
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "{name} greift nach den Sternen",
            "image_prompt": "A cinematic movie poster shot of the character from the reference image floating in deep space. The character is smiling confidently. Background is a magical galaxy with purple nebulas and bright stars. High resolution, 3D Pixar style masterpiece."
        },
        # SCENE 1: BEDROOM (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "In einem Zimmer, gemütlich und klein, träumt {name} davon, im Weltall zu sein. 'Die Sterne funkeln so hell und klar, ich wünschte', sagt {name}, 'ich wäre schon da!'",
            "image_prompt": "Wide shot of the character from the reference image sitting in a cozy children's bedroom at night. The character is looking through a telescope out the window at the starry sky. Toys on the floor, warm lamp lighting inside, blue moonlight outside. 3D Pixar animation style."
        },
        # SCENE 2: LAUNCH
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "Plötzlich wackelt das Bett und es blitzt, das Zimmer hat sich in ein Raumschiff geschnitzt! Der Countdown läuft, das Herz klopft schnell, der Antrieb leuchtet unglaublich hell.",
            "image_prompt": "Dynamic low angle shot inside a high-tech spaceship cockpit. The character from the reference image is sitting in the pilot seat, pressing glowing buttons. Stars are streaking by outside the window like warp speed. Exciting atmosphere, sparks, 3D Pixar style."
        },
        # SCENE 3: ZERO GRAVITY
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Schwerelos schwebt nun alles umher, selbst der Teddybär ist gar nicht mehr schwer. {name} lacht und dreht sich im Kreis, das Weltall ist riesig, so schwarz und so weiß.",
            "image_prompt": "The character from the reference image is floating in zero gravity inside a spaceship corridor. Happy expression, arms spread out. Floating objects like a pencil and a cup around them. View of planet Earth through the window. 3D Pixar style."
        },
        # SCENE 4: ALIEN PLANET LANDING
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Eine Landung auf dem Planeten Kunterbunt, hier ist nichts eckig, alles ist rund. Rote Bäume und lila Gras, das macht {name} riesigen Spaß!",
            "image_prompt": "Wide landscape shot of an alien planet surface with purple grass and red round bulbous trees. The character from the reference image is stepping out of the spaceship ramp, looking amazed at the horizon. Colorful nebula in the sky. 3D Pixar style."
        },
        # SCENE 5: MEETING THE ALIEN
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Wer guckt denn da hinterm Felsen hervor? Ein kleines Alien mit nur einem Ohr! Es winkt ganz freundlich und piepst ganz froh: 'Willkommen, mein Freund, im Weltall-Büro!'",
            "image_prompt": "Eye-level shot of the character from the reference image kneeling down to look at a cute small green alien with big eyes hiding behind a glowing crystal rock. Friendly interaction, bioluminescent plants in background. 3D Pixar style."
        },
        # SCENE 6: PLAYING
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Sie spielen Fangen, sie hüpfen so hoch, über Krater und über das schwarze Loch. Mit einem Sprung geht es meterweit, was für eine wunderbare Zeit.",
            "image_prompt": "Action shot of the character from the reference image jumping high in low gravity over a moon crater alongside a cute green alien. Laughing, dynamic pose, stardust sparkling around them, two moons in the sky. 3D Pixar style."
        },
        # SCENE 7: THE GIFT
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Doch die Uhr am Armaturenbrett blinkt, die Erde ruft, der Abschied winkt. Das Alien schenkt noch einen leuchtenden Stein, 'Der soll immer dein Begleiter sein.'",
            "image_prompt": "Emotional close-up. A cute alien handing a glowing blue crystal gem to the character from the reference image. The character looks grateful, holding the crystal with both hands. Spaceship with open door in background. 3D Pixar style."
        },
        # SCENE 8: FLYING BACK
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Zurück im Schiff, der Turbo geht an, so schnell wie nur eine Rakete kann. Vorbei am Mond und am Satellit, {name} nimmt viele Erinnerungen mit.",
            "image_prompt": "View from behind the character from the reference image, looking out the front window of the spaceship towards approaching planet Earth (blue marble). Fast motion blur stars, cockpit lights reflecting on the glass. 3D Pixar style."
        },
        # SCENE 9: BACK IN BEDROOM
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "Die Landung ist sanft, das Zimmer ist da, war das ein Traum oder war es wahr?",
            "image_prompt": "Bedroom setting again, morning sunlight coming through window. The character from the reference image is sitting on the edge of the bed, rubbing eyes, looking confused but happy. 3D Pixar style."
        },
        # SCENE 10: THE PROOF
        {
            "id": 10,
            "type": "story",
            "is_preview": True,
            "text": "Doch in der Hand, da leuchtet es hell, der Stein vom Alien, ganz aktuell. {name} lächelt und schläft tief ein, Abenteuer können so wunderbar sein.",
            "image_prompt": "Extreme close-up on the hand of the character from the reference image opening to reveal the glowing blue alien crystal from scene 7. Soft magical glow illuminating the character's face while lying in bed. Peaceful atmosphere, 3D Pixar style."
        }
    ]
}
