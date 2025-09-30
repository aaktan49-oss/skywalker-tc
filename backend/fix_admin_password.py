import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import get_password_hash
from models import COLLECTIONS
from dotenv import load_dotenv
import os

load_dotenv('.env')

async def fix_admin_password():
    """Fix admin password with proper hashing"""
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Generate new password hash using our auth module
        new_password_hash = get_password_hash("admin123")
        print(f"Generated new hash: {new_password_hash[:20]}...")
        
        # Update admin password
        result = await db[COLLECTIONS['admin_users']].update_one(
            {"username": "admin"},
            {"$set": {"password": new_password_hash}}
        )
        
        if result.modified_count > 0:
            print("✅ Admin password updated successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("❌ Failed to update admin password")
        
    except Exception as e:
        print(f"❌ Error fixing admin password: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin_password())