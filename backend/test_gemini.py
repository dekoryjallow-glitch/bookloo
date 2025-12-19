import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Hardcode key from .env for test
API_KEY = "AIzaSyB6MTqBaiQn7EzZOSZcdCwTpEgy7l2I-q4"

def test_gemini():
    client = genai.Client(api_key=API_KEY)
    
    # Load a sample image (use any small asset)
    try:
        if os.path.exists("assets/mockup_cover.jpg"):
             img = Image.open("assets/mockup_cover.jpg")
        elif os.path.exists("assets/mockup_open.png"):
             img = Image.open("assets/mockup_open.png")
        else:
             print("No local asset found, creating dummy")
             img = Image.new('RGB', (100, 100), color='white')
    except Exception as e:
        print(f"Image load error: {e}")
        return

    print("📸 sending request to models/gemini-2.5-flash-image with FULL PROMPT...")
    
    prompt = (
        "Transform this child into a 3D Pixar animated character. "
        "Disney concept art style, cute portrait, vibrant colors, smooth 3D render, "
        "subsurface scattering, big expressive eyes, cinematic lighting, 8k resolution. "
        "Keep the exact same facial features, skin tone, and ethnicity. "
        "Full body front view, clean white background, professional character concept art."
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-image",
            contents=[img, prompt],
        )
        print("\n--- RESPONSE ---")
        if response.candidates:
            for i, c in enumerate(response.candidates):
                if c.content and c.content.parts:
                    for part in c.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(f"  Text: {part.text}")
                        if hasattr(part, 'inline_data') and part.inline_data:
                            print(f"  ✅ Image Data Found! Mime: {part.inline_data.mime_type}")
        else:
            print("No candidates.")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    test_gemini()
