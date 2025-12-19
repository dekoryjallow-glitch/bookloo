# backend/app/themes/templates/space_story.py
"""
Space Adventure Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.

NOTE: Image prompts describe "the character from the reference image" because
Flux Kontext uses the input_image directly for character preservation.
"""
from .prompt_constants import QUALITY_BOOSTER

SPACE_TEMPLATE = {
    "theme_id": "space",
    "title_pattern": "{name} greift nach den Sternen",
    "default_outfit_prompt": "",  # Not used with Flux Kontext
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "{name} greift nach den Sternen",
            "image_prompt": f"Epic cinematic close-up portrait of the character from the reference image, who is a {{character_desc}}, floating in deep space. Expressive wonder in sparkling eyes. Background: detailed purple galaxy nebula with swirling cosmic dust. Rim lighting on the suit, volumetric star glow. {QUALITY_BOOSTER}"
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
            "text": "Das Alien schenkt noch einen leuchtenden Stein, 'Der soll immer dein Begleiter sein.' Es funkelt wie Gold und strahlt wie das Licht, so ein schönes Geschenk vergisst {name} nicht.",
            "image_prompt": "Emotional close-up. A cute alien handing a glowing blue crystal gem to the character from the reference image. The character looks grateful, holding the crystal with both hands. Spaceship with open door in background. 3D Pixar style."
        },
        # SCENE 8: STAR SHOWER (NEW)
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Doch was ist das dort? Ein Regen aus Glas? Nein, Sternenstaub kitzelt {name} an der Nas! In allen Farben leuchtet die Nacht, {name} hat vor Freude ganz laut gelacht.",
            "image_prompt": "Magical scene in space. The character from the reference image is surrounded by a shower of colorful, glowing stardust particles. The alien is cheering next to them. Vibrant pink, blue and gold sparkles everywhere. 3D Pixar style."
        },
        # SCENE 9: COMET RIDE (NEW)
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "Ein Komet flitzt vorbei, so schnell wie der Wind, 'Halt dich fest!', ruft das Alien ganz geschwind. Sie reiten den Schweif, ein Ritt durch das All, mit einem gewaltigen Sternen-Knall!",
            "image_prompt": "Dynamic action shot. The character from the reference image and the alien are sitting on a glowing, fast-moving comet with a long sparkling tail. Streaking lights, intense speed, joyful expressions. 3D Pixar style."
        },
        # SCENE 10: FLYING BACK
        {
            "id": 10,
            "type": "story",
            "is_preview": False,
            "text": "Zurück im Schiff, der Turbo geht an, so schnell wie nur eine Rakete kann. Vorbei am Mond und am Satellit, {name} nimmt viele Erinnerungen mit.",
            "image_prompt": "View from behind the character from the reference image, looking out the front window of the spaceship towards approaching planet Earth (blue marble). Fast motion blur stars, cockpit lights reflecting on the glass. 3D Pixar style."
        },
        # SCENE 11: RE-ENTRY (NEW)
        {
            "id": 11,
            "type": "story",
            "is_preview": False,
            "text": "Durch die Wolken zum Boden, ganz warm wird es nun, die Rakete hat jetzt ordentlich zu tun. Bald sind wir zuhause, der Garten ist nah, {name} ist wieder als Entdecker da!",
            "image_prompt": "Exterior shot of a small round spaceship entering Earth's atmosphere, glowing with orange friction heat. Clouds below, blue sky appearing. Dynamic angle, epic feeling. 3D Pixar style."
        },
        # SCENE 12: BACK IN BEDROOM
        {
            "id": 12,
            "type": "story",
            "is_preview": False,
            "text": "Die Landung ist sanft, das Zimmer ist da, war das ein Traum oder war es wahr? Das Bett ist weich und die Decke ist warm, {name} kuschelt sich ein in Mamas Arm.",
            "image_prompt": "Bedroom setting again, morning sunlight coming through window. The character from the reference image is sitting on the edge of the bed, rubbing eyes, looking confused but happy. 3D Pixar style."
        },
        # SCENE 13: THE PROOF
        {
            "id": 13,
            "type": "story",
            "is_preview": True,
            "text": "Doch in der Hand, da leuchtet es hell, der Stein vom Alien, ganz aktuell. {name} lächelt und schläft tief ein, Abenteuer können so wunderbar sein.",
            "image_prompt": "Extreme close-up on the hand of the character from the reference image opening to reveal the glowing blue alien crystal from scene 7. Soft magical glow illuminating the character's face while lying in bed. Peaceful atmosphere, 3D Pixar style."
        }
    ]
}
