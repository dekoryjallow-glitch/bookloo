import requests
import os

# Ensure we have a file
if not os.path.exists("assets/mockup_cover.jpg"):
    print("Please create assets/mockup_cover.jpg first (or use any jpg)")
    # make dummy
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='red')
    if not os.path.exists("assets"): os.makedirs("assets")
    img.save("assets/mockup_cover.jpg")

url = "http://localhost:8000/api/assets/generate-character-preview"
files = {
    'file': ('test.jpg', open('assets/mockup_cover.jpg', 'rb'), 'image/jpeg')
}
data = {
    'gender': 'boy',
    'name': 'TestChild'
}

print(f"🚀 Sending request to {url}...")
try:
    response = requests.post(url, files=files, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
