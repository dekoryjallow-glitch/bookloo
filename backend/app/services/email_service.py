"""
bookloo - Email Service
Handles sending notifications and transactional emails.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service for sending emails via bookloo.
    """
    
    SENDER_NAME = "bookloo Team"
    SENDER_EMAIL = "hallo@bookloo.xyz"
    SIGNATURE = "Dein Team von bookloo"
    
    def __init__(self):
        # Placeholder for real mail client (e.g. Resend, SendGrid)
        self.enabled = False
        
    async def send_email(self, to_email: str, subject: str, body: str):
        """Send a basic email."""
        print(f"📧 Sending Email to {to_email}...")
        print(f"   From: {self.SENDER_NAME} <{self.SENDER_EMAIL}>")
        print(f"   Subject: {subject}")
        print(f"   Body: {body}")
        print(f"   --")
        print(f"   {self.SIGNATURE}")
        
        if not self.enabled:
            logger.info(f"   [MOCK] Email sent to {to_email}")
            return True
            
        return True

    async def notify_book_ready(self, user_email: str, book_name: str, preview_url: str):
        """Notify user that their book preview is ready."""
        subject = f"✨ Dein Abenteuer ist bereit: {book_name}"
        body = f"Hallo!\n\nDein personalisiertes Buch '{book_name}' ist fertig generiert. Du kannst es dir hier ansehen:\n{preview_url}\n\nWir wünschen viel Spaß beim Entdecken!"
        return await self.send_email(user_email, subject, body)

    async def notify_order_confirmation(self, user_email: str, book_name: str):
        """Confirm full generation has started."""
        subject = f"🎁 Deine Bestellung für {book_name}"
        body = f"Hallo!\n\nVielen Dank für deine Bestellung! Wir generieren jetzt die restlichen Szenen für '{book_name}' und erstellen dein PDF. Sobald alles fertig ist, melden wir uns wieder!"
        return await self.send_email(user_email, subject, body)
