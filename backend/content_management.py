from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import (
    SiteContentItem, SiteContentCreate, SiteContentUpdate, SiteContentType,
    NewsArticle, NewsArticleCreate, NewsArticleUpdate, NewsCategory,
    CompanyProject, CompanyProjectCreate, CompanyProjectUpdate, ProjectStatus,
    SiteSettings, SiteSettingsUpdate,
    TeamMemberModel, TeamMemberCreate, TeamMemberUpdate,
    TestimonialModel, TestimonialCreate, TestimonialUpdate,
    FAQModel, FAQCreate, FAQUpdate,
    COLLECTIONS
)
from auth import get_admin_user
from portal_auth import get_current_user
import uuid

router = APIRouter(prefix="/api/content", tags=["Content Management"])

# Database will be injected from server.py
db = None

def set_database(database):
    global db
    db = database

async def get_database() -> AsyncIOMotorDatabase:
    return db

async def get_current_admin_user(credentials = Depends(get_current_user)):
    """Get current admin user with proper role validation"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if credentials.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return credentials

# Site Content Management Endpoints
@router.get("/site-content", response_model=List[SiteContentItem])
async def get_site_content(
    section: Optional[SiteContentType] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get site content items (public endpoint)"""
    try:
        filter_query = {"isActive": True}
        if section:
            filter_query["section"] = section
        
        cursor = db[COLLECTIONS['site_content']].find(filter_query).sort("order", 1)
        content_items = await cursor.to_list(length=None)
        
        return [SiteContentItem(**item) for item in content_items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site content: {str(e)}")

@router.post("/admin/site-content", response_model=dict)
async def create_site_content(
    content_data: SiteContentCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new site content item (admin only)"""
    try:
        # Check if content with same section and key already exists
        existing_content = await db[COLLECTIONS['site_content']].find_one({
            "section": content_data.section,
            "key": content_data.key
        })
        
        if existing_content:
            raise HTTPException(
                status_code=400, 
                detail=f"Content with key '{content_data.key}' already exists in section '{content_data.section}'"
            )
        
        content_item = SiteContentItem(
            **content_data.dict(),
            updatedBy=current_admin.id
        )
        
        content_dict = content_item.dict()
        await db[COLLECTIONS['site_content']].insert_one(content_dict)
        
        return {"success": True, "message": "Site content created successfully", "id": content_item.id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating site content: {str(e)}")

@router.put("/admin/site-content/{content_id}", response_model=dict)
async def update_site_content(
    content_id: str,
    content_data: SiteContentUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update site content item (admin only)"""
    try:
        # Check if content exists
        existing_content = await db[COLLECTIONS['site_content']].find_one({"id": content_id})
        if not existing_content:
            raise HTTPException(status_code=404, detail="Content item not found")
        
        update_data = {k: v for k, v in content_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        update_data["updatedBy"] = current_admin.id
        
        await db[COLLECTIONS['site_content']].update_one(
            {"id": content_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Site content updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating site content: {str(e)}")

@router.delete("/admin/site-content/{content_id}", response_model=dict)
async def delete_site_content(
    content_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete site content item (admin only)"""
    try:
        result = await db[COLLECTIONS['site_content']].delete_one({"id": content_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Content item not found")
        
        return {"success": True, "message": "Site content deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting site content: {str(e)}")

# News Management Endpoints
@router.get("/news", response_model=List[NewsArticle])
async def get_news_articles(
    category: Optional[NewsCategory] = None,
    limit: int = Query(default=10, le=50),
    skip: int = Query(default=0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get published news articles (public endpoint)"""
    try:
        filter_query = {"isPublished": True}
        if category:
            filter_query["category"] = category
        
        cursor = db[COLLECTIONS['news_articles']].find(filter_query).sort("publishedAt", -1).skip(skip).limit(limit)
        articles = await cursor.to_list(length=None)
        
        return [NewsArticle(**article) for article in articles]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news articles: {str(e)}")

@router.get("/news/{article_id}", response_model=NewsArticle)
async def get_news_article(
    article_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single news article by ID (public endpoint)"""
    try:
        article = await db[COLLECTIONS['news_articles']].find_one({
            "id": article_id,
            "isPublished": True
        })
        
        if not article:
            raise HTTPException(status_code=404, detail="News article not found")
        
        return NewsArticle(**article)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news article: {str(e)}")

@router.post("/admin/news", response_model=dict)
async def create_news_article(
    article_data: NewsArticleCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new news article (admin only)"""
    try:
        article = NewsArticle(
            **article_data.dict(),
            createdBy=current_admin.id
        )
        
        article_dict = article.dict()
        await db[COLLECTIONS['news_articles']].insert_one(article_dict)
        
        return {"success": True, "message": "News article created successfully", "id": article.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating news article: {str(e)}")

@router.put("/admin/news/{article_id}", response_model=dict)
async def update_news_article(
    article_id: str,
    article_data: NewsArticleUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update news article (admin only)"""
    try:
        # Check if article exists
        existing_article = await db[COLLECTIONS['news_articles']].find_one({"id": article_id})
        if not existing_article:
            raise HTTPException(status_code=404, detail="News article not found")
        
        update_data = {k: v for k, v in article_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['news_articles']].update_one(
            {"id": article_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "News article updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating news article: {str(e)}")

@router.delete("/admin/news/{article_id}", response_model=dict)
async def delete_news_article(
    article_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete news article (admin only)"""
    try:
        result = await db[COLLECTIONS['news_articles']].delete_one({"id": article_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="News article not found")
        
        return {"success": True, "message": "News article deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting news article: {str(e)}")

# Company Projects Endpoints
@router.get("/projects", response_model=List[CompanyProject])
async def get_company_projects(
    status: Optional[ProjectStatus] = None,
    category: Optional[str] = None,
    limit: int = Query(default=10, le=50),
    skip: int = Query(default=0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get public company projects (public endpoint)"""
    try:
        filter_query = {"isPublic": True}
        if status:
            filter_query["status"] = status
        if category:
            filter_query["category"] = category
        
        cursor = db[COLLECTIONS['company_projects']].find(filter_query).sort("endDate", -1).skip(skip).limit(limit)
        projects = await cursor.to_list(length=None)
        
        return [CompanyProject(**project) for project in projects]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company projects: {str(e)}")

@router.get("/projects/{project_id}", response_model=CompanyProject)
async def get_company_project(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single company project by ID (public endpoint)"""
    try:
        project = await db[COLLECTIONS['company_projects']].find_one({
            "id": project_id,
            "isPublic": True
        })
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return CompanyProject(**project)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")

@router.post("/admin/projects", response_model=dict)
async def create_company_project(
    project_data: CompanyProjectCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new company project (admin only)"""
    try:
        project = CompanyProject(
            **project_data.dict(),
            createdBy=current_admin.id
        )
        
        project_dict = project.dict()
        await db[COLLECTIONS['company_projects']].insert_one(project_dict)
        
        return {"success": True, "message": "Company project created successfully", "id": project.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating company project: {str(e)}")

@router.put("/admin/projects/{project_id}", response_model=dict)
async def update_company_project(
    project_id: str,
    project_data: CompanyProjectUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update company project (admin only)"""
    try:
        # Check if project exists
        existing_project = await db[COLLECTIONS['company_projects']].find_one({"id": project_id})
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = {k: v for k, v in project_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['company_projects']].update_one(
            {"id": project_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Company project updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating company project: {str(e)}")

@router.delete("/admin/projects/{project_id}", response_model=dict)
async def delete_company_project(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete company project (admin only)"""
    try:
        result = await db[COLLECTIONS['company_projects']].delete_one({"id": project_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"success": True, "message": "Company project deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting company project: {str(e)}")

# Admin endpoints for all content
@router.get("/admin/news", response_model=List[NewsArticle])
async def get_all_news_articles_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all news articles including unpublished (admin only)"""
    try:
        cursor = db[COLLECTIONS['news_articles']].find({}).sort("createdAt", -1)
        articles = await cursor.to_list(length=None)
        
        return [NewsArticle(**article) for article in articles]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news articles: {str(e)}")

@router.get("/admin/projects", response_model=List[CompanyProject])
async def get_all_company_projects_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all company projects including private ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['company_projects']].find({}).sort("createdAt", -1)
        projects = await cursor.to_list(length=None)
        
        return [CompanyProject(**project) for project in projects]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company projects: {str(e)}")

# Site Settings Management
@router.get("/site-settings", response_model=dict)
async def get_site_settings(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get site settings (public endpoint)"""
    try:
        settings = await db[COLLECTIONS['site_settings']].find_one({"isActive": True})
        
        if not settings:
            # Return default settings if none exist
            default_settings = SiteSettings()
            return default_settings.dict()
        
        return settings
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site settings: {str(e)}")

@router.put("/admin/site-settings", response_model=dict)
async def update_site_settings(
    settings_data: SiteSettingsUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update site settings (admin only)"""
    try:
        # Get existing settings or create new
        existing_settings = await db[COLLECTIONS['site_settings']].find_one({"isActive": True})
        
        update_data = {k: v for k, v in settings_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        update_data["updatedBy"] = current_admin.id
        
        if existing_settings:
            # Update existing
            await db[COLLECTIONS['site_settings']].update_one(
                {"id": existing_settings["id"]},
                {"$set": update_data}
            )
        else:
            # Create new
            new_settings = SiteSettings(**update_data, updatedBy=current_admin.id)
            settings_dict = new_settings.dict()
            await db[COLLECTIONS['site_settings']].insert_one(settings_dict)
        
        return {"success": True, "message": "Site settings updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating site settings: {str(e)}")

@router.get("/admin/site-content", response_model=List[SiteContentItem])
async def get_all_site_content_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all site content including inactive items (admin only)"""
    try:
        cursor = db[COLLECTIONS['site_content']].find({}).sort([("section", 1), ("order", 1)])
        content_items = await cursor.to_list(length=None)
        
        return [SiteContentItem(**item) for item in content_items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site content: {str(e)}")

# Team Member Management Endpoints
@router.get("/team", response_model=List[dict])
async def get_team_members(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get active team members (public endpoint)"""
    try:
        cursor = db[COLLECTIONS['team_members_cms']].find({"isActive": True}).sort("order", 1)
        team_members = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for member in team_members:
            if '_id' in member:
                del member['_id']
        
        return team_members
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team members: {str(e)}")

@router.post("/admin/team", response_model=dict)
async def create_team_member(
    member_data: TeamMemberCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new team member (admin only)"""
    try:
        member = TeamMemberModel(
            **member_data.dict(),
            createdBy=current_admin.id
        )
        
        member_dict = member.dict()
        await db[COLLECTIONS['team_members_cms']].insert_one(member_dict)
        
        return {"success": True, "message": "Team member created successfully", "id": member.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating team member: {str(e)}")

@router.get("/admin/team", response_model=List[dict])
async def get_all_team_members_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all team members including inactive ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['team_members_cms']].find({}).sort("order", 1)
        team_members = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for member in team_members:
            if '_id' in member:
                del member['_id']
        
        return team_members
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team members: {str(e)}")

@router.put("/admin/team/{member_id}", response_model=dict)
async def update_team_member(
    member_id: str,
    member_data: TeamMemberUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update team member (admin only)"""
    try:
        existing_member = await db[COLLECTIONS['team_members_cms']].find_one({"id": member_id})
        if not existing_member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        update_data = {k: v for k, v in member_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['team_members_cms']].update_one(
            {"id": member_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Team member updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating team member: {str(e)}")

@router.delete("/admin/team/{member_id}", response_model=dict)
async def delete_team_member(
    member_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete team member (admin only)"""
    try:
        result = await db[COLLECTIONS['team_members_cms']].delete_one({"id": member_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        return {"success": True, "message": "Team member deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting team member: {str(e)}")

# Testimonials Management Endpoints
@router.get("/testimonials", response_model=List[dict])
async def get_testimonials(
    limit: int = Query(default=10, le=50),
    featured_only: bool = Query(default=False),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get active testimonials (public endpoint)"""
    try:
        filter_query = {"isActive": True}
        if featured_only:
            filter_query["isFeatured"] = True
        
        cursor = db[COLLECTIONS['testimonials']].find(filter_query).sort("order", 1).limit(limit)
        testimonials = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for testimonial in testimonials:
            if '_id' in testimonial:
                del testimonial['_id']
        
        return testimonials
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching testimonials: {str(e)}")

@router.post("/admin/testimonials", response_model=dict)
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new testimonial (admin only)"""
    try:
        testimonial = TestimonialModel(
            **testimonial_data.dict(),
            createdBy=current_admin.id
        )
        
        testimonial_dict = testimonial.dict()
        await db[COLLECTIONS['testimonials']].insert_one(testimonial_dict)
        
        return {"success": True, "message": "Testimonial created successfully", "id": testimonial.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating testimonial: {str(e)}")

@router.get("/admin/testimonials", response_model=List[dict])
async def get_all_testimonials_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all testimonials including inactive ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['testimonials']].find({}).sort("order", 1)
        testimonials = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for testimonial in testimonials:
            if '_id' in testimonial:
                del testimonial['_id']
        
        return testimonials
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching testimonials: {str(e)}")

@router.put("/admin/testimonials/{testimonial_id}", response_model=dict)
async def update_testimonial(
    testimonial_id: str,
    testimonial_data: TestimonialUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update testimonial (admin only)"""
    try:
        existing_testimonial = await db[COLLECTIONS['testimonials']].find_one({"id": testimonial_id})
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        update_data = {k: v for k, v in testimonial_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['testimonials']].update_one(
            {"id": testimonial_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Testimonial updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating testimonial: {str(e)}")

@router.delete("/admin/testimonials/{testimonial_id}", response_model=dict)
async def delete_testimonial(
    testimonial_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete testimonial (admin only)"""
    try:
        result = await db[COLLECTIONS['testimonials']].delete_one({"id": testimonial_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        return {"success": True, "message": "Testimonial deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting testimonial: {str(e)}")

# FAQ Management Endpoints  
@router.get("/faqs", response_model=List[dict])
async def get_faqs(
    category: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get active FAQs (public endpoint)"""
    try:
        filter_query = {"isActive": True}
        if category:
            filter_query["category"] = category
        
        cursor = db[COLLECTIONS['faqs']].find(filter_query).sort("order", 1)
        faqs = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for faq in faqs:
            if '_id' in faq:
                del faq['_id']
        
        return faqs
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching FAQs: {str(e)}")

@router.post("/admin/faqs", response_model=dict)
async def create_faq(
    faq_data: FAQCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new FAQ (admin only)"""
    try:
        faq = FAQModel(
            **faq_data.dict(),
            createdBy=current_admin.id
        )
        
        faq_dict = faq.dict()
        await db[COLLECTIONS['faqs']].insert_one(faq_dict)
        
        return {"success": True, "message": "FAQ created successfully", "id": faq.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating FAQ: {str(e)}")

@router.get("/admin/faqs", response_model=List[dict])
async def get_all_faqs_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all FAQs including inactive ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['faqs']].find({}).sort([("category", 1), ("order", 1)])
        faqs = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for faq in faqs:
            if '_id' in faq:
                del faq['_id']
        
        return faqs
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching FAQs: {str(e)}")

@router.put("/admin/faqs/{faq_id}", response_model=dict)
async def update_faq(
    faq_id: str,
    faq_data: FAQUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update FAQ (admin only)"""
    try:
        existing_faq = await db[COLLECTIONS['faqs']].find_one({"id": faq_id})
        if not existing_faq:
            raise HTTPException(status_code=404, detail="FAQ not found")
        
        update_data = {k: v for k, v in faq_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['faqs']].update_one(
            {"id": faq_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "FAQ updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating FAQ: {str(e)}")

@router.delete("/admin/faqs/{faq_id}", response_model=dict)
async def delete_faq(
    faq_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete FAQ (admin only)"""
    try:
        result = await db[COLLECTIONS['faqs']].delete_one({"id": faq_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="FAQ not found")
        
        return {"success": True, "message": "FAQ deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting FAQ: {str(e)}")

# System Notifications Endpoints
@router.get("/notifications", response_model=List[dict])
async def get_system_notifications(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get active system notifications (public endpoint)"""
    try:
        current_time = datetime.utcnow()
        filter_query = {
            "isActive": True,
            "$or": [
                {"startDate": {"$lte": current_time}},
                {"startDate": None}
            ],
            "$or": [
                {"endDate": {"$gte": current_time}},
                {"endDate": None}
            ]
        }
        
        cursor = db[COLLECTIONS['system_notifications']].find(filter_query).sort("createdAt", -1)
        notifications = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for notification in notifications:
            if '_id' in notification:
                del notification['_id']
        
        return notifications
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.post("/admin/notifications", response_model=dict)
async def create_system_notification(
    notification_data: dict,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new system notification (admin only)"""
    try:
        from models import SystemNotification
        
        notification = SystemNotification(
            **notification_data,
            createdBy=current_admin.id
        )
        
        notification_dict = notification.dict()
        await db[COLLECTIONS['system_notifications']].insert_one(notification_dict)
        
        return {"success": True, "message": "System notification created successfully", "id": notification.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating system notification: {str(e)}")

@router.get("/admin/notifications", response_model=List[dict])
async def get_all_system_notifications_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all system notifications including inactive ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['system_notifications']].find({}).sort("createdAt", -1)
        notifications = await cursor.to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for notification in notifications:
            if '_id' in notification:
                del notification['_id']
        
        return notifications
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching system notifications: {str(e)}")

@router.put("/admin/notifications/{notification_id}", response_model=dict)
async def update_system_notification(
    notification_id: str,
    notification_data: dict,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update system notification (admin only)"""
    try:
        existing_notification = await db[COLLECTIONS['system_notifications']].find_one({"id": notification_id})
        if not existing_notification:
            raise HTTPException(status_code=404, detail="System notification not found")
        
        update_data = {k: v for k, v in notification_data.items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['system_notifications']].update_one(
            {"id": notification_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "System notification updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating system notification: {str(e)}")

@router.delete("/admin/notifications/{notification_id}", response_model=dict)
async def delete_system_notification(
    notification_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete system notification (admin only)"""
    try:
        result = await db[COLLECTIONS['system_notifications']].delete_one({"id": notification_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="System notification not found")
        
        return {"success": True, "message": "System notification deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting system notification: {str(e)}")