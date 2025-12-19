# backend/app/themes/templates/princess_story.py
"""
Princess Kingdom Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""

PRINCESS_THEME = {
    "theme_id": "princess",
    "title_pattern": "Prinzessin {name} im Zauberland",
    "default_outfit_prompt": "wearing a beautiful sparkling pastel-colored princess ballgown and a small golden tiara",
    "scenes": [
        # SCENE 0: COVER
        {
            "id": 0,
            "type": "cover",
            "is_preview": True,
            "text": "Prinzessin {name} im Zauberland",
            "image_prompt": "Pixar 3D style, epic movie poster shot. The character from the reference image, who is a {character_desc}, {outfit}, is standing on a castle balcony. In the background a fairytale castle with tall spires and pink clouds. Magical sparkles, golden hour lighting, masterpiece, 8k."
        },
        # SCENE 1: BEDROOM (INTRO)
        {
            "id": 1,
            "type": "story",
            "is_preview": True,
            "text": "{name} sitzt im Zimmer und blättert im Buch, sucht nach Drachen und Feen-Besuch. 'Ach wär ich Prinzessin', seufzt {name} ganz leis, 'in einem Schloss ganz aus Schnee und aus Eis.'",
            "image_prompt": "Pixar 3D style, wide shot of a cozy children's room. The character from the reference image is wearing normal casual clothes, sitting on a fluffy rug reading a large fairytale book. A toy castle is visible on the floor. Soft daylight, pastel colors."
        },
        # SCENE 2: TRANSFORMATION
        {
            "id": 2,
            "type": "story",
            "is_preview": False,
            "text": "Da glitzert die Seite, der Boden wird Gold, ein Teppich entrollt sich, ganz ehrfurchtsvoll. Die Wände werden hoch, aus Marmor und Stein, {name} tritt in den Thronsaal hinein.",
            "image_prompt": "Pixar 3D style, magical transformation scene. The character from the reference image stands in amazement as the bedroom transforms into a grand royal throne room with high pillars and chandeliers. Magical gold dust swirling around. Dynamic angle."
        },
        # SCENE 3: THE GARDEN
        {
            "id": 3,
            "type": "story",
            "is_preview": False,
            "text": "Hinaus in den Garten, die Blumen sie singen, Schmetterlinge tanzen und Vögelchen springen. Der Brunnen plätschert ein Liedchen dazu, 'Guten Morgen, Hoheit, wie geht es denn Du?'",
            "image_prompt": "Pixar 3D style, wide shot of a magical castle garden. The character from the reference image, {outfit}, is walking down a path lined with giant colorful flowers and a crystal fountain. Bright sunshine, vibrant colors."
        },
        # SCENE 4: THE TEA PARTY
        {
            "id": 4,
            "type": "story",
            "is_preview": False,
            "text": "Ein Tisch ist gedeckt mit Törtchen und Tee, so leckere Sachen, wohin ich nur seh. Die Hasen sind Kellner, die Igel sind Gäste, das ist ja wohl das allerschönste Feste.",
            "image_prompt": "Pixar 3D style, eye-level shot. The character from the reference image, {outfit}, is sitting at a fancy tea table in the garden, holding a tea cup. Cute bunnies wearing bowties are serving cake. whimsical atmosphere, detailed food."
        },
        # SCENE 5: THE UNICORN (KEY SCENE)
        {
            "id": 5,
            "type": "story",
            "is_preview": True,
            "text": "Wer kommt da getrabt, mit Mähne aus Licht? Ein wunderschönes Einhorn, das glaubt man doch nicht! Es neigt seinen Kopf, es wiehert ganz sacht, 'Komm steig auf, wir reiten durch die Nacht!'",
            "image_prompt": "Pixar 3D style, medium shot. The character from the reference image, {outfit}, is gently petting the nose of a magnificent white unicorn with a glowing horn and rainbow mane. The character looks delighted. Magical forest background with fireflies."
        },
        # SCENE 6: FLYING RIDE
        {
            "id": 6,
            "type": "story",
            "is_preview": False,
            "text": "Über die Wolken, das Schloss wird ganz klein, so fühlt sich echtes Fliegen an, wie fein! Der Wind in den Haaren, das Kleid weht im Wind, {name} ist das glücklichste Königskind.",
            "image_prompt": "Pixar 3D style, aerial action shot. The character from the reference image, {outfit}, is riding on the back of the unicorn, flying through pink and purple clouds. The castle is visible far below. Feeling of freedom and joy."
        },
        # SCENE 7: THE BALL
        {
            "id": 7,
            "type": "story",
            "is_preview": False,
            "text": "Am Abend ein Ball, die Musik spielt so laut, jeder hat auf Prinzessin {name} geschaut. Tanzend im Kreis, unter Lichtern so bunt, zu einer fröhlichen, magischen Stund.",
            "image_prompt": "Pixar 3D style, inside a grand ballroom. The character from the reference image, {outfit}, is dancing in the center. Dress is twirling. Festive atmosphere. 3D Pixar style."
        },
        # SCENE 8: THE DRAGON FRIEND (NEW)
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Über den Mauern, wer guckt denn da rein? Ein freundlicher Drache, so zahm und so fein! Er pustet kleine Herzen aus glühendem Rauch, {name} lacht laut und streichelt ihn auch.",
            "image_prompt": "Pixar 3D style, on the castle balcony. The character from the reference image, {outfit}, is petting a friendly purple dragon that is puffing out heart-shaped smoke clouds. 3D Pixar style."
        },
        # SCENE 9: THE SECRET LIBRARY (NEW)
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "In der Bibliothek, da schweben die Bücher, Geschichten erzählen sie, ohne Tücher! 'Lies uns!', rufen sie, 'wir haben viel zu berichten!', von Helden und Feen und fabelhaften Geschichten.",
            "image_prompt": "Pixar 3D style, inside a magical library. Glowing books are flying through the air around the character from the reference image, {outfit}. Golden lighting, dust motes. 3D Pixar style."
        },
        # SCENE 10: THE ROYAL FEAST (NEW)
        {
            "id": 10,
            "type": "story",
            "is_preview": False,
            "text": "Ein Festmahl wird serviert, auf Tellern aus Gold, so viel wie Prinzessin {name} nur wollt'. Es gibt Honigkuchen und Beerensaft klar, es schmeckt einfach königlich und wunderbar.",
            "image_prompt": "Pixar 3D style, inside a dining hall. The character from the reference image, {outfit}, is sitting at a long table filled with magical food. Friendly animals are sitting nearby. 3D Pixar style."
        },
        # SCENE 11: THE SOUVENIR
        {
            "id": 11,
            "type": "story",
            "is_preview": False,
            "text": "Das Einhorn schenkt noch eine Blume aus Glas, 'Damit du uns niemals vergisst, macht das Spaß?' Sie leuchtet wie Sterne, sie duftet nach Glück, doch nun muss {name} leider zurück.",
            "image_prompt": "Pixar 3D style, emotional close up. The character from the reference image, {outfit}, is holding a glowing crystal flower. Magical sparkles. 3D Pixar style."
        },
        # SCENE 12: FADING MAGIC
        {
            "id": 12,
            "type": "story",
            "is_preview": False,
            "text": "Das Schloss wird zu Nebel, die Musik wird ganz still, auch wenn {name} noch gar nicht nach Hause will. Die Augen fallen zu, der Traum ist vorbei.",
            "image_prompt": "Pixar 3D style, transition scene. The character from the reference image amidst swirling magical mist. Bedroom walls appearing. 3D Pixar style."
        },
        # SCENE 13: BACK HOME
        {
            "id": 13,
            "type": "story",
            "is_preview": True,
            "text": "Im eigenen Bett, die Decke ist weich, war das wirklich das Zauberreich? Doch auf dem Kissen, da liegt sie ganz klar, die gläserne Blume – es war alles wahr!",
            "image_prompt": "Pixar 3D style, bedroom setting at night. The character from the reference image is wearing pajamas, sleeping peacefully. Next to the pillow lies the glowing crystal flower. 3D Pixar style."
        }
    ]
}
