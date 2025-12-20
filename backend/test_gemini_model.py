import asyncio
import os
from google import genai
from google.genai import types
from PIL import Image
import requests
from io import BytesIO

async def test_gemini_image():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set")
        return

    client = genai.Client(api_key=api_key)
    
    # Dummy image (red square)
    img = Image.new('RGB', (100, 100), color = 'red')
    
    prompt = "A cute 3D Pixar character"
    model_id = "gemini-2.0-flash"
    
    print(f"🚀 Testing model: {model_id}")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=[img, prompt]
        )
        print("✅ Success!")
        if response.candidates:
             print(f"   Finish Reason: {response.candidates[0].finish_reason}")
             if response.candidates[0].content and response.candidates[0].content.parts:
                 for i, part in enumerate(response.candidates[0].content.parts):
                     print(f"   Part {i}: {type(part)}")
                     if hasattr(part, 'text') and part.text:
                         print(f"     Text: {part.text[:50]}...")
                     if hasattr(part, 'inline_data') and part.inline_data:
                         print(f"     Inline Data (Image) Found!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(test_gemini_image())
