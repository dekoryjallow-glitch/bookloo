import asyncio
import os
import stripe
from app.config import get_settings
from app.services.firebase import initialize_firebase, BookRepository

def debug_stripe():
    settings = get_settings()
    initialize_firebase(settings)
    repo = BookRepository()
    
    # 1. Get a valid book
    print("📋 Listing books...")
    # firebase-admin get() is sync by default
    docs = repo.collection.limit(1).get()
    
    if not docs:
        print("❌ No books found in DB")
        return
    
    book_doc = docs[0]
    book_id = book_doc.id
    book_data = book_doc.to_dict()
    user_id = book_data.get("user_id", "unknown")
    print(f"🔍 Testing with Book ID: {book_id}, User ID: {user_id}")
    
    # 2. Try Stripe Session Create
    stripe_key = settings.stripe_secret_key.strip()
    price_id = settings.stripe_price_id.strip()
    
    print(f"🔑 Secret Key (first 10): '{stripe_key[:10]}...'")
    print(f"🏷️ Price ID: '{price_id}'")
    
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY is empty!")
        return
    if not price_id:
        print("❌ STRIPE_PRICE_ID is empty!")
        return

    stripe.api_key = stripe_key
    stripe.api_version = "2023-10-16"
    
    try:
        print("🚀 Calling stripe.checkout.Session.create (omitting payment methods)...")
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            metadata={
                'book_id': book_id,
                'user_id': user_id
            }
        )
        print(f"✅ Success! Session URL: {session.url}")
    except Exception as e:
        print(f"❌ Stripe Error: {e}")

if __name__ == "__main__":
    debug_stripe()
