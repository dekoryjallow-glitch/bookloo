# backend/app/themes/templates/pirate_story.py
"""
Pirate Adventure Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""
from .prompt_constants import QUALITY_BOOSTER

PIRATE_THEME = {
    "theme_id": "pirate",
    "title_pattern": "Kapitän {name} und der Insel-Schatz",
    "default_outfit_prompt": "wearing a cute pirate captain outfit with a tricorn hat, a red and white striped shirt and a vest",
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "Kapitän {name} und der Insel-Schatz",
            "image_prompt": f"Epic cinematic portrait of the character from the reference image, who is a {{character_desc}}, {{outfit}}, standing heroically on the deck of a grand pirate ship. Expressive adventure spirit in sparkling eyes. White sails billowing, tropical islands in background. Golden hour dramatic lighting. {QUALITY_BOOSTER}"
        },
        # SCENE 1: BATHTUB/PLAYING (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "{name} sitzt in der Wanne, das Wasser spritzt hoch, ein kleines Boot schwimmt, es wackelt noch. 'Ahoi!', ruft {name}, 'Ich will zur See, dorthin, wo ich Palmen und Papageien seh!'",
            "image_prompt": "Pixar 3D style, wide shot of a bright bathroom. The character from the reference image is wearing normal clothes (or bathing suit), kneeling next to a bathtub playing with a small toy wooden ship. Bubbles in the air, playful atmosphere, tiled walls."
        },
        # SCENE 2: TRANSFORMATION
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "Plötzlich wird die Wanne zum riesigen Schiff, der Boden wird Wasser, Vorsicht vor dem Riff! Die Segel gehen hoch, der Wind bläst stark, {name} ist nun Kapitän auf diesem herrlichen Park.",
            "image_prompt": "Pixar 3D style, magical transformation scene. The bathtub transforms into a wooden ship hull. The character from the reference image looks amazed as the room walls dissolve into an open blue ocean. Magical sparkles, wind blowing hair, dynamic angle."
        },
        # SCENE 3: ON THE SHIP
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Das Fernrohr am Auge, den Blick weit voraus, 'Land in Sicht!', ruft Kapitän {name} heraus. Eine Insel aus Gold, mit Palmen so grün, so etwas Schönes hat man noch nie geseh'n.",
            "image_prompt": "Pixar 3D style, on the deck of a pirate ship. The character from the reference image, {outfit}, is looking through a brass spyglass towards the horizon. Blue ocean, splashing waves, clear blue sky, wood textures."
        },
        # SCENE 4: ARRIVAL AT ISLAND
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Der Anker wird geworfen, ritsch und ratsch, die Stiefel landen im weichen Sand-Matsch. Krabben huschen, Muscheln liegen dort, was für ein geheimnisvoller Ort.",
            "image_prompt": "Pixar 3D style, wide beach shot. The character from the reference image, {outfit}, is stepping off a small rowboat onto a white sandy beach. Tropical palm trees and big rocks in the background. Turquoise water, bright sunlight."
        },
        # SCENE 5: THE PARROT COMPANION
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Im Baum sitzt ein Papagei, bunt und laut, er hat dem Piraten auf die Schulter geschaut. 'Den Schatz, den Schatz, den suchen wir!', krächzt er und landet ganz neugierig hier.",
            "image_prompt": "Pixar 3D style, close up eye-level shot. The character from the reference image, {outfit}, is smiling at a colorful macaw parrot sitting on a palm leaf or on the character's shoulder. Lush jungle background, vibrant tropical colors."
        },
        # SCENE 6: THE MAP
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Die Karte ist alt, das Papier ist ganz gelb, 'X markiert den Punkt', so sagt man sich selb. Durch den Dschungel, über die Brücke aus Holz, {name} marschiert mutig und voller Stolz.",
            "image_prompt": "Pixar 3D style, view over the shoulder (or side view). The character from the reference image, {outfit}, is holding an old yellowed treasure map open, pointing at a red X. Jungle path background with vines and exotic flowers."
        },
        # SCENE 7: THE CAVE
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Eine Höhle, ganz dunkel, doch {name} hat Mut, die Fackel leuchtet, das tut richtig gut. Da funkelt es golden, ganz tief im Gestein, das muss der Piratenschatz sicher sein!",
            "image_prompt": "Pixar 3D style, inside a mysterious cave. The character from the reference image, {outfit}, is holding a lantern, illuminating glittering gold coins. Mysterious but friendly atmosphere. 3D Pixar style."
        },
        # SCENE 8: THE TREASURE CHEST
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Die Kiste geht auf, es knarrt und es klemmt, {name} findet darin Goldmünzen und Perlen, so viel man nur kann! Was für ein Fang!",
            "image_prompt": "Pixar 3D style, atmospheric cave interior shot. The character from the reference image, {outfit}, is kneeling behind a large open wooden treasure chest, face illuminated by the warm golden glow of overflowing gold coins, jewels and pearls. Ancient stone walls, spider webs in corners, sense of discovery and wonder."
        },
        # SCENE 9: STORM BATTLE (NEW)
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "Die Wellen sie peitschen, der Himmel wird grau, 'Festhalten!', ruft {name}, 'ich weiß es genau!' Kapitän {name} hält das Steuer ganz fest, bis sich der Sturm langsam wieder verlässt.",
            "image_prompt": "Pixar 3D style, dramatic action shot during a storm at sea. The character from the reference image, {outfit}, is gripping the ship's wooden wheel tightly with determined expression. Massive dark waves crashing, rain pouring, lightning illuminating dark clouds, the parrot holding on nearby. Heroic and intense atmosphere."
        },
        # SCENE 10: BEACH PARTY (NEW)
        {
            "id": 10,
            "type": "story",
            "is_preview": False,
            "text": "Sonne und Sand, wir feiern ein Fest, die Krabben sie tanzen, wer ist der Best'? Musik erklingt aus Muscheln so groß, bei Kapitän {name} ist heute was los!",
            "image_prompt": "Pixar 3D style, joyful wide shot of a tropical beach party. The character from the reference image, {outfit}, is dancing barefoot on the warm sand, surrounded by cute crabs playing tiny coconut drums and the colorful parrot. Musical notes floating in air, tropical fruits on a makeshift table, palm trees swaying, turquoise water sparkling, celebration atmosphere."
        },
        # SCENE 11: SAILING HOME
        {
            "id": 11,
            "type": "story",
            "is_preview": False,
            "text": "Die Taschen sind voll, die Sonne sinkt tief, das Schiff segelt heim, während alles schon schlief. Der Papagei winkt, die Insel wird klein, bald wird {name} wieder zuhause sein.",
            "image_prompt": "Pixar 3D style, peaceful sunset sailing shot from behind the ship. The character from the reference image, {outfit}, is standing at the ship's wheel steering towards a magnificent orange and pink sunset. The treasure island is a small silhouette in the distance. Calm golden waters, seagulls flying, sails catching warm light, nostalgic peaceful atmosphere."
        },
        # SCENE 12: BACK HOME
        {
            "id": 12,
            "type": "story",
            "is_preview": False,
            "text": "Im Bett liegt nun {name}, das Abenteuer war toll, der Kopf ist von Träumen und Seemannsgarn voll. Die Mama gibt einen Kuss auf die Stirn, 'Schlaf gut, kleiner Kapitän'.",
            "image_prompt": "Pixar 3D style, cozy bedroom scene at night. The character from the reference image is tucked into a comfortable bed with soft blankets, eyes closing peacefully. Mom is leaning over giving a gentle goodnight kiss on the forehead. Warm lamp light, toys visible on shelves, moonlight through window, loving tender atmosphere."
        },
        # SCENE 13: THE SOUVENIR
        {
            "id": 13,
            "type": "story",
            "is_preview": True,
            "text": "In der Hand eine Goldmünze, glänzend und schwer, morgen fahren wir wieder hinaus auf das Meer. {name} lächelt im Schlaf ganz versunken und froh, Abenteuer enden genau ebenso.",
            "image_prompt": "Pixar 3D style, extreme close-up on the character's hand holding a single gold pirate coin under the moonlight. Peaceful sleeping expression. 3D Pixar style."
        }
    ]
}
