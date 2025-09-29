import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import get_password_hash
from models import COLLECTIONS
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
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
        
        # Create admin user with simpler approach
        import bcrypt
        password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
        
        admin_data = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@skywalker.tc",
            "password": password_hash,
            "role": "superadmin",
            "createdAt": datetime.utcnow(),
            "lastLogin": None
        }
        
        result = await db[COLLECTIONS['admin_users']].insert_one(admin_data)
        print(f"✅ Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Email: admin@skywalker.tc")
        print(f"Role: superadmin")
        print(f"ID: {admin_data['id']}")
        
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