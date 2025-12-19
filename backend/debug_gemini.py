
import os
import asyncio
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 API Key found: {bool(api_key)}")

async def list_models():
    client = genai.Client(api_key=api_key)
    print("\n📋 Custom Listed Models:")
    
    # Try multiple ways to list, as SDK changes
    try:
        # Standard way
        for m in client.models.list(config={"page_size": 100}):
            if "gemini" in m.name:
                print(f" - {m.name} ({m.display_name})")
    except Exception as e:
        print(f"Error listing models: {e}")

async def test_generation():
    client = genai.Client(api_key=api_key)
    model_id = "models/gemini-2.5-flash-image" # The one we want to test
    print(f"\n🧪 Testing generation with: {model_id}")

    try:
        # Simple text prompt test
        response = client.models.generate_content(
            model=model_id,
            contents="Explain how AI works in one sentence."
        )
        print(f"✅ Success! Response: {response.text}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
    asyncio.run(test_generation())
