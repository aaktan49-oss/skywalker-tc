from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
import uuid
import math

# Import our models and auth
from models import *
from auth import *
from whatsapp_service import whatsapp_service
import portal_endpoints
import content_management
import file_management
import marketing_endpoints
import payment_endpoints
import sms_endpoints
import services_endpoints
import support_endpoints
import company_endpoints
import employee_endpoints

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Skywalker Portal API", version="1.0.0")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Create routers
api_router = APIRouter(prefix="/api")
admin_router = APIRouter(prefix="/api/admin", dependencies=[Depends(get_admin_user)])
customer_router = APIRouter(prefix="/api/customer")

# ===== PUBLIC ENDPOINTS =====

@api_router.get("/")
async def root():
    return {"message": "Skywalker.tc API - May the Force be with you!"}


@api_router.post("/influencer/apply", response_model=ApiResponse)
async def apply_influencer(application: InfluencerApplicationCreate):
    """Submit influencer application"""
    try:
        # Check if email already exists
        existing = await db[COLLECTIONS['influencer_applications']].find_one(
            {"email": application.email}
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Bu e-posta adresiyle zaten bir başvuru bulunuyor."
            )
        
        # Create new application
        app_data = InfluencerApplication(**application.dict())
        result = await db[COLLECTIONS['influencer_applications']].insert_one(
            app_data.dict()
        )
        
        return ApiResponse(
            success=True,
            message="Başvurunuz başarıyla alındı! 24-48 saat içinde size dönüş yapacağız.",
            data={"id": str(result.inserted_id)}
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Influencer application error: {e}")
        raise HTTPException(status_code=500, detail="Başvuru gönderilirken bir hata oluştu.")


@api_router.post("/contact/submit", response_model=ApiResponse)
async def submit_contact(message: ContactMessageCreate):
    """Submit contact form"""
    try:
        # Create new contact message
        contact_data = ContactMessage(**message.dict())
        result = await db[COLLECTIONS['contact_messages']].insert_one(
            contact_data.dict()
        )
        
        return ApiResponse(
            success=True,
            message="Mesajınız başarıyla gönderildi! 24 saat içinde size dönüş yapacağız.",
            data={"id": str(result.inserted_id)}
        )
    except Exception as e:
        logging.error(f"Contact submission error: {e}")
        raise HTTPException(status_code=500, detail="Mesaj gönderilirken bir hata oluştu.")


@api_router.get("/content/{key}")
async def get_content(key: str):
    """Get site content by key"""
    try:
        content = await db[COLLECTIONS['site_content']].find_one({"key": key})
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return {
            "success": True,
            "data": content.get("content", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Content retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Content retrieval failed")


# ===== ADMIN AUTHENTICATION =====

@api_router.post("/admin/login")
async def admin_login(credentials: AdminLogin):
    """Admin login"""
    try:
        # Find admin user
        admin = await db[COLLECTIONS['admin_users']].find_one(
            {"username": credentials.username}
        )
        
        if not admin or not verify_password(credentials.password, admin["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Update last login
        await db[COLLECTIONS['admin_users']].update_one(
            {"_id": admin["_id"]},
            {"$set": {"lastLogin": datetime.utcnow()}}
        )
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": admin["username"],
                "user_id": admin["id"],
                "role": admin["role"]
            }
        )
        
        admin_response = AdminUserResponse(
            id=admin["id"],
            username=admin["username"],
            email=admin["email"],
            role=admin["role"],
            createdAt=admin["createdAt"],
            lastLogin=admin.get("lastLogin")
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": admin_response,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Admin login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")


# ===== ADMIN ENDPOINTS (Protected) =====

@admin_router.get("/dashboard")
async def admin_dashboard():
    """Get admin dashboard statistics"""
    try:
        # Get counts
        influencer_count = await db[COLLECTIONS['influencer_applications']].count_documents({})
        pending_influencers = await db[COLLECTIONS['influencer_applications']].count_documents(
            {"status": "pending"}
        )
        contact_count = await db[COLLECTIONS['contact_messages']].count_documents({})
        new_contacts = await db[COLLECTIONS['contact_messages']].count_documents(
            {"status": "new"}
        )
        
        return {
            "success": True,
            "data": {
                "influencers": {
                    "total": influencer_count,
                    "pending": pending_influencers,
                    "approved": influencer_count - pending_influencers
                },
                "contacts": {
                    "total": contact_count,
                    "new": new_contacts,
                    "replied": contact_count - new_contacts
                }
            }
        }
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to load dashboard")


@admin_router.get("/influencers")
async def get_influencers(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Get influencer applications with pagination"""
    try:
        # Build filter
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        
        # Calculate pagination
        skip = (page - 1) * limit
        
        # Get total count
        total = await db[COLLECTIONS['influencer_applications']].count_documents(filter_dict)
        
        # Get applications
        cursor = db[COLLECTIONS['influencer_applications']].find(filter_dict).sort("createdAt", -1).skip(skip).limit(limit)
        applications = await cursor.to_list(length=limit)
        
        return PaginatedResponse(
            items=applications,
            total=total,
            page=page,
            limit=limit,
            totalPages=math.ceil(total / limit)
        )
    except Exception as e:
        logging.error(f"Get influencers error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve applications")


@admin_router.put("/influencers/{application_id}/status")
async def update_influencer_status(
    application_id: str,
    update_data: InfluencerApplicationUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update influencer application status"""
    try:
        result = await db[COLLECTIONS['influencer_applications']].update_one(
            {"id": application_id},
            {
                "$set": {
                    "status": update_data.status,
                    "reviewNotes": update_data.reviewNotes,
                    "reviewedBy": current_user["user_id"],
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return ApiResponse(
            success=True,
            message="Application status updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Update influencer status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update status")


@admin_router.get("/contacts")
async def get_contacts(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Get contact messages with pagination"""
    try:
        # Build filter
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        
        # Calculate pagination
        skip = (page - 1) * limit
        
        # Get total count
        total = await db[COLLECTIONS['contact_messages']].count_documents(filter_dict)
        
        # Get messages
        cursor = db[COLLECTIONS['contact_messages']].find(filter_dict).sort("createdAt", -1).skip(skip).limit(limit)
        messages = await cursor.to_list(length=limit)
        
        # Remove ObjectId for JSON serialization
        for message in messages:
            if '_id' in message:
                del message['_id']
        
        return PaginatedResponse(
            items=messages,
            total=total,
            page=page,
            limit=limit,
            totalPages=math.ceil(total / limit)
        )
    except Exception as e:
        logging.error(f"Get contacts error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")


@admin_router.put("/contacts/{message_id}/status")
async def update_contact_status(
    message_id: str,
    update_data: ContactMessageUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update contact message status"""
    try:
        result = await db[COLLECTIONS['contact_messages']].update_one(
            {"id": message_id},
            {
                "$set": {
                    "status": update_data.status,
                    "replyMessage": update_data.replyMessage,
                    "repliedBy": current_user["user_id"],
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return ApiResponse(
            success=True,
            message="Message status updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Update contact status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update status")


@admin_router.get("/content")
async def get_all_content():
    """Get all site content for editing"""
    try:
        cursor = db[COLLECTIONS['site_content']].find({})
        content_list = await cursor.to_list(length=None)
        return {
            "success": True,
            "data": content_list
        }
    except Exception as e:
        logging.error(f"Get all content error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content")


@admin_router.put("/content/{key}")
async def update_content(
    key: str,
    update_data: SiteContentUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update site content"""
    try:
        result = await db[COLLECTIONS['site_content']].update_one(
            {"key": key},
            {
                "$set": {
                    "content": update_data.content,
                    "updatedAt": datetime.utcnow(),
                    "updatedBy": current_user["user_id"]
                }
            },
            upsert=True
        )
        
        return ApiResponse(
            success=True,
            message="Content updated successfully"
        )
    except Exception as e:
        logging.error(f"Update content error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update content")


# Import additional endpoints
exec(open('/app/backend/customer_endpoints.py').read())
exec(open('/app/backend/admin_endpoints.py').read())
exec(open('/app/backend/admin_content_endpoints.py').read())


# Include routers (order matters for route matching)
app.include_router(content_management.router)  # Include first to avoid conflicts
app.include_router(portal_endpoints.router)
app.include_router(api_router)
app.include_router(admin_router)
app.include_router(customer_router)
app.include_router(file_management.router)
app.include_router(marketing_endpoints.router)
app.include_router(payment_endpoints.router)
app.include_router(sms_endpoints.router)
app.include_router(services_endpoints.router)
app.include_router(support_endpoints.router)
app.include_router(company_endpoints.router)
app.include_router(employee_endpoints.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inject database into portal endpoints
portal_endpoints.set_database(db)
content_management.set_database(db)
marketing_endpoints.set_database(db)
import portal_auth
portal_auth.set_database(db)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
