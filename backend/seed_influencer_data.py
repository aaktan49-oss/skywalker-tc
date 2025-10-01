"""
Seed script for Influencer Applications - Sample data for testing
"""

import asyncio
import motor.motor_asyncio
import os
from datetime import datetime
import uuid

async def seed_influencer_applications():
    # Database connection
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    db = client[os.getenv("DB_NAME", "test_database")]
    
    # Sample influencer applications
    applications_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "Ayşe Gürel",
            "email": "ayse.gurel@instagram.com",
            "phone": "+90 555 123 45 67",
            "instagram": "@ayse_beauty_guru",
            "followers": 150000,
            "engagement_rate": 4.2,
            "niche": "Beauty & Fashion",
            "location": "İstanbul",
            "age": 26,
            "bio": "Beauty content creator with 150K followers. Specialist in skincare reviews and makeup tutorials.",
            "collaboration_types": ["Product Review", "Story Mention", "Reels"],
            "rate_per_post": 2500,
            "rate_per_story": 800,
            "rate_per_reel": 3500,
            "status": "pending",
            "applied_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "portfolio_links": [
                "https://instagram.com/p/example1",
                "https://instagram.com/p/example2"
            ],
            "previous_brands": ["MAC Cosmetics", "Sephora", "L'Oreal"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mehmet Özkan",
            "email": "mehmet.tech@gmail.com",
            "phone": "+90 532 987 65 43",
            "instagram": "@mehmet_tech_review",
            "followers": 89000,
            "engagement_rate": 5.1,
            "niche": "Technology & Gadgets",
            "location": "Ankara",
            "age": 29,
            "bio": "Tech reviewer focusing on smartphones, laptops and gaming equipment. High engagement audience.",
            "collaboration_types": ["Product Review", "Unboxing", "Tutorial"],
            "rate_per_post": 1800,
            "rate_per_story": 600,
            "rate_per_reel": 2200,
            "status": "approved",
            "applied_at": datetime.utcnow(),
            "approved_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "portfolio_links": [
                "https://instagram.com/p/tech_review1",
                "https://youtube.com/watch?v=example"
            ],
            "previous_brands": ["Samsung", "Apple", "Xiaomi", "MSI"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Zeynep Kaya",
            "email": "zeynep.lifestyle@hotmail.com", 
            "phone": "+90 505 456 78 90",
            "instagram": "@zeynep_life_style",
            "followers": 67000,
            "engagement_rate": 3.8,
            "niche": "Lifestyle & Travel",
            "location": "İzmir",
            "age": 24,
            "bio": "Lifestyle blogger sharing travel experiences, fashion tips and daily life content.",
            "collaboration_types": ["Story Mention", "Reels", "IGTV"],
            "rate_per_post": 1200,
            "rate_per_story": 400,
            "rate_per_reel": 1800,
            "status": "pending",
            "applied_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "portfolio_links": [
                "https://instagram.com/p/lifestyle1",
                "https://instagram.com/p/travel1"
            ],
            "previous_brands": ["Zara", "Mango", "Turkish Airlines"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Emre Fitness",
            "email": "emre.fitness@outlook.com",
            "phone": "+90 544 321 98 76",
            "instagram": "@emre_fitness_coach",
            "followers": 234000,
            "engagement_rate": 6.2,
            "niche": "Fitness & Health",
            "location": "Bursa",
            "age": 31,
            "bio": "Certified fitness trainer and nutrition expert. High engagement with fitness enthusiasts.",
            "collaboration_types": ["Product Review", "Story Mention", "Live Session"],
            "rate_per_post": 4000,
            "rate_per_story": 1200,
            "rate_per_reel": 5500,
            "status": "approved",
            "applied_at": datetime.utcnow(),
            "approved_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "portfolio_links": [
                "https://instagram.com/p/workout1",
                "https://instagram.com/p/nutrition_tip"
            ],
            "previous_brands": ["Protein World", "Nike", "Adidas", "MyProtein"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Selin Mutfak",
            "email": "selin.yemek@gmail.com",
            "phone": "+90 533 654 32 10",
            "instagram": "@selin_mutfak_sirrlari",
            "followers": 45000,
            "engagement_rate": 7.1,
            "niche": "Food & Cooking",
            "location": "Antalya",
            "age": 28,
            "bio": "Home chef sharing traditional Turkish recipes and cooking tips. Very engaged audience.",
            "collaboration_types": ["Recipe Creation", "Story Mention", "Reels"],
            "rate_per_post": 900,
            "rate_per_story": 300,
            "rate_per_reel": 1300,
            "status": "rejected",
            "applied_at": datetime.utcnow(),
            "rejected_at": datetime.utcnow(),
            "rejection_reason": "Niche mismatch with current campaign requirements",
            "created_at": datetime.utcnow(),
            "portfolio_links": [
                "https://instagram.com/p/baklava_recipe",
                "https://instagram.com/p/turkish_breakfast"
            ],
            "previous_brands": ["Ülker", "Pınar", "Migros"]
        }
    ]
    
    # Sample collaboration requests
    collaborations_data = [
        {
            "id": str(uuid.uuid4()),
            "title": "Beauty Brand Summer Campaign",
            "description": "Looking for beauty influencers for summer skincare campaign. Product gifting and payment included.",
            "category": "Beauty & Fashion",
            "budget_min": 15000,
            "budget_max": 35000,
            "currency": "TRY",
            "requirements": [
                "Minimum 50K followers",
                "Beauty/skincare niche",
                "Turkey-based",
                "High engagement rate (>3%)"
            ],
            "deliverables": [
                "2 feed posts",
                "5 story mentions", 
                "1 reel video"
            ],
            "deadline": "2024-11-15",
            "status": "active",
            "created_by": "admin",
            "applicants": ["ayse.gurel@instagram.com", "zeynep.lifestyle@hotmail.com"],
            "applicant_count": 8,
            "approved_count": 2,
            "created_at": datetime.utcnow(),
            "contact_email": "campaigns@skywalker.tc"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Tech Product Launch",
            "description": "New smartphone launch campaign. Looking for tech reviewers with authentic audience.",
            "category": "Technology",
            "budget_min": 25000,
            "budget_max": 50000,
            "currency": "TRY", 
            "requirements": [
                "Tech review focus",
                "Minimum 75K followers",
                "Male audience 65%+",
                "Previous tech brand collaborations"
            ],
            "deliverables": [
                "Unboxing video",
                "Detailed review post",
                "Story highlights"
            ],
            "deadline": "2024-10-30",
            "status": "active",
            "created_by": "admin",
            "applicants": ["mehmet.tech@gmail.com"],
            "applicant_count": 3,
            "approved_count": 1,
            "created_at": datetime.utcnow(),
            "contact_email": "tech@skywalker.tc"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Fitness Equipment Promotion",
            "description": "Home fitness equipment brand looking for fitness influencers for Q4 campaign.",
            "category": "Fitness & Health",
            "budget_min": 20000,
            "budget_max": 40000,
            "currency": "TRY",
            "requirements": [
                "Fitness/health niche",
                "Minimum 100K followers",
                "Workout content regular",
                "Professional trainer preferred"
            ],
            "deliverables": [
                "Equipment demo video",
                "Workout routine reel",
                "Story series"
            ],
            "deadline": "2024-12-01",
            "status": "active",
            "created_by": "admin",
            "applicants": ["emre.fitness@outlook.com"],
            "applicant_count": 4,
            "approved_count": 2,
            "created_at": datetime.utcnow(),
            "contact_email": "fitness@skywalker.tc"
        }
    ]
    
    try:
        # Clear existing data
        await db.influencer_applications.delete_many({})
        await db.collaboration_requests.delete_many({})
        print("Cleared existing data")
        
        # Insert influencer applications
        for app_data in applications_data:
            await db.influencer_applications.insert_one(app_data)
            print(f"✅ Added influencer: {app_data['name']} (@{app_data['instagram']})")
        
        # Insert collaboration requests
        for collab_data in collaborations_data:
            await db.collaboration_requests.insert_one(collab_data)
            print(f"✅ Added collaboration: {collab_data['title']}")
        
        print(f"\n🎉 Successfully seeded:")
        print(f"📱 {len(applications_data)} influencer applications")
        print(f"🤝 {len(collaborations_data)} collaboration requests")
        
        # Show summary
        total_apps = await db.influencer_applications.count_documents({})
        pending_apps = await db.influencer_applications.count_documents({"status": "pending"})
        approved_apps = await db.influencer_applications.count_documents({"status": "approved"})
        
        print(f"\n📊 Current Status:")
        print(f"   Total applications: {total_apps}")
        print(f"   Pending: {pending_apps}")
        print(f"   Approved: {approved_apps}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_influencer_applications())