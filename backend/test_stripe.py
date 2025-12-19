import requests
import sys

def test_stripe_session():
    # Use a real book ID from your Firestore if you have one, 
    # or just test with a dummy one to see if we get a 404 (valid) or 500 (invalid).
    book_id = "test-book-id" 
    url = "http://localhost:8000/api/payment/create-checkout-session"
    
    print(f"Testing Stripe endpoint: {url}")
    try:
        response = requests.post(url, json={"book_id": book_id})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_stripe_session()
