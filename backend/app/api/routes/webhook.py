"""
Storybook.ai - Stripe Webhook Handler
Processes payment confirmation and triggers full book generation.
"""

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
import stripe
import logging

from app.config import get_settings
from app.services.firebase import BookRepository
from app.models.book import BookStatus
from app.api.routes.books import complete_book_task

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/stripe")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    POST /api/webhook/stripe
    Stripe Webhook handler for checkout.session.completed
    """
    settings = get_settings()
    stripe.api_key = settings.stripe_secret_key
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    if not sig_header:
        logger.error("❌ Missing stripe-signature header")
        raise HTTPException(status_code=400, detail="Missing signature")

    try:
        # 1. Signature Verification
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        logger.error(f"❌ Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"❌ Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Event Handling
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # 3. Data Extraction (metadata)
        metadata = session.get('metadata', {})
        book_id = metadata.get('book_id')
        
        if book_id:
            logger.info(f"💰 Payment confirmed for Book ID: {book_id}")
            
            repo = BookRepository()
            
            # 4. Status Update (Firestore)
            # Setze status auf paid_processing (PAID_PROCESSING_FULL)
            await repo.update_status(book_id, BookStatus.PAID_PROCESSING_FULL, 10)
            
            # 5. TRIGGER (Async)
            # Rufe die Funktion generate_remaining_scenes (complete_book_task) auf
            background_tasks.add_task(generate_remaining_scenes, book_id)
            logger.info(f"🚀 Triggered full generation for {book_id}")
        else:
            logger.warning("⚠️ No book_id found in session metadata")

    return {"status": "success"}


async def generate_remaining_scenes(book_id: str):
    """
    Wrapper for complete_book_task to follow requested naming convention.
    Generates missing scenes and creates final PDF.
    """
    logger.info(f"🛠️ Starting generate_remaining_scenes for {book_id}")
    await complete_book_task(book_id)
