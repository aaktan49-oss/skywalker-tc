from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum
import uuid


# Enums
class ApplicationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ContactStatus(str, Enum):
    new = "new"
    read = "read"
    replied = "replied"
    archived = "archived"


class ContentType(str, Enum):
    text = "text"
    array = "array"
    object = "object"


class AdminRole(str, Enum):
    admin = "admin"
    superadmin = "superadmin"


# Pydantic Models for Request/Response
class InfluencerApplicationCreate(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    instagram: str = Field(..., min_length=1, max_length=100)
    tiktok: Optional[str] = Field(None, max_length=100)
    followersCount: str = Field(..., min_length=1, max_length=20)
    category: str = Field(..., min_length=1, max_length=100)
    message: Optional[str] = Field(None, max_length=1000)


class InfluencerApplication(InfluencerApplicationCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ApplicationStatus = ApplicationStatus.pending
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    reviewedBy: Optional[str] = None
    reviewNotes: Optional[str] = None


class InfluencerApplicationUpdate(BaseModel):
    status: ApplicationStatus
    reviewNotes: Optional[str] = None


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    service: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)


class ContactMessage(ContactMessageCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ContactStatus = ContactStatus.new
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    repliedBy: Optional[str] = None
    replyMessage: Optional[str] = None


class ContactMessageUpdate(BaseModel):
    status: ContactStatus
    replyMessage: Optional[str] = None


class SiteContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str = Field(..., min_length=1, max_length=100)
    type: ContentType
    content: Any
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    updatedBy: Optional[str] = None


class SiteContentUpdate(BaseModel):
    content: Any


class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str  # This will be hashed
    role: AdminRole = AdminRole.admin
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastLogin: Optional[datetime] = None


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminUserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: AdminRole
    createdAt: datetime
    lastLogin: Optional[datetime] = None


# Response Models
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    totalPages: int


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


# Database Collections Names
COLLECTIONS = {
    'influencer_applications': 'influencer_applications',
    'contact_messages': 'contact_messages',
    'site_content': 'site_content',
    'admin_users': 'admin_users'
}