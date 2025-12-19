"""
Storybook.ai - Fixed Story Templates
Predefined, curated stories for each theme.
This eliminates GPT-4 latency and gives full control over story quality.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class SceneTemplate:
    """A single scene in the story template."""
    scene_number: int
    scene_type: str  # "cover", "key_scene", "regular"
    visual_prompt: str
    text: str
    emotion: Optional[str] = None
    location: Optional[str] = None


@dataclass
class StoryTemplate:
    """Complete story template with scenes."""
    theme_id: str
    title: str
    moral: str
    scenes: List[SceneTemplate]


# ==============================================================================
# WELTRAUM / SPACE ADVENTURE (11 Scenes)
# ==============================================================================
SPACE_ADVENTURE = StoryTemplate(
    theme_id="space",
    title="Die große Sternenreise",
    moral="Mut und Neugier führen zu großen Entdeckungen",
    scenes=[
        # COVER
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} als mutiger Astronaut im weißen Raumanzug, sitzt im futuristischen Raumschiff-Cockpit mit bunten Kontrollen, durch das große Panoramafenster ist ein spektakulärer Sternenhimmel mit bunten Nebeln sichtbar, {character_name} lächelt aufgeregt und zeigt Daumen hoch, heroische und abenteuerlustige Pose, Pixar 3D animation style, Disney quality, vibrant space colors, cinematic lighting, epic composition""",
            text="Das ist {character_name} - bereit für das größte Abenteuer!",
        ),
        # ACT 1: SETUP (Scenes 1-3) - KEY SCENES for preview
        SceneTemplate(
            scene_number=1,
            scene_type="key_scene",
            location="Kinderzimmer bei Nacht",
            visual_prompt="""{character_name} im gemütlichen Schlafanzug steht am großen Fenster, schaut fasziniert durch ein Teleskop in den Nachthimmel, ein besonders heller mysteriöser Stern leuchtet draußen, im Zimmer Weltraum-Poster und Raketen-Modelle, warmes Licht von einer Astronauten-Nachttischlampe, {character_name} hat große staunende Augen, magische und träumerische Atmosphäre, Pixar 3D animation style, cozy bedroom, magical starlight, sense of wonder""",
            text="Eines Nachts entdeckte {character_name} einen geheimnisvollen Stern am Himmel. Er leuchtete heller als alle anderen - fast so, als würde er {character_name} rufen!",
            emotion="Neugier und Staunen",
        ),
        SceneTemplate(
            scene_number=2,
            scene_type="key_scene",
            location="Dachboden - Die Entdeckung",
            visual_prompt="""{character_name} auf einem staubigen alten Dachboden, Sonnenstrahlen fallen magisch durch ein kleines Dachfenster, in der Ecke steht ein altes glänzendes Raumschiff-Modell das golden leuchtet, das Raumschiff scheint zu pulsieren und zu leben, {character_name} geht vorsichtig näher mit ausgestreckter Hand, Staubpartikel tanzen im Lichtstrahl, staunender Gesichtsausdruck, Pixar 3D animation style, magical discovery moment, dust particles in golden light, sense of mystery""",
            text="Am nächsten Morgen fand {character_name} auf dem Dachboden etwas Unglaubliches: Ein altes Raumschiff-Modell, das zu leuchten begann! Als {character_name} es berührte... geschah Magie!",
            emotion="Überraschung und Faszination",
        ),
        SceneTemplate(
            scene_number=3,
            scene_type="key_scene",
            location="Garten - Der Start",
            visual_prompt="""{character_name} in vollem Astronautenanzug mit glänzendem Helm, steht im heimischen Garten vor einem riesigen echten Raumschiff, das kleine Modell hat sich in eine majestätische Rakete verwandelt, dramatischer Nachthimmel voller Sterne über dem Haus, die Rakete steht auf einer leuchtenden Startrampe mit dampfenden Düsen, {character_name} winkt aufgeregt, Pixar 3D animation style, epic launch moment, starry night, dramatic lighting, sense of adventure""",
            text="Das Modell verwandelte sich in ein echtes Raumschiff! {character_name} zog den Raumanzug an. 'Bis bald, Erde!' rief {character_name}. Dann begann der Countdown: 3... 2... 1... START!",
            emotion="Aufregung und Mut",
        ),
        # ACT 2: ADVENTURE (Scenes 4-7)
        SceneTemplate(
            scene_number=4,
            scene_type="regular",
            location="Durchs Asteroid-Feld",
            visual_prompt="""{character_name} konzentriert am Steuer des Raumschiffs, fliegt geschickt durch ein spektakuläres Asteroid-Feld, riesige bunte Felsen schweben überall in lila blau und rosa leuchtenden Kristall-Tönen, ferne Galaxien und Nebel im Hintergrund, {character_name} hat beide Hände fest am Steuerknüppel, dynamische Action, Pixar 3D animation style, vibrant space colors, exciting navigation scene, dramatic asteroid field""",
            text="Das Raumschiff flog durch ein gefährliches Asteroid-Feld! Links, rechts, oben, unten - überall schwebten riesige Felsen. Aber {character_name} steuerte mutig und geschickt hindurch!",
            emotion="Konzentration und Mut",
        ),
        SceneTemplate(
            scene_number=5,
            scene_type="regular",
            location="Der fremde Planet",
            visual_prompt="""{character_name} steht auf einem wunderschönen fremden Planeten, die Landschaft ist in pink und lila mit riesigen pilzförmigen Bäumen, zwei Sonnen stehen am orangefarbenen Himmel, eine kleine süße Alien-Kreatur wie ein leuchtender Weltraum-Hase mit Antennen sitzt auf {character_name}s Schulter, {character_name} lacht fröhlich, das Raumschiff im Hintergrund gelandet, Pixar 3D animation style, alien world, surreal beautiful landscape, warm lighting, sense of wonder and friendship""",
            text="Auf einem bunten Planeten traf {character_name} ein niedliches Alien namens Zipp! Zipp hatte drei Augen und leuchtete wie ein Glühwürmchen. Die beiden wurden sofort Freunde!",
            emotion="Freude und Freundschaft",
        ),
        SceneTemplate(
            scene_number=6,
            scene_type="regular",
            location="Begegnung mit Weltraum-Walen",
            visual_prompt="""{character_name} schaut durch das große Cockpit-Fenster mit offenem Mund, gigantische majestätische Weltraum-Wale schwimmen friedlich vorbei, die Wale sind durchsichtig und leuchten in schönen Blau- und Türkistönen, sie hinterlassen glitzernde Sternenstaub-Spuren, {character_name} drückt beide Hände begeistert ans Fenster, magische und friedliche Begegnung, Pixar 3D animation style, majestic space whales, bioluminescent creatures, magical encounter, sense of awe""",
            text="Plötzlich tauchten gigantische Weltraum-Wale auf! Sie leuchteten wie Nordlichter und sangen wunderschöne Lieder. {character_name} hatte noch nie etwas so Magisches gesehen!",
            emotion="Ehrfurcht und Glück",
        ),
        SceneTemplate(
            scene_number=7,
            scene_type="regular",
            location="Durch den kosmischen Sturm",
            visual_prompt="""{character_name} im Cockpit während eines dramatischen aber nicht beängstigenden Weltraum-Sturms, bunte kosmische Blitze in pink blau und lila außerhalb des Schiffs, das kleine Alien Zipp hilft mit und zeigt auf Instrumente, {character_name} hält das Steuer fest aber lächelt mutig, Instrumente blinken bunt, Pixar 3D animation style, dramatic storm scene but not scary, colorful lightning, heroic teamwork moment""",
            text="Ein kosmischer Sturm! Das Raumschiff schüttelte und die Lichter blinkten. Aber {character_name} und Zipp arbeiteten zusammen. 'Wir schaffen das!' rief {character_name} mutig.",
            emotion="Mut und Zusammenhalt",
        ),
        # ACT 3: RESOLUTION (Scenes 8-10)
        SceneTemplate(
            scene_number=8,
            scene_type="regular",
            location="Die Mondlandung",
            visual_prompt="""{character_name} macht den ersten Schritt auf den Mond, steht in vollem Raumanzug auf der grauen Mondoberfläche, pflanzt eine bunte Flagge mit Stern-Symbol in den Boden, deutliche Fußabdrücke im Mondstaub sichtbar, die wunderschöne blaue Erde leuchtet groß am schwarzen Sternenhimmel, {character_name} macht eine stolze Siegerpose, das Raumschiff im Hintergrund, Pixar 3D animation style, moon landing, Earth visible in sky, triumphant moment, soft starlight""",
            text="Endlich erreichte {character_name} den Mond! 'Ein kleiner Schritt für mich, ein riesiger für alle Kinder!' Die Erde sah von hier so schön aus - wie eine blaue Murmel.",
            emotion="Stolz und Erfüllung",
        ),
        SceneTemplate(
            scene_number=9,
            scene_type="regular",
            location="Abschied und Heimkehr",
            visual_prompt="""{character_name} umarmt sanft das kleine Alien Zipp zum Abschied, sie stehen vor dem Raumschiff auf dem bunten Planeten, Zipp hält ein kleines Geschenk einen leuchtenden Kristall in den Händen, {character_name} hat Tränen in den Augen aber lächelt warm, Sonnenuntergang mit zwei Sonnen am Horizont, andere Aliens winken im Hintergrund, Pixar 3D animation style, bittersweet farewell, warm sunset lighting, friendship and love""",
            text="Es war Zeit, nach Hause zu fliegen. Zipp gab {character_name} einen leuchtenden Kristall als Erinnerung. 'Freunde bleiben immer im Herzen', sagte {character_name}. Und dann ging die Reise zurück zur Erde.",
            emotion="Wehmut und Dankbarkeit",
        ),
        SceneTemplate(
            scene_number=10,
            scene_type="regular",
            location="Wieder zu Hause",
            visual_prompt="""{character_name} liegt glücklich im eigenen Bett, hält den leuchtenden Kristall von Zipp in der Hand, an der Wand hängt ein selbstgemaltes Bild der Weltraumreise, im Regal stehen neue Souvenirs Mini-Flagge vom Mond und Foto mit Zipp, der Astronautenhelm liegt neben dem Bett, durchs Fenster sind Sterne sichtbar und einer blinkt besonders hell, {character_name} lächelt zufrieden und träumerisch, Pixar 3D animation style, cozy bedroom, peaceful night, sweet dreams, magical memories""",
            text="Wieder zu Hause erzählte {character_name} allen von den Abenteuern. Und jede Nacht, wenn {character_name} zu den Sternen schaute, blinkte einer besonders hell - das war Zipp, der zurückwinkte. Das Ende... oder der Anfang neuer Träume?",
            emotion="Zufriedenheit und Vorfreude",
        ),
    ],
)


# ==============================================================================
# PLACEHOLDER TEMPLATES FOR OTHER THEMES
# (Will be filled in later)
# ==============================================================================
DINO_ADVENTURE = StoryTemplate(
    theme_id="dinos",
    title="Das Dino-Abenteuer",
    moral="Freundschaft überwindet alle Unterschiede",
    scenes=[
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} als mutiger Dino-Forscher mit Safari-Hut, steht neben einem freundlichen grünen Brachiosaurus, üppiger Dschungel im Hintergrund, Pixar 3D animation style, vibrant jungle colors""",
            text="Das ist {character_name} - bereit für ein Urzeit-Abenteuer!",
        ),
    ],
)

PIRATES_ADVENTURE = StoryTemplate(
    theme_id="pirates",
    title="Die Schatzsuche",
    moral="Der wahre Schatz ist Freundschaft",
    scenes=[
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} als mutiger Pirat am Steuer eines bunten Piratenschiffs, Papagei auf der Schulter, tropische Inseln im Hintergrund, Pixar 3D animation style, vibrant ocean colors""",
            text="Das ist {character_name} - bereit für eine Schatzsuche!",
        ),
    ],
)

PRINCESS_ADVENTURE = StoryTemplate(
    theme_id="princess",
    title="Das Königreich der Träume",
    moral="Jeder kann ein Held sein",
    scenes=[
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} als strahlende Prinzessin im Schloss, funkelnde Tiara, magisches Einhorn im Hintergrund, rosa und goldene Farben, Pixar 3D animation style, magical castle""",
            text="Das ist {character_name} - bereit für ein königliches Abenteuer!",
        ),
    ],
)

MAGIC_ADVENTURE = StoryTemplate(
    theme_id="magic",
    title="Der Zauberwald",
    moral="Magie steckt in uns allen",
    scenes=[
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} mit glitzerndem Zauberstab im verzauberten Wald, umgeben von niedlichen Feen und magischen Tieren, leuchtende Pilze und Glühwürmchen, Pixar 3D animation style, enchanted forest""",
            text="Das ist {character_name} - bereit für ein magisches Abenteuer!",
        ),
    ],
)

UNDERWATER_ADVENTURE = StoryTemplate(
    theme_id="underwater",
    title="Das Geheimnis der Tiefsee",
    moral="Die Welt unter dem Meer ist voller Wunder",
    scenes=[
        SceneTemplate(
            scene_number=0,
            scene_type="cover",
            visual_prompt="""{character_name} als Meerjungfrau/Meermann mit glitzernder Flosse, schwimmt mit freundlichen Delfinen durch ein buntes Korallenriff, magische Unterwasserwelt, Pixar 3D animation style, vibrant ocean colors""",
            text="Das ist {character_name} - bereit für ein Unterwasser-Abenteuer!",
        ),
    ],
)


# ==============================================================================
# TEMPLATE REGISTRY
# ==============================================================================
STORY_TEMPLATES: Dict[str, StoryTemplate] = {
    "space": SPACE_ADVENTURE,
    "dinos": DINO_ADVENTURE,
    "pirates": PIRATES_ADVENTURE,
    "princess": PRINCESS_ADVENTURE,
    "magic": MAGIC_ADVENTURE,
    "underwater": UNDERWATER_ADVENTURE,
}


def get_story_template(theme: str) -> StoryTemplate:
    """Get a story template by theme ID."""
    if theme not in STORY_TEMPLATES:
        raise ValueError(f"Unknown theme: {theme}. Available: {list(STORY_TEMPLATES.keys())}")
    return STORY_TEMPLATES[theme]


def personalize_template(template: StoryTemplate, character_name: str) -> StoryTemplate:
    """Replace {character_name} placeholders with the actual name."""
    personalized_scenes = []
    for scene in template.scenes:
        personalized_scenes.append(SceneTemplate(
            scene_number=scene.scene_number,
            scene_type=scene.scene_type,
            visual_prompt=scene.visual_prompt.replace("{character_name}", character_name),
            text=scene.text.replace("{character_name}", character_name),
            emotion=scene.emotion,
            location=scene.location,
        ))
    
    return StoryTemplate(
        theme_id=template.theme_id,
        title=template.title.replace("{character_name}", character_name),
        moral=template.moral,
        scenes=personalized_scenes,
    )
