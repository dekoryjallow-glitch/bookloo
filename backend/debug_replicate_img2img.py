
import os
import replicate
from dotenv import load_dotenv

load_dotenv(".env")
api_token = os.getenv("REPLICATE_API_TOKEN")

def test_flux_dev_img2img():
    model = "black-forest-labs/flux-dev"
    print(f"\n🧪 Testing {model} with INPUT_IMAGE...")
    
    # Use a dummy image URL (Google Logo or similar)
    dummy_image = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    
    try:
        client = replicate.Client(api_token=api_token)
        output = client.run(
            model,
            input={
                "prompt": "a cyberpunk version of this logo",
                "image": dummy_image, # Try 'image' key
                "prompt_strength": 0.8
            }
        )
        print(f"✅ Success with 'image' key! Output: {output}")
        return
    except Exception as e:
        print(f"❌ Failed with 'image' key: {e}")

    try:
        client = replicate.Client(api_token=api_token)
        output = client.run(
            model,
            input={
                "prompt": "a cyberpunk version of this logo",
                "input_image": dummy_image, # Try 'input_image' key (used in code)
                "aspect_ratio": "1:1"
            }
        )
        print(f"✅ Success with 'input_image' key! Output: {output}")
        return
    except Exception as e:
        print(f"❌ Failed with 'input_image' key: {e}")

if __name__ == "__main__":
    test_flux_dev_img2img()
