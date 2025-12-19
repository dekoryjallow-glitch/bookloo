# backend/app/themes/templates/princess_story.py
"""
Princess Kingdom Theme for Storybook.ai (V2 - Flux Kontext)
Uses Flux Kontext for scene generation with character preservation.
"""
from .prompt_constants import QUALITY_BOOSTER

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
            "image_prompt": f"Epic cinematic portrait of the character from the reference image, who is a {{character_desc}}, {{outfit}}, standing gracefully on a castle balcony. Expressive joy in sparkling eyes. Fairytale castle with tall spires and pink clouds in background. Golden hour warm lighting, magical sparkles. {QUALITY_BOOSTER}"
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
            "image_prompt": "Pixar 3D style, wide shot inside a grand ballroom with crystal chandeliers. The character from the reference image, {outfit}, is dancing gracefully in the center of the dance floor. Dress is twirling beautifully. Golden candles, elegant guests watching, magical sparkles in the air, warm festive atmosphere."
        },
        # SCENE 8: THE DRAGON FRIEND (NEW)
        {
            "id": 8,
            "type": "story",
            "is_preview": False,
            "text": "Über den Mauern, wer guckt denn da rein? Ein freundlicher Drache, so zahm und so fein! Er pustet kleine Herzen aus glühendem Rauch, {name} lacht laut und streichelt ihn auch.",
            "image_prompt": "Pixar 3D style, medium shot on a castle balcony at sunset. The character from the reference image, {outfit}, is gently petting a friendly purple dragon that is puffing out heart-shaped pink smoke clouds. The dragon looks adorable with big eyes. Orange and purple sky in background, magical atmosphere."
        },
        # SCENE 9: THE SECRET LIBRARY (NEW)
        {
            "id": 9,
            "type": "story",
            "is_preview": False,
            "text": "In der Bibliothek, da schweben die Bücher, Geschichten erzählen sie, ohne Tücher! 'Lies uns!', rufen sie, 'wir haben viel zu berichten!', von Helden und Feen und fabelhaften Geschichten.",
            "image_prompt": "Pixar 3D style, wide angle shot inside a towering magical library with endless bookshelves. Glowing books are flying through the air around the character from the reference image, {outfit}. The character reaches up to catch one. Golden sunlight streaming through tall windows, dust motes sparkling, mystical atmosphere."
        },
        # SCENE 10: THE ROYAL FEAST (NEW)
        {
            "id": 10,
            "type": "story",
            "is_preview": False,
            "text": "Ein Festmahl wird serviert, auf Tellern aus Gold, so viel wie Prinzessin {name} nur wollt'. Es gibt Honigkuchen und Beerensaft klar, es schmeckt einfach königlich und wunderbar.",
            "image_prompt": "Pixar 3D style, wide shot inside a royal dining hall with a long golden table. The character from the reference image, {outfit}, is sitting at the head of the table surrounded by colorful magical desserts and treats. Cute animals (bunnies, squirrels) are seated as guests. Warm candlelight, elegant atmosphere."
        },
        # SCENE 11: THE SOUVENIR
        {
            "id": 11,
            "type": "story",
            "is_preview": False,
            "text": "Das Einhorn schenkt noch eine Blume aus Glas, 'Damit du uns niemals vergisst, macht das Spaß?' Sie leuchtet wie Sterne, sie duftet nach Glück, doch nun muss {name} leider zurück.",
            "image_prompt": "Pixar 3D style, emotional close-up shot. The unicorn gently places a glowing crystal flower into the hands of the character from the reference image, {outfit}. Soft magical glow illuminating the character's grateful face, sparkles and light particles floating around, bittersweet farewell atmosphere."
        },
        # SCENE 12: FADING MAGIC
        {
            "id": 12,
            "type": "story",
            "is_preview": False,
            "text": "Das Schloss wird zu Nebel, die Musik wird ganz still, auch wenn {name} noch gar nicht nach Hause will. Die Augen fallen zu, der Traum ist vorbei.",
            "image_prompt": "Pixar 3D style, dreamy transition scene. The character from the reference image is standing amidst swirling magical purple and gold mist. The fairy tale castle is fading into the mist behind, while the familiar bedroom walls are reappearing around. Soft ethereal lighting, peaceful expression, magical dust particles."
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
