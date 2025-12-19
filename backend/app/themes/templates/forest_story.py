# backend/app/themes/templates/forest_story.py
"""
Magic Forest Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""

FOREST_THEME = {
    "theme_id": "forest",
    "title_pattern": "{name} im Zauberwald",
    "default_outfit_prompt": "wearing a magical outfit made of green leaves and soft fabrics, with a small green cape, looking like a forest elf",
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "{name} im Zauberwald",
            "image_prompt": "Pixar 3D style, epic movie poster shot. The character from the reference image, who is a {character_desc}, {outfit}, is sitting on a giant glowing mushroom in a magical forest. Surrounded by floating fireflies and sparkles. Mysterious blue and green lighting, masterpiece, 8k."
        },
        # SCENE 1: GARDEN HEDGE (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "Hinter dem Haus, bei der alten Hecke, entdeckt {name} eine versteckte Ecke. Ein kleines Tor, ganz aus Efeu gemacht, wer hätte das bloß gedacht?",
            "image_prompt": "Pixar 3D style, wide shot of a garden corner. The character from the reference image is wearing normal casual clothes, pushing aside branches of a thick green hedge to reveal a small, glowing wooden door hidden within the leaves. Curious expression, sunlight filtering through."
        },
        # SCENE 2: CRAWLING THROUGH
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "{name} schlüpft hindurch, ganz leise und sacht, auf einmal wird aus dem Tag eine Nacht? Nein, es leuchtet überall, wie bei einem Sternschnuppen-Fall.",
            "image_prompt": "Pixar 3D style, transition scene. The character from the reference image is crawling through a tunnel of vines and flowers. The light changes from daylight behind to a magical purple twilight ahead. Magical dust particles in the air."
        },
        # SCENE 3: THE GIANT MUSHROOMS
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Der Wald ist riesig, die Pilze sind hoch, höher als ein Haus sind sie doch! Sie leuchten in Blau und in Pink, {name} staunt und winkt.",
            "image_prompt": "Pixar 3D style, wide angle low shot of a fantasy forest. The character from the reference image, {outfit}, is standing under towering giant mushrooms that glow with neon colors. The character looks tiny compared to the mushrooms. Wonder and awe."
        },
        # SCENE 4: THE FAIRY QUEEN
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Da surrt es und schwirrt es, ein Licht kommt heran, eine kleine Fee, die zaubern kann. 'Hallo {name}', ruft sie fein, 'willkommen in unserem Wald, tritt ein!'",
            "image_prompt": "Pixar 3D style, close up shot. The character from the reference image, {outfit}, is looking at a small glowing fairy flying in front of their nose. The fairy leaves a trail of gold dust. Background is blurred magical forest bokeh."
        },
        # SCENE 5: RIDING THE STAG (KEY SCENE)
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Ein Hirsch kommt geschritten, mit Geweih aus Kristall, er trägt {name} sicher, ohne einen Fall. Durch das Moos, über den Bach, die Eulen werden im Baume wach.",
            "image_prompt": "Pixar 3D style, side view action shot. The character from the reference image, {outfit}, is sitting on the back of a majestic stag with antlers made of glowing crystal. They are walking through a shallow magical stream. Peaceful and majestic atmosphere."
        },
        # SCENE 6: THE FOREST CONCERT
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Die Tiere machen Musik, die Grillen, die Finken, die Glühwürmchen, die im Takte blinken. {name} klatscht in die Hände und lacht, was für eine wunderschöne Pracht.",
            "image_prompt": "Pixar 3D style, group shot. The character from the reference image, {outfit}, is sitting on a log, surrounded by cute woodland animals (rabbits, squirrels, birds) who seem to be singing or playing instruments. The character is clapping hands happily. Magical gathering."
        },
        # SCENE 7: THE ACORN GIFT
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Die Fee schenkt eine Eichel, sie schimmert in Gold, 'Die ist nur für dich, weil du bist so hold.' Ein Zauber steckt drin, für Mut und für Glück, nun geh bitte wieder nach Hause zurück.",
            "image_prompt": "Pixar 3D style, close up on hands. The glowing fairy is placing a golden, shining magical acorn into the open hands of the character from the reference image, {outfit}. Soft, warm light emanating from the acorn illuminating the character's face."
        },
        # SCENE 8: LEAVING THE FOREST
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Zurück durch die Hecke, das licht wird ganz hell, der Zauberwald schwindet, doch gar nicht so schnell. Der Hirsch winkt noch einmal, die Fee ruft 'Ade', bis ich euch im Traume wiederseh.",
            "image_prompt": "Pixar 3D style, looking back shot. The character from the reference image, {outfit}, is stepping back through the vine tunnel towards the bright daylight of the garden, looking back one last time at the fading magical twilight forest and the waving animals."
        },
        # SCENE 9: BACK IN GARDEN
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "Im Garten ist es still, die Sonne scheint warm, {name} nimmt den Teddy fest in den Arm. War ich wirklich fort? Oder war es ein Spiel? Ich habe erlebt, so unglaublich viel.",
            "image_prompt": "Pixar 3D style, garden setting, sunny afternoon. The character from the reference image is wearing normal clothes again, standing next to the hedge, hugging a teddy bear tightly. Leaves in their hair. Realistic garden background."
        },
        # SCENE 10: THE PROOF
        {
            "id": 10,
            "type": "story",
            "is_preview": True,
            "text": "Doch in der Tasche, da raschelt es leis, {name} greift hinein und was ist der Beweis? Die goldene Eichel, sie liegt in der Hand, ein Gruß aus dem fernen Zauberland.",
            "image_prompt": "Pixar 3D style, extreme close-up on the character from the reference image's hand holding the golden acorn from scene 7 against the fabric of their normal trousers. Sunlight hits the gold, making it sparkle. A knowing smile on the face (partially visible)."
        }
    ]
}
