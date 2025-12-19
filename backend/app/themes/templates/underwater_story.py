# backend/app/themes/templates/underwater_story.py
"""
Underwater Magic Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""

UNDERWATER_THEME = {
    "theme_id": "underwater",
    "title_pattern": "{name} und das Meeres-Wunder",
    "default_outfit_prompt": "with a shimmering colorful mermaid tail instead of legs, floating underwater, magical underwater aura",
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "{name} und das Meeres-Wunder",
            "image_prompt": "Pixar 3D style, epic movie poster shot. The character from the reference image, who is a {character_desc}, {outfit}, has a glittering mermaid tail and is swimming underwater alongside a friendly dolphin. Sunlight rays piercing through the blue water. Colorful coral reef background, bubbles, masterpiece, 8k."
        },
        # SCENE 1: BEACH DISCOVERY (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "{name} läuft am Strand, die Füße im Sand, da spült eine Welle was in die Hand. Eine Muschel, die singt, die leuchtet in Blau, 'Komm mit', flüstert sie, 'ich zeig dir den Bau.'",
            "image_prompt": "Pixar 3D style, wide shot of a sunny beach. The character from the reference image is wearing normal summer clothes or swimwear, standing at the water's edge, holding a large glowing blue seashell to their ear to listen. Blue ocean, white sand, seagulls."
        },
        # SCENE 2: THE DIVE / TRANSFORMATION
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "Ein Sprung in die Wellen, ein kühles Nass, doch was passiert nun? Was ist denn das? Die Beine verschwinden, eine Flosse wächst dran, jetzt schwimmt {name}, wie kein anderer kann!",
            "image_prompt": "Pixar 3D style, underwater transition shot. The character from the reference image is diving under the water surface. Magical bubbles surround the legs which are transforming {outfit}. The character looks surprised and happy at their new tail. Light rays from above."
        },
        # SCENE 3: THE CORAL REEF
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Hinab in die Tiefe, zum bunten Riff, vorbei am versunkenen Piratenschiff. Die Fische sie leuchten in Gelb und in Rot, hier unten gibt es kein Abendbrot.",
            "image_prompt": "Pixar 3D style, wide angle shot of a vibrant coral reef city. The character from the reference image, {outfit}, is swimming gracefully past colorful corals and huge schools of neon fish. A shipwreck is visible in the background distance."
        },
        # SCENE 4: THE CRAB CHOIR
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Die Krabben sie trommeln, die Quallen sie schweben, so lustig ist also das Unterwasser-Leben. {name} tanzt mit, dreht Pirouetten im Meer, das Schwimmen fällt heute gar nicht mehr schwer.",
            "image_prompt": "Pixar 3D style, playful scene. The character from the reference image, {outfit}, is dancing underwater with a group of cute crabs playing drums on shells. Glowing jellyfish are floating around like lanterns. Happy atmosphere."
        },
        # SCENE 5: THE WISE TURTLE (KEY SCENE)
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Eine Schildkröte paddelt uralt und weise, 'Wohin geht sie denn, die wunderbare Reise?' 'Ich suche die Perle', sagt {name} geschwind, 'die Perle, die man nur im tiefen Meer find.'",
            "image_prompt": "Pixar 3D style, close up eye-level shot. The character from the reference image, {outfit}, is floating face-to-face with a giant, ancient sea turtle. The turtle looks friendly and wise. Sunlight patterns reflecting on their faces."
        },
        # SCENE 6: DOLPHIN RIDE
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Ein Delfin kommt geschossen, 'Halt dich gut fest!', wir schwimmen zum schönsten Unterwasser-Nest. Durch Strömung und Wellen, so schnell wie ein Pfeil, das ist wirklich der allerbeste Teil.",
            "image_prompt": "Pixar 3D style, dynamic action shot. The character from the reference image, {outfit}, is holding onto the dorsal fin of a playful dolphin, speeding through the ocean water. Bubbles trailing behind, hair flowing in the water current. Exhilarating speed."
        },
        # SCENE 7: THE GIANT CLAM
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Ganz tief am Boden, da liegt eine Muschel, so weich wie ein Kissen, so groß wie ein Kuschel. Sie öffnet sich langsam, ein Schimmern erwacht, die Perle des Meeres, in voller Pracht.",
            "image_prompt": "Pixar 3D style, mystery scene. A giant purple clam shell is opening up on the ocean floor. Inside lies a huge, glowing pink pearl. The character from the reference image, {outfit}, is hovering in front of it, face illuminated by the pearl's glow."
        },
        # SCENE 8: SWIMMING UP
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Mit der Perle im Arm geht es wieder nach oben, die Fische und Krebse, sie winken und toben. Das Wasser wird heller, die Sonne bricht ein, gleich wird {name} wieder an Lande sein.",
            "image_prompt": "Pixar 3D style, low angle looking up towards the water surface. The character from the reference image, {outfit}, is swimming upwards towards the bright sun, holding the pearl tight. Silhouette of the surface waves visible."
        },
        # SCENE 9: BACK ON BEACH
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "Der Strand ist so warm, der Sand ist so weich, die Flosse ist weg, doch die Erinnerung reich. War ich ein Fisch? Oder hab ich geträumt? Ich bin froh, dass ich dieses Erlebnis nicht säumt.",
            "image_prompt": "Pixar 3D style, beach setting, sunset. The character from the reference image is back in normal clothes/swimwear, sitting in the sand, wet hair, looking out at the calm ocean. The sun is setting orange on the horizon."
        },
        # SCENE 10: THE PROOF
        {
            "id": 10,
            "type": "story",
            "is_preview": True,
            "text": "Doch in der Hand, da schimmert es rund, die Perle aus dem tiefen Meeresgrund. {name} lächelt und steckt sie gut ein, das Meer wird immer ein Freund von mir sein.",
            "image_prompt": "Pixar 3D style, extreme close-up on the character from the reference image's open hand holding the large, pink shimmering pearl from scene 7. Sand grains on the hand. Soft sunset light making the pearl glow."
        }
    ]
}
