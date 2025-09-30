import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models import COLLECTIONS
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
import bcrypt

load_dotenv('.env')

async def recreate_admin():
    """Recreate admin user with direct bcrypt approach"""
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Remove existing admin
        await db[COLLECTIONS['admin_users']].delete_one({"username": "admin"})
        print("✅ Removed existing admin user")
        
        # Create new password hash using bcrypt directly
        password = "admin123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create admin user
        admin_data = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@skywalker.tc",
            "password": password_hash,
            "role": "superadmin",
            "createdAt": datetime.utcnow(),
            "lastLogin": None
        }
        
        await db[COLLECTIONS['admin_users']].insert_one(admin_data)
        
        print("✅ Admin user recreated successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Hash: {password_hash[:30]}...")
        
        # Test the hash
        test_result = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        print(f"Password verification test: {test_result}")
        
    except Exception as e:
        print(f"❌ Error recreating admin user: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(recreate_admin())