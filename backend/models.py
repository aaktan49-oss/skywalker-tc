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
    'admin_users': 'admin_users',
    'customers': 'customers',
    'tickets': 'tickets',
    'team_members': 'team_members',
    'ticket_messages': 'ticket_messages',
    'site_settings': 'site_settings',
    # New B2B Portal Collections
    'users': 'users',
    'collaborations': 'collaborations',
    'collaboration_interests': 'collaboration_interests',
    'partner_requests': 'partner_requests',
    'notifications': 'notifications',
    'company_logos': 'company_logos',
    'news_articles': 'news_articles',
    'company_projects': 'company_projects',
    # Support System Collections
    'support_tickets': 'support_tickets',
    'ticket_responses': 'ticket_responses',
    'customer_profiles': 'customer_profiles',
    # Company Management Collections  
    'meeting_notes': 'meeting_notes',
    'recurring_tasks': 'recurring_tasks',
    'partnership_requests': 'partnership_requests',
    'uploaded_files': 'uploaded_files',
    # New CMS Collections
    'team_members_cms': 'team_members_cms',
    'testimonials': 'testimonials',
    'faqs': 'faqs',
    'system_notifications': 'system_notifications',
    'notification_templates': 'notification_templates',
    # Marketing & Analytics Collections
    'newsletter_subscribers': 'newsletter_subscribers',
    'newsletter_campaigns': 'newsletter_campaigns',
    'lead_captures': 'lead_captures',
    'page_views': 'page_views',
    'analytics_events': 'analytics_events'
}


# New Models for Extended System

# Site Content Management Models
class SiteContentType(str, Enum):
    hero_section = "hero_section"
    services = "services"
    about = "about"
    team = "team"
    testimonials = "testimonials"
    faq = "faq"
    contact = "contact"
    header_nav = "header_nav"
    footer = "footer"

class SiteContentItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section: SiteContentType
    key: str  # unique identifier within section
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    linkText: Optional[str] = None
    order: int = 0
    isActive: bool = True
    metadata: dict = {}  # Additional flexible data
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    updatedBy: Optional[str] = None  # admin user id

class SiteContentCreate(BaseModel):
    section: SiteContentType
    key: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    linkText: Optional[str] = None
    order: int = 0
    metadata: dict = {}

class SiteContentItemUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    linkText: Optional[str] = None
    order: Optional[int] = None
    isActive: Optional[bool] = None
    metadata: Optional[dict] = None

# Page Settings Model for global site settings
class SiteSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    siteName: str = "Skywalker.tc"
    siteDescription: str = "Trendyol E-ticaret Danışmanlık ve Pazarlama Hizmetleri"
    contactEmail: str = "info@skywalker.tc"
    contactPhone: str = "+90 555 123 45 67"
    address: str = "İstanbul, Türkiye"
    logo: str = ""
    favicon: str = ""
    primaryColor: str = "#8B5CF6"
    secondaryColor: str = "#3B82F6"
    socialMedia: dict = {}
    seoKeywords: List[str] = []
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    # SEO & Analytics Settings
    googleAnalyticsId: str = ""
    googleAdsId: str = ""
    googleTagManagerId: str = ""
    googleSearchConsoleId: str = ""
    facebookPixelId: str = ""
    metaVerificationCode: str = ""
    googleVerificationCode: str = ""
    bingVerificationCode: str = ""
    yandexVerificationCode: str = ""
    
    # Meta Tags
    metaTitle: str = ""
    metaDescription: str = ""
    metaKeywords: List[str] = []
    ogTitle: str = ""
    ogDescription: str = ""
    ogImage: str = ""
    twitterCard: str = "summary_large_image"
    twitterSite: str = ""
    twitterCreator: str = ""
    
    # Business Settings
    businessSchema: dict = {}
    whatsappNumber: str = ""
    liveChatEnabled: bool = False
    liveChatWidget: str = ""
    newsletterEnabled: bool = True
    cookieConsentEnabled: bool = True

class SiteSettingsUpdate(BaseModel):
    siteName: Optional[str] = None
    siteDescription: Optional[str] = None
    contactEmail: Optional[str] = None
    contactPhone: Optional[str] = None
    address: Optional[str] = None
    logo: Optional[str] = None
    favicon: Optional[str] = None
    primaryColor: Optional[str] = None
    secondaryColor: Optional[str] = None
    socialMedia: Optional[dict] = None
    seoKeywords: Optional[List[str]] = None
    isActive: Optional[bool] = None
    
    # SEO & Analytics Settings
    googleAnalyticsId: Optional[str] = None
    googleAdsId: Optional[str] = None
    googleTagManagerId: Optional[str] = None
    googleSearchConsoleId: Optional[str] = None
    facebookPixelId: Optional[str] = None
    metaVerificationCode: Optional[str] = None
    googleVerificationCode: Optional[str] = None
    bingVerificationCode: Optional[str] = None
    yandexVerificationCode: Optional[str] = None
    
    # Meta Tags
    metaTitle: Optional[str] = None
    metaDescription: Optional[str] = None
    metaKeywords: Optional[List[str]] = None
    ogTitle: Optional[str] = None
    ogDescription: Optional[str] = None
    ogImage: Optional[str] = None
    twitterCard: Optional[str] = None
    twitterSite: Optional[str] = None
    twitterCreator: Optional[str] = None
    
    # Business Settings
    businessSchema: Optional[dict] = None
    whatsappNumber: Optional[str] = None
    liveChatEnabled: Optional[bool] = None
    liveChatWidget: Optional[str] = None
    newsletterEnabled: Optional[bool] = None
    cookieConsentEnabled: Optional[bool] = None

# News System Models
class NewsCategory(str, Enum):
    company_news = "company_news"
    success_stories = "success_stories"
    industry_news = "industry_news"
    announcements = "announcements"

class NewsArticle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    excerpt: Optional[str] = None
    imageUrl: Optional[str] = None
    category: NewsCategory
    isPublished: bool = True
    publishedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None  # admin user id

class NewsArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    imageUrl: Optional[str] = None
    category: NewsCategory
    isPublished: bool = True

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    imageUrl: Optional[str] = None
    category: Optional[NewsCategory] = None
    isPublished: Optional[bool] = None

# Company Projects Models
class ProjectStatus(str, Enum):
    completed = "completed"
    in_progress = "in_progress"
    planned = "planned"

class CompanyProject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clientName: str
    clientEmail: Optional[str] = None
    projectTitle: str
    description: str
    category: str  # e.g., "E-commerce Optimization", "Social Media Management"
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    status: ProjectStatus
    results: Optional[str] = None  # Project outcomes/results
    imageUrl: Optional[str] = None
    images: List[str] = []  # Multiple project images
    tags: List[str] = []
    isPublic: bool = True  # Whether to show in public portfolio
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None  # admin user id

class CompanyProjectCreate(BaseModel):
    clientName: str = Field(..., min_length=1, max_length=200)
    clientEmail: Optional[EmailStr] = None
    projectTitle: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    status: ProjectStatus
    results: Optional[str] = None
    imageUrl: Optional[str] = None
    images: List[str] = []
    tags: List[str] = []
    isPublic: bool = True

class CompanyProjectUpdate(BaseModel):
    clientName: Optional[str] = Field(None, min_length=1, max_length=200)
    clientEmail: Optional[EmailStr] = None
    projectTitle: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    status: Optional[ProjectStatus] = None
    results: Optional[str] = None
    imageUrl: Optional[str] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    isPublic: Optional[bool] = None

# Duplicate SiteSettings class removed - using comprehensive version above


# New Models for Extended System

class CustomerRegistration(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=6)


class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    password: str  # hashed
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastLogin: Optional[datetime] = None


class CustomerLogin(BaseModel):
    email: EmailStr
    password: str


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    waiting_customer = "waiting_customer"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    priority: TicketPriority = TicketPriority.medium
    service: Optional[str] = Field(None, max_length=100)


class Ticket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticketNumber: str = Field(default_factory=lambda: f"SKY-{uuid.uuid4().hex[:8].upper()}")
    customerId: str
    title: str
    description: str
    status: TicketStatus = TicketStatus.open
    priority: TicketPriority
    service: Optional[str] = None
    assignedTo: Optional[str] = None  # team member id
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    resolvedAt: Optional[datetime] = None


class TicketMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticketId: str
    senderId: str
    senderType: str  # 'customer' or 'team'
    senderName: str
    message: str = Field(..., min_length=1, max_length=2000)
    isInternal: bool = False  # internal team notes
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class TicketMessageCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    isInternal: bool = False


class TeamMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    character: str = Field(..., min_length=1, max_length=100)  # Star Wars character
    role: str = Field(..., min_length=1, max_length=100)
    specialization: str = Field(..., min_length=1, max_length=200)
    avatar: Optional[str] = None  # image URL
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus
    assignedTo: Optional[str] = None
    resolutionNote: Optional[str] = None


class WhatsAppConfig(BaseModel):
    apiKey: str
    phoneNumber: str
    isActive: bool = True


# ===== NEW B2B PORTAL MODELS =====

class UserRole(str, Enum):
    admin = "admin"
    influencer = "influencer" 
    partner = "partner"
    employee = "employee"  # Çalışan rolü


# Çalışan Yetki Seviyeleri
class EmployeePermission(str, Enum):
    contacts = "contacts"              # İletişim mesajları
    collaborations = "collaborations"  # İşbirlikleri  
    users = "users"                   # Kullanıcı yönetimi
    content = "content"               # İçerik yönetimi
    analytics = "analytics"           # Analitik raporları
    settings = "settings"             # Sistem ayarları


# CollaborationStatus moved to enhanced collaboration section


class PartnerRequestCategory(str, Enum):
    genel = "genel"
    grafik = "grafik"
    teknik = "teknik"
    satis = "satis"
    reklam = "reklam"


class NotificationType(str, Enum):
    email = "email"
    site = "site"
    both = "both"


# ===== SUPPORT TICKET SYSTEM =====
class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"
    

class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class SupportTicket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticketNumber: str = Field(default_factory=lambda: f"TICK-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}")
    customerId: str  # Reference to User or contact info
    customerEmail: str
    customerName: str
    customerPhone: Optional[str] = None
    subject: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    priority: TicketPriority = TicketPriority.medium
    status: TicketStatus = TicketStatus.open
    assignedTo: Optional[str] = None  # Employee ID
    category: str = Field(..., min_length=1)  # "technical", "billing", "general"
    tags: List[str] = []
    attachments: List[str] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    resolvedAt: Optional[datetime] = None
    closedAt: Optional[datetime] = None


class TicketResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticketId: str
    responderId: str  # Employee/Admin ID
    responderName: str
    message: str = Field(..., min_length=1)
    isInternal: bool = False  # Internal notes vs customer responses
    attachments: List[str] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)


# ===== CUSTOMER MANAGEMENT SYSTEM =====
class CustomerProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = None
    totalTickets: int = 0
    activeTickets: int = 0
    lastContactDate: Optional[datetime] = None
    customerSince: datetime = Field(default_factory=datetime.utcnow)
    notes: str = ""
    tags: List[str] = []
    priority: str = "normal"  # "vip", "normal", "low"


# ===== COMPANY MANAGEMENT SYSTEM =====
class CompanyInternalProject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    companyId: str  # Reference to partner user ID
    projectName: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)  # "active", "completed", "paused"
    startDate: datetime = Field(default_factory=datetime.utcnow)
    endDate: Optional[datetime] = None
    assignedEmployees: List[str] = []  # Employee IDs
    budget: Optional[float] = None
    completedTasks: List[str] = []
    pendingTasks: List[str] = []
    documents: List[str] = []  # File paths
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class MeetingNote(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    companyId: str
    title: str = Field(..., min_length=1, max_length=200)
    meetingDate: datetime
    participants: List[str] = []  # Names or employee IDs
    documentPath: str  # Path to uploaded Word document
    summary: Optional[str] = None
    actionItems: List[str] = []
    createdBy: str  # Employee ID
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class RecurringTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    companyId: str
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    frequency: str = Field(..., min_length=1)  # "daily", "weekly", "monthly", "quarterly"
    assignedTo: str  # Employee ID
    nextDueDate: datetime
    lastCompleted: Optional[datetime] = None
    isActive: bool = True
    priority: str = "medium"  # "low", "medium", "high"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


# User Management
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    password: str  # hashed
    role: UserRole
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    isActive: bool = True
    isApproved: bool = False  # For influencer auto-approval
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastLogin: Optional[datetime] = None
    
    # Role-specific fields
    instagram: Optional[str] = None  # For influencers
    tiktok: Optional[str] = None     # For influencers
    followersCount: Optional[str] = None  # For influencers
    category: Optional[str] = None   # For influencers
    
    # Employee permissions
    permissions: List[EmployeePermission] = []  # For employees


class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    role: UserRole
    
    # Influencer specific fields
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    followersCount: Optional[str] = None
    category: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    firstName: str
    lastName: str
    phone: Optional[str]
    company: Optional[str]
    isActive: bool
    isApproved: bool
    createdAt: datetime
    lastLogin: Optional[datetime]
    instagram: Optional[str] = None
    followersCount: Optional[str] = None
    category: Optional[str] = None


# Collaboration System Enhancements
class CollaborationStatus(str, Enum):
    draft = "draft"          # Admin tarafından oluşturuldu ama yayınlanmadı
    published = "published"  # Yayınlandı, influencer'lar görebilir
    in_progress = "in_progress"  # En az 1 influencer kabul etti
    completed = "completed"  # Tamamlandı
    cancelled = "cancelled"  # İptal edildi

class CollaborationPriority(str, Enum):
    low = "low"
    medium = "medium"  
    high = "high"
    urgent = "urgent"

class Collaboration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    requirements: Optional[str] = None  # Gereksinimler
    deliverables: List[str] = []  # Teslimatlar
    category: str  # influencer kategori filtresi için
    budget: Optional[float] = None
    deadline: Optional[datetime] = None
    priority: CollaborationPriority = CollaborationPriority.medium
    status: CollaborationStatus = CollaborationStatus.draft
    tags: List[str] = []
    
    # Targeting
    minFollowers: Optional[int] = None
    maxFollowers: Optional[int] = None
    targetCategories: List[str] = []  # hedef influencer kategorileri
    targetLocations: List[str] = []   # hedef şehirler
    
    # Media requirements
    imageUrl: Optional[str] = None
    attachments: List[str] = []
    
    # Admin tracking
    createdBy: str  # admin user id
    assignedInfluencers: List[str] = []  # kabul eden influencer'lar
    maxInfluencers: int = 1  # max kaç influencer kabul edebilir
    
    # Dates
    publishedAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    completedAt: Optional[datetime] = None

class CollaborationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    requirements: Optional[str] = None
    deliverables: List[str] = []
    category: str = Field(..., min_length=1)
    budget: Optional[float] = Field(None, ge=0)
    deadline: Optional[datetime] = None
    priority: CollaborationPriority = CollaborationPriority.medium
    tags: List[str] = []
    minFollowers: Optional[int] = Field(None, ge=0)
    maxFollowers: Optional[int] = Field(None, ge=0)
    targetCategories: List[str] = []
    targetLocations: List[str] = []
    imageUrl: Optional[str] = None
    attachments: List[str] = []
    maxInfluencers: int = Field(1, ge=1, le=10)

class CollaborationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    requirements: Optional[str] = None
    deliverables: Optional[List[str]] = None
    category: Optional[str] = Field(None, min_length=1)
    budget: Optional[float] = Field(None, ge=0)
    deadline: Optional[datetime] = None
    priority: Optional[CollaborationPriority] = None
    status: Optional[CollaborationStatus] = None
    tags: Optional[List[str]] = None
    minFollowers: Optional[int] = Field(None, ge=0)
    maxFollowers: Optional[int] = Field(None, ge=0)
    targetCategories: Optional[List[str]] = None
    targetLocations: Optional[List[str]] = None
    imageUrl: Optional[str] = None
    attachments: Optional[List[str]] = None
    maxInfluencers: Optional[int] = Field(None, ge=1, le=10)

# Collaboration Interest (Influencer Applications)
class InterestStatus(str, Enum):
    pending = "pending"      # Başvuru yapıldı
    approved = "approved"    # Admin onayladı
    rejected = "rejected"    # Admin reddetti
    withdrawn = "withdrawn"  # Influencer geri çekti

class CollaborationInterest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    collaborationId: str
    influencerId: str  # User ID of influencer
    
    # Application details
    message: Optional[str] = None  # Influencer'ın mesajı
    proposedDelivery: Optional[datetime] = None  # Önerdiği teslimat tarihi
    proposedBudget: Optional[float] = None  # Önerdiği ücret
    portfolio: List[str] = []  # Portfolio linkler
    
    # Status
    status: InterestStatus = InterestStatus.pending
    
    # Admin responses
    adminResponse: Optional[str] = None
    adminNotes: Optional[str] = None
    rejectionReason: Optional[str] = None
    
    # Dates
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    respondedAt: Optional[datetime] = None

class CollaborationInterestCreate(BaseModel):
    collaborationId: str
    message: Optional[str] = None
    proposedDelivery: Optional[datetime] = None
    proposedBudget: Optional[float] = Field(None, ge=0)
    portfolio: List[str] = []

class CollaborationInterestUpdate(BaseModel):
    message: Optional[str] = None
    proposedDelivery: Optional[datetime] = None
    proposedBudget: Optional[float] = Field(None, ge=0)
    portfolio: Optional[List[str]] = None
    status: Optional[InterestStatus] = None
    adminResponse: Optional[str] = None
    adminNotes: Optional[str] = None
    rejectionReason: Optional[str] = None


# Partner Request Management
class PartnerRequestCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    category: PartnerRequestCategory
    priority: TicketPriority = TicketPriority.medium
    budget: Optional[str] = Field(None, max_length=50)
    deadline: Optional[datetime] = None


class PartnerRequest(PartnerRequestCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    requestNumber: str = Field(default_factory=lambda: f"REQ-{uuid.uuid4().hex[:8].upper()}")
    partnerId: str  # User ID
    status: TicketStatus = TicketStatus.open
    assignedTo: Optional[str] = None  # Admin/team member ID
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    resolvedAt: Optional[datetime] = None


class PartnerRequestUpdate(BaseModel):
    status: TicketStatus
    assignedTo: Optional[str] = None
    resolutionNote: Optional[str] = None


# Notification Management
class NotificationCreate(BaseModel):
    userId: str
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    type: NotificationType = NotificationType.site
    actionUrl: Optional[str] = None


class Notification(NotificationCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    isRead: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    readAt: Optional[datetime] = None


# Company Logo Management  
class CompanyLogo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    companyName: str = Field(..., min_length=1, max_length=100)
    logoUrl: str = Field(..., min_length=1, max_length=500)
    website: Optional[str] = None
    category: Optional[str] = None
    isActive: bool = True
    isSuccess: bool = False
    order: int = 0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class CompanyLogoCreate(BaseModel):
    companyName: str = Field(..., min_length=1, max_length=100)
    logoUrl: str = Field(..., min_length=1, max_length=500)
    website: Optional[str] = None
    category: Optional[str] = None
    isActive: bool = True
    isSuccess: bool = False
    order: int = 0


class CompanyLogoUpdate(BaseModel):
    companyName: Optional[str] = None
    logoUrl: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    isActive: Optional[bool] = None
    isSuccess: Optional[bool] = None
    order: Optional[int] = None


# Team Member Management Models
class TeamMemberCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    imageUrl: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    expertise: List[str] = []
    order: int = 0

class TeamMemberModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: str
    department: str
    bio: Optional[str] = None
    imageUrl: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    expertise: List[str] = []
    order: int = 0
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    imageUrl: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    expertise: Optional[List[str]] = None
    order: Optional[int] = None
    isActive: Optional[bool] = None


# Testimonial Management Models
class TestimonialCreate(BaseModel):
    clientName: str = Field(..., min_length=1, max_length=100)
    clientPosition: Optional[str] = Field(None, max_length=100)
    clientCompany: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)
    rating: int = Field(..., ge=1, le=5)
    imageUrl: Optional[str] = None
    projectType: Optional[str] = Field(None, max_length=100)
    order: int = 0

class TestimonialModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clientName: str
    clientPosition: Optional[str] = None
    clientCompany: str
    content: str
    rating: int
    imageUrl: Optional[str] = None
    projectType: Optional[str] = None
    order: int = 0
    isActive: bool = True
    isFeatured: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None

class TestimonialUpdate(BaseModel):
    clientName: Optional[str] = Field(None, min_length=1, max_length=100)
    clientPosition: Optional[str] = Field(None, max_length=100)
    clientCompany: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    imageUrl: Optional[str] = None
    projectType: Optional[str] = Field(None, max_length=100)
    order: Optional[int] = None
    isActive: Optional[bool] = None
    isFeatured: Optional[bool] = None


# FAQ Management Models
class FAQCreate(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1, max_length=2000)
    category: str = Field(..., min_length=1, max_length=100)
    order: int = 0

class FAQModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    answer: str
    category: str
    order: int = 0
    isActive: bool = True
    viewCount: int = 0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None

class FAQUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1, max_length=500)
    answer: Optional[str] = Field(None, min_length=1, max_length=2000)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    order: Optional[int] = None
    isActive: Optional[bool] = None


# Notification System Models
class NotificationTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)  # 'new_collaboration', 'project_update', etc.
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=1000)
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class SystemNotification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(..., min_length=1, max_length=50)
    targetUsers: List[str] = []  # User IDs, empty list means all users
    isGlobal: bool = True
    isActive: bool = True
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str

class SystemNotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(..., min_length=1, max_length=50)
    targetUsers: List[str] = []
    isGlobal: bool = True
    isActive: bool = True
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None

class SystemNotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    targetUsers: Optional[List[str]] = None
    isGlobal: Optional[bool] = None
    isActive: Optional[bool] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None


# Newsletter System Models
class NewsletterSubscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: Optional[str] = None
    isActive: bool = True
    subscribedAt: datetime = Field(default_factory=datetime.utcnow)
    unsubscribedAt: Optional[datetime] = None
    source: str = "website"  # website, admin, api
    tags: List[str] = []
    preferences: dict = {}

class NewsletterSubscriberCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    source: str = "website"
    tags: List[str] = []

class NewsletterCampaign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    htmlContent: Optional[str] = None
    status: str = "draft"  # draft, scheduled, sent, cancelled
    scheduledAt: Optional[datetime] = None
    sentAt: Optional[datetime] = None
    totalRecipients: int = 0
    openCount: int = 0
    clickCount: int = 0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str

class LeadCapture(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None
    source: str = "contact_form"  # contact_form, landing_page, popup
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    isProcessed: bool = False
    processedAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)


# Performance & Analytics Models
class PageView(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    path: str
    referrer: Optional[str] = None
    userAgent: Optional[str] = None
    ipAddress: Optional[str] = None
    sessionId: Optional[str] = None
    userId: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    loadTime: Optional[float] = None
    device: Optional[str] = None
    browser: Optional[str] = None
    country: Optional[str] = None

class AnalyticsEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    eventType: str  # page_view, click, form_submit, download, etc.
    eventCategory: Optional[str] = None
    eventLabel: Optional[str] = None
    eventValue: Optional[float] = None
    userId: Optional[str] = None
    sessionId: Optional[str] = None
    metadata: dict = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ===== PAYMENT GATEWAY MODELS (IYZICO) =====

class PaymentStatus(str, Enum):
    pending = "pending"
    success = "success"
    failure = "failure"
    cancelled = "cancelled"

class PaymentCardModel(BaseModel):
    cardHolderName: str = Field(..., min_length=1, max_length=50)
    cardNumber: str = Field(..., min_length=13, max_length=19)
    expireMonth: str = Field(..., pattern="^(0[1-9]|1[0-2])$")
    expireYear: str = Field(..., pattern="^20[2-9][0-9]$")
    cvc: str = Field(..., min_length=3, max_length=4)
    registerCard: str = "0"

class PaymentBuyerModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = Field(..., min_length=1, max_length=50)
    surname: str = Field(..., min_length=1, max_length=50)
    gsmNumber: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    identityNumber: str = Field(..., min_length=11, max_length=11)
    registrationAddress: str = Field(..., min_length=1, max_length=200)
    ip: str = Field(..., min_length=7, max_length=15)
    city: str = Field(..., min_length=1, max_length=50)
    country: str = "Turkey"
    zipCode: str = Field(..., min_length=5, max_length=10)

class PaymentAddressModel(BaseModel):
    contactName: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=50)
    country: str = "Turkey"
    address: str = Field(..., min_length=1, max_length=200)
    zipCode: str = Field(..., min_length=5, max_length=10)

class PaymentBasketItemModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = Field(..., min_length=1, max_length=100)
    category1: str = Field(..., min_length=1, max_length=50)
    category2: Optional[str] = Field(None, max_length=50)
    itemType: str = "PHYSICAL"
    price: float = Field(..., gt=0)

class PaymentRequestModel(BaseModel):
    locale: str = "tr"
    conversationId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    price: float = Field(..., gt=0)
    paidPrice: float = Field(..., gt=0)
    currency: str = "TRY"
    installment: int = 1
    basketId: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    paymentChannel: str = "WEB"
    paymentGroup: str = "PRODUCT"
    paymentCard: PaymentCardModel
    buyer: PaymentBuyerModel
    shippingAddress: PaymentAddressModel
    billingAddress: PaymentAddressModel
    basketItems: List[PaymentBasketItemModel]

class PaymentTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversationId: str
    paymentId: Optional[str] = None
    basketId: str
    status: PaymentStatus = PaymentStatus.pending
    amount: float
    paidAmount: float
    currency: str = "TRY"
    installment: int = 1
    
    # Customer info
    buyerEmail: str
    buyerName: str
    buyerPhone: str
    
    # Response data
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    fraudStatus: Optional[int] = None
    binNumber: Optional[str] = None
    cardAssociation: Optional[str] = None
    cardFamily: Optional[str] = None
    cardType: Optional[str] = None
    
    # Timestamps
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Business context
    serviceType: Optional[str] = None  # "danışmanlık", "pr_paketi", etc.
    relatedEntityId: Optional[str] = None  # ticket_id, collaboration_id, etc.

class PaymentTransactionCreate(BaseModel):
    serviceType: str = Field(..., min_length=1, max_length=50)
    relatedEntityId: Optional[str] = None
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=200)


# ===== SMS GATEWAY MODELS (NETGSM) =====

class SMSStatus(str, Enum):
    pending = "pending"
    sent = "sent" 
    delivered = "delivered"
    failed = "failed"
    expired = "expired"

class SMSSendRequest(BaseModel):
    phoneNumber: str = Field(..., min_length=10, max_length=15)
    message: str = Field(..., min_length=1, max_length=1600)
    priority: str = Field("normal", pattern="^(low|normal|high)$")
    scheduleTime: Optional[datetime] = None

class BulkSMSRequest(BaseModel):
    recipients: List[str] = Field(..., min_length=1, max_length=1000)
    message: str = Field(..., min_length=1, max_length=1600)
    batchSize: int = Field(10, ge=1, le=100)
    priority: str = Field("normal", pattern="^(low|normal|high)$")
    scheduleTime: Optional[datetime] = None

class SMSTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    jobId: Optional[str] = None  # NetGSM job ID
    phoneNumber: str
    message: str
    status: SMSStatus = SMSStatus.pending
    
    # Delivery info
    sentAt: Optional[datetime] = None
    deliveredAt: Optional[datetime] = None
    errorMessage: Optional[str] = None
    errorCode: Optional[str] = None
    
    # Business context
    triggerType: str  # "customer_request_response", "influencer_notification", "general"
    relatedEntityId: Optional[str] = None  # ticket_id, collaboration_id, etc.
    relatedEntityType: Optional[str] = None  # "ticket", "collaboration", etc.
    
    # Retry logic
    retryCount: int = 0
    maxRetries: int = 3
    nextRetryAt: Optional[datetime] = None
    
    # Timestamps
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class SMSTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    triggerType: str = Field(..., min_length=1, max_length=50)
    template: str = Field(..., min_length=1, max_length=1600)
    variables: List[str] = []  # Available template variables
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class SMSTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    triggerType: str = Field(..., min_length=1, max_length=50)
    template: str = Field(..., min_length=1, max_length=1600)
    variables: List[str] = []

class SMSConfig(BaseModel):
    userCode: str
    password: str
    msgHeader: str
    apiUrl: str = "https://api.netgsm.com.tr/sms/send/get"
    isActive: bool = True
    maxDailyLimit: int = 1000
    currentDailyCount: int = 0
    lastResetDate: datetime = Field(default_factory=datetime.utcnow)


# ===== SERVICES MODELS (GALAKTIK HIZMETLER) =====

class ServiceType(str, Enum):
    ecommerce = "e-ticaret"
    social_media = "sosyal_medya"
    seo = "seo"
    content_marketing = "icerik_pazarlama"
    influencer_marketing = "influencer_pazarlama"
    branding = "marka_yonetimi"
    strategy = "strateji_danismanligi"
    other = "diger"

class ServiceFeature(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    included: bool = True

class Service(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    shortDescription: str = Field(..., min_length=1, max_length=300)
    serviceType: ServiceType
    price: Optional[float] = None  # null for "İletişime Geç" services
    currency: str = "TRY"
    duration: str = Field(..., min_length=1, max_length=100)  # "1-3 ay", "Sürekli", etc.
    
    # Visual elements
    icon: str = Field(..., min_length=1, max_length=100)  # emoji or icon class
    imageUrl: Optional[str] = None
    color: str = "#8B5CF6"  # hex color for card styling
    
    # Features and details
    features: List[ServiceFeature] = []
    deliverables: List[str] = []  # What client gets
    requirements: List[str] = []  # What client needs to provide
    
    # Process information
    processSteps: List[str] = []  # How we deliver the service
    timeline: str = Field(..., min_length=1, max_length=500)  # Detailed timeline
    
    # Display options
    isActive: bool = True
    isFeatured: bool = False  # Highlight on homepage
    showPrice: bool = True  # Show price or "İletişime Geç"
    order: int = 0  # Display order
    
    # SEO and marketing
    tags: List[str] = []
    metaTitle: Optional[str] = None
    metaDescription: Optional[str] = None
    
    # Statistics and performance
    popularityScore: int = 0  # For sorting popular services
    completedProjects: int = 0  # Number of completed projects
    
    # Creation and modification
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: Optional[str] = None  # Admin user ID

class ServiceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    shortDescription: str = Field(..., min_length=1, max_length=300)
    serviceType: ServiceType
    price: Optional[float] = None
    duration: str = Field(..., min_length=1, max_length=100)
    icon: str = Field(..., min_length=1, max_length=100)
    imageUrl: Optional[str] = None
    color: str = "#8B5CF6"
    features: List[ServiceFeature] = []
    deliverables: List[str] = []
    requirements: List[str] = []
    processSteps: List[str] = []
    timeline: str = Field(..., min_length=1, max_length=500)
    isActive: bool = True
    isFeatured: bool = False
    showPrice: bool = True
    order: int = 0
    tags: List[str] = []
    metaTitle: Optional[str] = None
    metaDescription: Optional[str] = None

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    shortDescription: Optional[str] = None
    serviceType: Optional[ServiceType] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    icon: Optional[str] = None
    imageUrl: Optional[str] = None
    color: Optional[str] = None
    features: Optional[List[ServiceFeature]] = None
    deliverables: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    processSteps: Optional[List[str]] = None
    timeline: Optional[str] = None
    isActive: Optional[bool] = None
    isFeatured: Optional[bool] = None
    showPrice: Optional[bool] = None
    order: Optional[int] = None
    tags: Optional[List[str]] = None
    metaTitle: Optional[str] = None
    metaDescription: Optional[str] = None
    popularityScore: Optional[int] = None
    completedProjects: Optional[int] = None