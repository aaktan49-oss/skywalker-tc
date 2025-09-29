import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models import COLLECTIONS, TeamMember
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


async def create_team_members():
    """Create Star Wars themed team members"""
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Check if team members already exist
        existing_count = await db[COLLECTIONS['team_members']].count_documents({})
        
        if existing_count > 0:
            print("Team members already exist!")
            return
        
        # Star Wars themed team members
        team_members = [
            {
                "id": str(uuid.uuid4()),
                "name": "Obi-Wan Kenobi",
                "character": "Jedi Master",
                "role": "SEO & Optimizasyon Uzmanı",
                "specialization": "Trendyol SEO stratejileri ve ürün optimizasyonu konusunda galaksinin en deneyimli ustası.",
                "avatar": "https://images.unsplash.com/photo-1566753323558-f4e0952af115?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Yoda",
                "character": "Grand Master",
                "role": "Strateji & Danışmanlık Lideri", 
                "specialization": "900 yıllık deneyimle karlılık stratejileri ve iş geliştirme konularında rehberlik sağlar.",
                "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Luke Skywalker",
                "character": "Jedi Knight",
                "role": "Reklam & Kampanya Uzmanı",
                "specialization": "PPC kampanyaları ve reklam optimizasyonu ile güçlü sonuçlar yaratır.",
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Princess Leia",
                "character": "Rebel Leader",
                "role": "Müşteri İlişkileri Lideri",
                "specialization": "Müşteri deneyimi ve ilişki yönetiminde galaksinin en güçlü lideri.",
                "avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b890?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Ahsoka Tano",
                "character": "Former Jedi",
                "role": "İçerik & Tasarım Uzmanı",
                "specialization": "Kreativ tasarım ve marka kimliği oluşturma konusunda uzman.",
                "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Han Solo",
                "character": "Smuggler & Pilot",
                "role": "İhracat & Global Pazarlama",
                "specialization": "Uluslararası pazarlarda hızlı ve etkili çözümler sunar.",
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Chewbacca",
                "character": "Wookiee Warrior",
                "role": "Teknik Destek & Altyapı",
                "specialization": "Teknik sorunları çözmek ve platform entegrasyonları konusunda güvenilir.",
                "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "R2-D2",
                "character": "Astromech Droid",
                "role": "Veri Analizi & Raporlama",
                "specialization": "Performans analizi, veri madenciliği ve detaylı raporlama konusunda uzman.",
                "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Mace Windu",
                "character": "Jedi Master",
                "role": "İnfluencer Marketing Lideri",
                "specialization": "Sosyal medya stratejileri ve influencer işbirlikleri konusunda usta.",
                "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "isActive": True,
                "createdAt": datetime.utcnow()
            }
        ]
        
        # Insert team members
        result = await db[COLLECTIONS['team_members']].insert_many(team_members)
        
        print(f"✅ {len(team_members)} Star Wars team members created successfully!")
        
        for member in team_members:
            print(f"   {member['character']} {member['name']} - {member['role']}")
        
    except Exception as e:
        print(f"❌ Error creating team members: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(create_team_members())