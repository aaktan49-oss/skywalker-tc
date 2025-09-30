#!/usr/bin/env python3
"""
Fix Demo Partner Account Approval
Updates the partner@demo.com account to be approved
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def fix_partner_approval():
    """Update partner@demo.com to be approved"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Find and update the partner account
        result = await db.users.update_one(
            {"email": "partner@demo.com", "role": "partner"},
            {"$set": {"isApproved": True}}
        )
        
        if result.matched_count > 0:
            print("✅ Successfully updated partner@demo.com to be approved")
            
            # Verify the update
            partner = await db.users.find_one({"email": "partner@demo.com"})
            if partner:
                print(f"   Partner approval status: {partner.get('isApproved', False)}")
                print(f"   Partner role: {partner.get('role')}")
                print(f"   Partner company: {partner.get('company')}")
            else:
                print("❌ Partner account not found after update")
        else:
            print("❌ Partner account not found or not updated")
            
            # Check if account exists
            partner = await db.users.find_one({"email": "partner@demo.com"})
            if partner:
                print(f"   Found partner but update failed. Current approval: {partner.get('isApproved', False)}")
            else:
                print("   Partner account does not exist")
    
    except Exception as e:
        print(f"❌ Error updating partner account: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_partner_approval())