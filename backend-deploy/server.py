from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, List
import os
import logging
import uuid
import math
import bcrypt
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Configuration
SECRET_KEY = "skywalker_jwt_secret_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

# Models
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    createdAt: datetime
    lastLogin: Optional[datetime] = None

class ApiResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[dict] = None

# MongoDB Collections
COLLECTIONS = {
    'admin_users': 'admin_users',
    'influencer_applications': 'influencer_applications',
    'contact_messages': 'contact_messages',
    'customers': 'customers',
    'tickets': 'tickets',
    'team_members': 'team_members',
    'site_content': 'site_content'
}

# FastAPI app
app = FastAPI(title="Skywalker.tc API", version="1.0.0")

# CORS
origins = [
    "https://aaktan49-oss.github.io",
    "https://aaktan49-oss.github.io/skywalker-tc",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb+srv://admin:admin123@cluster0.mongodb.net/skywalker?retryWrites=true&w=majority')
client = AsyncIOMotorClient(mongo_url)
db = client.skywalker

# Auth functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logging.error(f"Password verification error: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current authenticated user from token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "username": username,
            "user_id": user_id,
            "role": role
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Routes
@app.get("/")
async def root():
    return {"message": "Skywalker.tc API - May the Force be with you!", "status": "active"}

@app.get("/api")
async def api_root():
    return {"message": "Skywalker.tc API - May the Force be with you!", "version": "1.0.0"}

@app.post("/api/admin/login")
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

@app.get("/api/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(get_current_user)):
    """Get admin dashboard statistics"""
    try:
        # Get counts
        influencer_count = await db[COLLECTIONS['influencer_applications']].count_documents({})
        contact_count = await db[COLLECTIONS['contact_messages']].count_documents({})
        customer_count = await db[COLLECTIONS['customers']].count_documents({})
        ticket_count = await db[COLLECTIONS['tickets']].count_documents({})
        
        return {
            "success": True,
            "data": {
                "influencers": {
                    "total": influencer_count,
                    "pending": 0,
                    "approved": influencer_count
                },
                "contacts": {
                    "total": contact_count,
                    "new": 0,
                    "replied": contact_count
                },
                "tickets": {
                    "total": ticket_count,
                    "open": 0,
                    "in_progress": 0,
                    "resolved": ticket_count,
                    "recent": 0
                },
                "customers": {
                    "total": customer_count,
                    "active": customer_count
                }
            }
        }
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to load dashboard")

@app.get("/api/team")
async def get_team():
    """Get team members"""
    try:
        # Sample team data with Star Wars characters
        team_data = [
            {
                "id": str(uuid.uuid4()),
                "name": "Luke Skywalker",
                "title": "Jedi Master & CEO",
                "description": "Galaksinin en deneyimli Jedi ustası. E-ticaret güçlerini kullanarak işletmeleri zafere götürür.",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face",
                "character_type": "jedi"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Princess Leia",
                "title": "Marketing Stratejisti",
                "description": "İsyan Liderliği deneyimi ile dijital pazarlama stratejilerinde uzman. Marka direncini artırır.",
                "image_url": "https://images.unsplash.com/photo-1494790108755-2616b612b359?w=300&h=300&fit=crop&crop=face",
                "character_type": "leader"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Han Solo",
                "title": "E-ticaret Pilotu",
                "description": "Millennium Falcon hızında e-ticaret çözümleri sunar. En zorlu projelerde bile başarıyı getirir.",
                "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face",
                "character_type": "pilot"
            }
        ]
        
        return {
            "success": True,
            "data": team_data
        }
    except Exception as e:
        logging.error(f"Get team error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve team")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)