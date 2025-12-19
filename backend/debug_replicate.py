
import os
import replicate
from dotenv import load_dotenv

load_dotenv(".env")
api_token = os.getenv("REPLICATE_API_TOKEN")

print(f"🔑 API Token found: {bool(api_token)}")

def test_flux_dev():
    model = "black-forest-labs/flux-dev"
    print(f"\n🧪 Testing {model}...")
    try:
        client = replicate.Client(api_token=api_token)
        # Verify model exists by getting it
        # model_obj = client.models.get(model) # This might fail if public interface is different, let's just run it
        
        output = client.run(
            model,
            input={
                "prompt": "a tiny astronaut teddy bear on the moon, pixar style",
                "aspect_ratio": "1:1",
                "output_quality": 80
            }
        )
        print(f"✅ Success! Output: {output}")
        return True
    except Exception as e:
        print(f"❌ Failed {model}: {e}")
        return False

def test_flux_1_dev():
    model = "black-forest-labs/flux-1-dev" 
    print(f"\n🧪 Testing {model}...")
    try:
        client = replicate.Client(api_token=api_token)
        output = client.run(
            model,
            input={
                "prompt": "a tiny astronaut teddy bear on the moon, pixar style",
                "aspect_ratio": "1:1",
                "output_quality": 80
            }
        )
        print(f"✅ Success! Output: {output}")
        return True
    except Exception as e:
        print(f"❌ Failed {model}: {e}")
        return False

if __name__ == "__main__":
    if not test_flux_dev():
        test_flux_1_dev()
