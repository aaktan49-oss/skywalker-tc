import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import get_password_hash
from models import AdminUser, COLLECTIONS, AdminRole
from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


async def create_admin_user():
    """Create initial admin user"""
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Check if admin already exists
        existing_admin = await db[COLLECTIONS['admin_users']].find_one(
            {"username": "admin"}
        )
        
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_data = AdminUser(
            username="admin",
            email="admin@skywalker.tc",
            password=get_password_hash("admin123"),  # Default password
            role=AdminRole.superadmin
        )
        
        result = await db[COLLECTIONS['admin_users']].insert_one(admin_data.dict())
        print(f"✅ Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: skywalker2025")
        print(f"Email: admin@skywalker.tc")
        print(f"Role: superadmin")
        print(f"ID: {admin_data.id}")
        
        # Create some default content
        default_contents = [
            {
                "key": "hero_title",
                "type": "text",
                "content": "Trendyol Galaksisinde Liderlik"
            },
            {
                "key": "hero_subtitle", 
                "type": "text",
                "content": "Karlılık odaklı danışmanlık ile firmanızın kazancını artırmayı hedefliyoruz. ROI odaklı stratejilerle e-ticaret imparatorluğunuzu kurun!"
            },
            {
                "key": "company_stats",
                "type": "object",
                "content": {
                    "projects": "50+",
                    "experience": "10+", 
                    "team": "15+"
                }
            }
        ]
        
        for content in default_contents:
            await db[COLLECTIONS['site_content']].update_one(
                {"key": content["key"]},
                {"$set": content},
                upsert=True
            )
        
        print(f"✅ Default site content created!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())