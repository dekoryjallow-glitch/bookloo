# backend/app/themes/templates/dino_story.py
"""
Dino Explorer Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""

DINO_THEME = {
    "theme_id": "dino",
    "title_pattern": "{name} im Land der Dinos",
    "default_outfit_prompt": "wearing a cute beige safari explorer outfit with a hat, cargo shorts and boots",
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "{name} im Land der Dinos",
            "image_prompt": "Pixar 3D style, epic movie poster shot. The character from the reference image, who is a {character_desc}, {outfit}, is standing confidently in a prehistoric jungle, surrounded by friendly colorful dinosaurs like a Triceratops and a Brachiosaurus. Golden hour lighting, magical atmosphere, 8k resolution, masterpiece."
        },
        # SCENE 1: GARDEN DISCOVERY (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "{name} spielt im Garten, gräbt tief im Sand, da spürt {name} plötzlich etwas Hardes in der Hand. Ein riesiger Knochen, so alt und so schwer, wo kommt der bloß her?",
            "image_prompt": "Pixar 3D style, wide shot of a sunny garden behind a house. The character from the reference image is wearing normal casual kids clothes, kneeling in a sandbox, holding up a large ancient dinosaur fossil bone with a surprised and happy expression. Green grass, blue sky, detailed background."
        },
        # SCENE 2: THE PORTAL
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "Der Knochen beginnt zu leuchten, ein Wirbelwind entsteht, {name} staunt, wie sich die Welt um einen dreht! Schwupps, geht es durch einen Tunnel aus Licht, so etwas gab es vorher noch nicht.",
            "image_prompt": "Pixar 3D style, dynamic action shot. The character from the reference image is being pulled into a swirling vortex of magical green and golden light appearing in the garden. The character looks excited, hair blowing in the wind. Magical particles, glowing atmosphere."
        },
        # SCENE 3: ARRIVAL IN JUNGLE
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Plötzlich ist es warm, die Bäume sind riesengroß, {name} landet weich im grünen Moos. Ein Urwald so bunt, mit Farnen so breit, willkommen in der Dinosaurier-Zeit!",
            "image_prompt": "Pixar 3D style, wide angle shot of a lush prehistoric jungle with giant ferns and waterfalls. The character from the reference image, {outfit}, is standing on a mossy rock, looking around in awe. Sunlight streaming through giant leaves. Vibrant colors."
        },
        # SCENE 4: THE GENTLE GIANT
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Die Erde bebt leicht, ein Schatten fällt, wer ist der Größte hier in der Welt? Ein Brachiosaurus, der Hals so lang, doch {name} ist überhaupt nicht bang.",
            "image_prompt": "Pixar 3D style, low angle shot looking up at a massive friendly Brachiosaurus eating leaves from a tree. The character from the reference image, {outfit}, stands close to the dinosaur's leg, looking up with a big smile, reaching out a hand. Majestic scale, peaceful mood."
        },
        # SCENE 5: RIDING THE TRICERATOPS
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Ein Triceratops trabt fröhlich herbei, 'Komm steig auf', ruft er, 'du bist frei!' {name} klettert auf den Rücken geschwind, und reitet so schnell wie der Wind.",
            "image_prompt": "Pixar 3D style, action shot. The character from the reference image, {outfit}, is sitting on the back of a friendly Triceratops, riding it through a prehistoric meadow. The character is laughing and holding onto the horns gently. Dynamic motion, dust kicking up, bright sunny day."
        },
        # SCENE 6: DINO EGG
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Im Nest da knackt es, was mag das sein? Ein Dino-Baby, so süß und so klein! Es schlüpft aus dem Ei und guckt {name} an, wer wohl am besten Grimassen schneiden kann?",
            "image_prompt": "Pixar 3D style, close up eye-level shot. The character from the reference image, {outfit}, is crouching next to a dinosaur nest with large cracked eggs. A cute baby T-Rex is popping its head out of an egg, looking at the character. The character is making a funny face at the baby dino."
        },
        # SCENE 7: PTERODACTYL FLIGHT
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Ein Flugsaurier gleitet leise heran, 'Wer will fliegen, so hoch er nur kann?' {name} hält sich fest, die Aussicht ist toll, der Himmel ist von bunten Wolken voll.",
            "image_prompt": "Pixar 3D style, aerial shot looking down at the jungle landscape. The character from the reference image, {outfit}, is flying on the back of a friendly Pterodactyl, arms wide open. Clouds nearby, volcanoes in the distance. 3D Pixar style."
        },
        # SCENE 8: WATERFALL SPLASH (NEW)
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Ein Wasserfall glitzert, so klar und so rein, 'Komm', ruft ein Dino, 'wir springen hinein!' Das Wasser spritzt hoch, eine kühlende Pracht, {name} hat im Wasser ganz laut gelacht.",
            "image_prompt": "Pixar 3D style, action shot. The character from the reference image is jumping into a crystal clear jungle pool under a waterfall. Friendly water dinosaurs are splashing around. Tropical flowers, bright sun. 3D Pixar style."
        },
        # SCENE 9: VOLCANO DISCOVERY (NEW)
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "In der Ferne, da dampft es, ein Berg voller Rauch, 'Ein Vulkan!', ruft {name}, 'und guck mal dort auch!' Die Erde ist warm, die Steine sind bunt, hier gibt es Abenteuer zu jeder Stund.",
            "image_prompt": "Pixar 3D style, wide shot. The character from the reference image is standing on a ridge overlooking a smoking (not erupting) volcano in the distance. Jungle below, exotic birds. 3D Pixar style."
        },
        # SCENE 10: JUNGLE FEAST (NEW)
        {
            "id": 10,
            "type": "story",
            "is_preview": False,
            "text": "Hungrig vom Reiten, vom Fliegen und Gehen, gibt es nun Früchte, so groß und so schön. Die Dinos sie teilen, es schmeckt wunderbar, so ein Festmahl ist wirklich ganz rar.",
            "image_prompt": "Pixar 3D style, group shot. The character from the reference image is sitting on a log with several small friendly dinosaurs, eating giant colorful glowing jungle fruits. Happy atmosphere, soft lighting. 3D Pixar style."
        },
        # SCENE 11: SUNSET GOODBYE
        {
            "id": 11,
            "type": "story",
            "is_preview": False,
            "text": "Die Sonne geht unter, der Himmel wird rot, 'Ich muss jetzt heim zum Abendbrot!' Die Dinos winken, sie rufen 'Auf Wiedersehen', es war wirklich wunderschön.",
            "image_prompt": "Pixar 3D style, sunset scene. The character from the reference image, {outfit}, is standing near a glowing portal, waving goodbye to a group of dinosaurs. Warm orange and purple lighting. 3D Pixar style."
        },
        # SCENE 12: BACK IN GARDEN
        {
            "id": 12,
            "type": "story",
            "is_preview": False,
            "text": "Der Wirbelwind bringt {name} zurück, genau in den Garten, was für ein Glück. Die Mama ruft: 'Essen ist bereit!', das war eine tolle Reise durch die Zeit.",
            "image_prompt": "Pixar 3D style, the garden setting again, evening light. The character from the reference image is back in normal clothes, standing in the grass, dusting off pants. 3D Pixar style."
        },
        # SCENE 13: THE SOUVENIR
        {
            "id": 13,
            "type": "story",
            "is_preview": True,
            "text": "Doch schau mal genau in die Hosentasche rein, da findet {name} einen bunten Dino-Stein. Er leuchtet im Dunkeln und erinnert daran, dass man mit Fantasie alles erleben kann.",
            "image_prompt": "Pixar 3D style, extreme close-up on the character from the reference image's hands holding a glowing, fossilized dinosaur tooth. Magical sparkle, cozy atmosphere. 3D Pixar style."
        }
    ]
}
