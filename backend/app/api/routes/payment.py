"""
Storybook.ai - Payment API Routes
Endpoints for handling Stripe payments and webhooks.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
import stripe
from app.config import get_settings
from app.services.firebase import BookRepository
from pydantic import BaseModel
from app.api.routes.books import complete_book_task

router = APIRouter()

class CheckoutRequest(BaseModel):
    book_id: str

@router.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    """
    Creates a Stripe Checkout Session for a book purchase.
    """
    settings = get_settings()
    repo = BookRepository()
    
    print(f"💰 Creating Checkout Session for Book: {request.book_id}")
    
    # 1. Load book to verify existence and get user_id
    try:
        book = await repo.get_book(request.book_id)
        if not book:
            print(f"❌ Book {request.book_id} not found in Firestore")
            raise HTTPException(status_code=404, detail="Book not found")
        print(f"   ✅ Book found: {book.child_name} (User: {book.user_id})")
    except Exception as e:
        print(f"❌ Error loading book from Firestore: {e}")
        raise HTTPException(status_code=500, detail="Firestore error")
        
    stripe.api_key = settings.stripe_secret_key
    stripe.api_version = "2023-10-16"
    print(f"   🔑 Stripe Key set: {settings.stripe_secret_key[:10]}...")
    print(f"   🏷️ Price ID: {settings.stripe_price_id}")
    
    try:
        # 2. Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            # Omit payment_method_types and automatic_payment_methods 
            # to use Dashboard settings (requires api_version 2022-11-15+)
            line_items=[
                {
                    'price': settings.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{settings.frontend_url}/dashboard?payment_success=true&book_id={request.book_id}",
            cancel_url=f"{settings.frontend_url}/preview/{request.book_id}",
            metadata={
                'book_id': request.book_id,
                'user_id': book.user_id
            }
        )
        print(f"   ✅ Session created: {checkout_session.url[:50]}...")
        return {"checkout_url": checkout_session.url}
        
    except Exception as e:
        import traceback
        print(f"❌ Stripe Error Details: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

