import aiohttp
import logging
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# WhatsApp Business API Configuration
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://api.whatsapp.com/send")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")


class WhatsAppService:
    def __init__(self):
        self.api_url = WHATSAPP_API_URL
        self.token = WHATSAPP_TOKEN
        self.phone_id = WHATSAPP_PHONE_ID
        self.is_enabled = bool(self.token and self.phone_id)
    
    async def send_message(self, phone_number: str, message: str) -> bool:
        """Send WhatsApp message to customer"""
        if not self.is_enabled:
            logger.warning("WhatsApp service not configured - skipping message send")
            return False
        
        try:
            # For now, we'll use a simple URL-based approach
            # In production, you'd want to use WhatsApp Business API
            whatsapp_url = f"https://wa.me/{phone_number.replace('+', '').replace(' ', '')}?text={message}"
            
            logger.info(f"WhatsApp message prepared for {phone_number}: {whatsapp_url}")
            
            # Since we can't actually send via API without proper WhatsApp Business setup,
            # we'll just log the message and return True for demo purposes
            logger.info(f"Mock WhatsApp send - Phone: {phone_number}, Message: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return False
    
    async def send_ticket_notification(self, phone_number: str, ticket_number: str, message: str, customer_name: str) -> bool:
        """Send ticket-related notification"""
        formatted_message = f"""
🎯 Skywalker.tc Destek Bildirimi

Merhaba {customer_name},

Talep Numarası: {ticket_number}
{message}

Detaylar için: skywalker.tc/tickets

May the Force be with you! ⭐
        """.strip()
        
        return await self.send_message(phone_number, formatted_message)
    
    async def send_ticket_resolved_notification(self, phone_number: str, ticket_number: str, customer_name: str, resolution_note: str = "") -> bool:
        """Send notification when ticket is resolved"""
        message = f"""
✅ Talebiniz Çözüldü!

Merhaba {customer_name},

Talep Numarası: {ticket_number}
Durum: Çözüldü

{resolution_note if resolution_note else 'Talebiniz başarıyla çözülmüştür.'}

Geri bildirimleriniz için: skywalker.tc

Teşekkürler! 🚀
        """.strip()
        
        return await self.send_message(phone_number, message)
    
    async def send_welcome_message(self, phone_number: str, customer_name: str) -> bool:
        """Send welcome message to new customers"""
        message = f"""
🌟 Skywalker.tc'ye Hoş Geldiniz!

Merhaba {customer_name},

Trendyol galaksisinde liderlik yolculuğunuz başladı! 

Hesabınız aktif edildi. Artık:
• Destek talebi oluşturabilir
• Uzman ekibimizle iletişim kurabilir  
• Projelerinizi takip edebilirsiniz

Güç sizinle olsun! ⚡

skywalker.tc
        """.strip()
        
        return await self.send_message(phone_number, message)


# Global WhatsApp service instance
whatsapp_service = WhatsAppService()