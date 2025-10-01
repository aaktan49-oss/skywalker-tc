from fastapi import APIRouter, HTTPException, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr

from content_management import get_current_admin_user
from models import (
    NewsletterSubscriber, NewsletterSubscriberCreate, NewsletterCampaign,
    LeadCapture, PageView, AnalyticsEvent, COLLECTIONS
)
# Database will be injected from server.py
db = None

def set_database(database):
    global db
    db = database

async def get_database() -> AsyncIOMotorDatabase:
    return db

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])

# Newsletter Endpoints
@router.post("/newsletter/subscribe", response_model=dict)
async def subscribe_newsletter(
    subscriber_data: NewsletterSubscriberCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Subscribe to newsletter (public endpoint)"""
    try:
        # Check if already subscribed
        existing = await db[COLLECTIONS['newsletter_subscribers']].find_one(
            {"email": subscriber_data.email}
        )
        
        if existing:
            if existing.get('isActive'):
                return {"success": False, "message": "Bu e-posta adresi zaten kayıtlı"}
            else:
                # Reactivate subscription
                await db[COLLECTIONS['newsletter_subscribers']].update_one(
                    {"email": subscriber_data.email},
                    {
                        "$set": {
                            "isActive": True,
                            "subscribedAt": datetime.utcnow(),
                            "unsubscribedAt": None
                        }
                    }
                )
                return {"success": True, "message": "Newsletter aboneliğiniz yeniden aktifleştirildi"}
        
        subscriber = NewsletterSubscriber(
            **subscriber_data.dict()
        )
        
        subscriber_dict = subscriber.dict()
        await db[COLLECTIONS['newsletter_subscribers']].insert_one(subscriber_dict)
        
        return {"success": True, "message": "Newsletter aboneliği başarıyla tamamlandı"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subscribing to newsletter: {str(e)}")

class UnsubscribeRequest(BaseModel):
    email: EmailStr

@router.post("/newsletter/unsubscribe", response_model=dict)
async def unsubscribe_newsletter(
    request: UnsubscribeRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Unsubscribe from newsletter"""
    try:
        result = await db[COLLECTIONS['newsletter_subscribers']].update_one(
            {"email": request.email},
            {
                "$set": {
                    "isActive": False,
                    "unsubscribedAt": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            return {"success": False, "message": "E-posta adresi bulunamadı"}
        
        return {"success": True, "message": "Newsletter aboneliğiniz iptal edildi"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error unsubscribing: {str(e)}")

@router.get("/admin/newsletter/subscribers", response_model=List[dict])
async def get_newsletter_subscribers(
    active_only: bool = True,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get newsletter subscribers (admin only)"""
    try:
        filter_query = {"isActive": True} if active_only else {}
        
        cursor = db[COLLECTIONS['newsletter_subscribers']].find(filter_query).sort("subscribedAt", -1)
        subscribers = await cursor.to_list(length=None)
        
        # Clean up data
        for subscriber in subscribers:
            if '_id' in subscriber:
                del subscriber['_id']
        
        return subscribers
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subscribers: {str(e)}")

# Lead Capture Endpoints
@router.post("/leads/capture", response_model=dict)
async def capture_lead(
    lead_data: dict,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Capture lead information (public endpoint)"""
    try:
        lead = LeadCapture(
            **lead_data,
            ipAddress=request.client.host if request.client else None,
            userAgent=request.headers.get("user-agent")
        )
        
        lead_dict = lead.dict()
        await db[COLLECTIONS['lead_captures']].insert_one(lead_dict)
        
        return {"success": True, "message": "Bilgileriniz başarıyla kaydedildi"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error capturing lead: {str(e)}")

@router.get("/admin/leads", response_model=List[dict])
async def get_leads(
    unprocessed_only: bool = False,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get captured leads (admin only)"""
    try:
        filter_query = {"isProcessed": False} if unprocessed_only else {}
        
        cursor = db[COLLECTIONS['lead_captures']].find(filter_query).sort("createdAt", -1)
        leads = await cursor.to_list(length=None)
        
        # Clean up data
        for lead in leads:
            if '_id' in lead:
                del lead['_id']
        
        return leads
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leads: {str(e)}")

@router.put("/admin/leads/{lead_id}/process", response_model=dict)
async def process_lead(
    lead_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Mark lead as processed (admin only)"""
    try:
        result = await db[COLLECTIONS['lead_captures']].update_one(
            {"id": lead_id},
            {
                "$set": {
                    "isProcessed": True,
                    "processedAt": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {"success": True, "message": "Lead processed successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing lead: {str(e)}")

# Analytics Endpoints
@router.post("/analytics/page-view", response_model=dict)
async def track_page_view(
    page_data: dict,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Track page view (public endpoint)"""
    try:
        page_view = PageView(
            **page_data,
            ipAddress=request.client.host if request.client else None,
            userAgent=request.headers.get("user-agent"),
            referrer=request.headers.get("referer")
        )
        
        page_view_dict = page_view.dict()
        await db[COLLECTIONS['page_views']].insert_one(page_view_dict)
        
        return {"success": True}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking page view: {str(e)}")

@router.post("/analytics/event", response_model=dict)
async def track_event(
    event_data: dict,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Track analytics event (public endpoint)"""
    try:
        event = AnalyticsEvent(**event_data)
        
        event_dict = event.dict()
        await db[COLLECTIONS['analytics_events']].insert_one(event_dict)
        
        return {"success": True}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking event: {str(e)}")

@router.get("/admin/analytics/dashboard", response_model=dict)
async def get_analytics_dashboard(
    days: int = 30,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get analytics dashboard data (admin only)"""
    try:
        from datetime import timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Page views
        page_views_cursor = db[COLLECTIONS['page_views']].find(
            {"timestamp": {"$gte": start_date}}
        )
        page_views = await page_views_cursor.to_list(length=None)
        
        # Newsletter subscribers
        subscribers_count = await db[COLLECTIONS['newsletter_subscribers']].count_documents({"isActive": True})
        
        # Leads
        leads_count = await db[COLLECTIONS['lead_captures']].count_documents(
            {"createdAt": {"$gte": start_date}}
        )
        
        # Top pages
        page_stats = {}
        for view in page_views:
            path = view.get('path', '/')
            page_stats[path] = page_stats.get(path, 0) + 1
        
        top_pages = sorted(page_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_page_views": len(page_views),
            "newsletter_subscribers": subscribers_count,
            "new_leads": leads_count,
            "top_pages": [{"path": path, "views": views} for path, views in top_pages],
            "period_days": days
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")

# WhatsApp Integration
@router.post("/whatsapp/send-message", response_model=dict)
async def send_whatsapp_message(
    phone: str,
    message: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Generate WhatsApp message link (admin only)"""
    try:
        # Clean phone number
        clean_phone = ''.join(filter(str.isdigit, phone))
        if not clean_phone.startswith('90'):
            clean_phone = '90' + clean_phone
        
        # Create WhatsApp link
        whatsapp_url = f"https://wa.me/{clean_phone}?text={message}"
        
        return {
            "success": True,
            "whatsapp_url": whatsapp_url,
            "message": "WhatsApp link created successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating WhatsApp link: {str(e)}")

# Sitemap Generation
@router.get("/sitemap", response_model=dict)
async def generate_sitemap(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Generate sitemap data"""
    try:
        urls = [
            {"loc": "/", "priority": "1.0", "changefreq": "daily"},
            {"loc": "/haber", "priority": "0.8", "changefreq": "daily"},
            {"loc": "/projelerimiz", "priority": "0.8", "changefreq": "weekly"},
            {"loc": "/takimim", "priority": "0.7", "changefreq": "monthly"},
            {"loc": "/referanslar", "priority": "0.7", "changefreq": "monthly"},
            {"loc": "/sss", "priority": "0.6", "changefreq": "monthly"},
            {"loc": "/iletisim", "priority": "0.9", "changefreq": "monthly"},
        ]
        
        # Add news articles
        cursor = db[COLLECTIONS['news_articles']].find({"isActive": True})
        articles = await cursor.to_list(length=None)
        
        for article in articles:
            urls.append({
                "loc": f"/haber/{article['id']}",
                "priority": "0.7",
                "changefreq": "monthly",
                "lastmod": article.get('publishedAt', article.get('createdAt'))
            })
        
        return {"urls": urls}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sitemap: {str(e)}")