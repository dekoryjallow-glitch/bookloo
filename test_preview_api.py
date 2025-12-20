import requests
import os

def test_api():
    url = "http://localhost:8000/api/assets/generate-character-preview"
    
    # Use a dummy image
    image_path = "backend/test_image.jpg"
    # Create a dummy image if not exists
    if not os.path.exists(image_path):
        from PIL import Image
        img = Image.new('RGB', (100, 100), color = 'red')
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        img.save(image_path)

    files = {'file': open(image_path, 'rb')}
    data = {'gender': 'boy', 'name': 'Test'}
    
    print(f"🚀 Testing API: {url}")
    try:
        response = requests.post(url, files=files, data=data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_api()
