"""
Seed script for Services (Galaktik Hizmetler) - Sample data for testing
"""

import asyncio
import motor.motor_asyncio
import os
from datetime import datetime
from models import Service, ServiceType, ServiceFeature

async def seed_services():
    # Database connection
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    db = client[os.getenv("DB_NAME", "test_database")]
    
    # Sample services data
    services_data = [
        {
            "title": "E-ticaret Mağaza Kurulumu",
            "description": "Sıfırdan e-ticaret mağazanızı kurup, optimize ediyoruz. Trendyol, Hepsiburada, n11 ve kendi web sitenizde satışlarınızı artırmanız için gerekli tüm altyapıyı hazırlıyoruz.",
            "shortDescription": "Profesyonel e-ticaret mağaza kurulumu ve optimizasyonu",
            "serviceType": ServiceType.ecommerce,
            "price": 15000.0,
            "duration": "2-4 hafta",
            "icon": "🛒",
            "color": "#10B981",
            "features": [
                ServiceFeature(title="Mağaza Kurulumu", description="Trendyol, Hepsiburada, n11 mağaza açılışı", included=True),
                ServiceFeature(title="Ürün Yükleme", description="500'e kadar ürün yükleme ve optimizasyonu", included=True),
                ServiceFeature(title="SEO Optimizasyonu", description="Arama motoru optimizasyonu", included=True),
                ServiceFeature(title="Reklam Kampanyası", description="İlk ay ücretsiz reklam yönetimi", included=True),
            ],
            "deliverables": [
                "Tamamlanmış e-ticaret mağazası",
                "Yüklenmiş ürün katalogu",
                "SEO raporu",
                "Reklam kampanya stratejisi",
                "Yönetim paneli eğitimi"
            ],
            "requirements": [
                "Ürün listesi ve görselleri",
                "Şirket bilgileri ve belgeler",
                "Banka hesap bilgileri",
                "Logo ve marka materyalleri"
            ],
            "processSteps": [
                "Mağaza açılış işlemleri (1 hafta)",
                "Ürün yükleme ve düzenleme (1 hafta)",
                "SEO ve optimizasyon (1 hafta)",
                "Test ve canlıya alma (3-5 gün)"
            ],
            "timeline": "1. hafta: Mağaza kurulumu ve onaylar, 2. hafta: Ürün yükleme, 3. hafta: Optimizasyon ve test, 4. hafta: Canlıya alma",
            "isActive": True,
            "isFeatured": True,
            "showPrice": True,
            "order": 1,
            "tags": ["e-ticaret", "mağaza", "trendyol", "hepsiburada"],
            "popularityScore": 95,
            "completedProjects": 150
        },
        {
            "title": "Sosyal Medya Yönetimi Premium",
            "description": "Instagram, TikTok, Facebook ve LinkedIn hesaplarınızı profesyonel olarak yönetiyoruz. İçerik üretimi, reels çekimi, story yönetimi ve takipçi artırma stratejileri dahil.",
            "shortDescription": "Profesyonel sosyal medya hesap yönetimi ve içerik üretimi",
            "serviceType": ServiceType.social_media,
            "price": 8000.0,
            "duration": "Aylık paket",
            "icon": "📱",
            "color": "#8B5CF6",
            "features": [
                ServiceFeature(title="İçerik Üretimi", description="Günlük 2-3 kaliteli içerik", included=True),
                ServiceFeature(title="Reels & Story", description="Haftalık reels ve günlük story", included=True),
                ServiceFeature(title="Hashtag Analizi", description="En etkili hashtag setleri", included=True),
                ServiceFeature(title="Takipçi Etkileşimi", description="Yorumlara yanıt ve DM yönetimi", included=True),
            ],
            "deliverables": [
                "Aylık 60+ gönderi",
                "Haftalık reels videoları",
                "Story şablonları",
                "Performans raporu",
                "Hashtag stratejisi"
            ],
            "requirements": [
                "Sosyal medya hesap erişimi",
                "Marka rehberi",
                "Ürün/hizmet bilgileri",
                "Hedef kitle analizi"
            ],
            "processSteps": [
                "Hesap analizi ve strateji",
                "İçerik takvimi hazırlama",
                "İçerik üretimi başlangıç",
                "Performans takibi ve optimizasyon"
            ],
            "timeline": "İlk hafta: Analiz ve planlama, Sonraki haftalar: Günlük içerik üretimi ve yayınlama",
            "isActive": True,
            "isFeatured": True,
            "showPrice": True,
            "order": 2,
            "tags": ["sosyal medya", "instagram", "tiktok", "içerik"],
            "popularityScore": 88,
            "completedProjects": 200
        },
        {
            "title": "Influencer Pazarlama Kampanyası",
            "description": "Markanız için en uygun influencerları bulup, etkili iş birlikleri kuruyoruz. Mikro ve makro influencerlarla kampanya yönetimi, performans takibi ve ROI analizi dahil.",
            "shortDescription": "Influencerlarla profesyonel iş birliği ve kampanya yönetimi",
            "serviceType": ServiceType.influencer_marketing,
            "price": 12000.0,
            "duration": "1-2 ay",
            "icon": "⭐",
            "color": "#F59E0B",
            "features": [
                ServiceFeature(title="Influencer Araştırması", description="Markanıza uygun influencer bulma", included=True),
                ServiceFeature(title="Kampanya Yönetimi", description="A'dan Z'ye kampanya koordinasyonu", included=True),
                ServiceFeature(title="İçerik Kontrolü", description="Paylaşım öncesi onay süreci", included=True),
                ServiceFeature(title="Performans Analizi", description="Detaylı ROI ve engagement raporu", included=True),
            ],
            "deliverables": [
                "Influencer listesi ve profilleri",
                "Kampanya stratejisi",
                "İçerik onay süreci",
                "Performans raporu",
                "ROI analizi"
            ],
            "requirements": [
                "Kampanya bütçesi",
                "Hedef kitle profili",
                "Marka kimliği",
                "Kampanya hedefleri"
            ],
            "processSteps": [
                "Hedef analizi ve influencer araştırması",
                "İletişim ve anlaşma süreçleri",
                "Kampanya yürütme ve takip",
                "Analiz ve raporlama"
            ],
            "timeline": "1. hafta: Influencer araştırması, 2-3. hafta: İletişim ve anlaşmalar, 4-6. hafta: Kampanya yürütme",
            "isActive": True,
            "isFeatured": False,
            "showPrice": True,
            "order": 3,
            "tags": ["influencer", "pazarlama", "kampanya", "sosyal medya"],
            "popularityScore": 78,
            "completedProjects": 85
        },
        {
            "title": "SEO ve Google Ads Optimizasyonu",
            "description": "Web sitenizin Google'da üst sıralara çıkması için teknik SEO, içerik optimizasyonu ve Google Ads kampanya yönetimi. Organik trafik artışı garantili.",
            "shortDescription": "Google'da görünürlük artırma ve trafik optimizasyonu",
            "serviceType": ServiceType.seo,
            "price": 6500.0,
            "duration": "3-6 ay",
            "icon": "🔍",
            "color": "#3B82F6",
            "features": [
                ServiceFeature(title="Teknik SEO", description="Site hızı, mobile uyumluluk optimizasyonu", included=True),
                ServiceFeature(title="İçerik SEO", description="Anahtar kelime analizi ve içerik optimizasyonu", included=True),
                ServiceFeature(title="Google Ads", description="Profesyonel reklam kampanya yönetimi", included=True),
                ServiceFeature(title="Aylık Raporlama", description="Detaylı performans ve trafik raporları", included=True),
            ],
            "deliverables": [
                "Teknik SEO raporu",
                "Optimizasyon checklist",
                "Google Ads kampanyaları",
                "Aylık performans raporları",
                "Anahtar kelime stratejisi"
            ],
            "requirements": [
                "Website erişimi",
                "Google Analytics hesabı",
                "Hedef anahtar kelimeler",
                "Rekabet analizi bilgisi"
            ],
            "processSteps": [
                "Site analizi ve teknik inceleme",
                "SEO stratejisi geliştirme",
                "Optimizasyon uygulama",
                "Google Ads kurulumu ve yönetimi"
            ],
            "timeline": "1. ay: Analiz ve strateji, 2-3. ay: Optimizasyon uygulaması, 4-6. ay: Takip ve iyileştirme",
            "isActive": True,
            "isFeatured": False,
            "showPrice": True,
            "order": 4,
            "tags": ["seo", "google ads", "trafik", "optimizasyon"],
            "popularityScore": 72,
            "completedProjects": 120
        },
        {
            "title": "Marka Kimliği ve Strateji Danışmanlığı",
            "description": "Markanızın pazardaki konumunu güçlendirmek için kapsamlı marka kimliği çalışması, rakip analizi ve pazarlama stratejisi geliştiriyoruz.",
            "shortDescription": "Marka kimliği oluşturma ve pazarlama stratejisi geliştirme",
            "serviceType": ServiceType.branding,
            "price": None,
            "duration": "4-8 hafta",
            "icon": "🎯",
            "color": "#EF4444",
            "features": [
                ServiceFeature(title="Marka Analizi", description="Mevcut durum ve potansiyel analizi", included=True),
                ServiceFeature(title="Rakip Araştırması", description="Detaylı pazar ve rakip analizi", included=True),
                ServiceFeature(title="Strateji Geliştirme", description="Özelleştirilmiş pazarlama stratejisi", included=True),
                ServiceFeature(title="Uygulama Rehberi", description="Adım adım uygulama kılavuzu", included=True),
            ],
            "deliverables": [
                "Marka analiz raporu",
                "Rakip analiz raporu",
                "Pazarlama stratejisi dökümanı",
                "Uygulama roadmap'i",
                "Marka rehberi"
            ],
            "requirements": [
                "Marka geçmişi bilgileri",
                "Hedef pazar tanımı",
                "Bütçe bilgisi",
                "Vizyon ve misyon"
            ],
            "processSteps": [
                "Mevcut durum analizi",
                "Pazar ve rakip araştırması",
                "Strateji geliştirme atölyeleri",
                "Sonuç raporu hazırlama"
            ],
            "timeline": "1-2. hafta: Analiz çalışmaları, 3-4. hafta: Strateji geliştirme, 5-6. hafta: Dokümantasyon",
            "isActive": True,
            "isFeatured": False,
            "showPrice": False,
            "order": 5,
            "tags": ["marka", "strateji", "analiz", "danışmanlık"],
            "popularityScore": 65,
            "completedProjects": 45
        }
    ]
    
    # Insert services
    try:
        # Clear existing services
        await db.services.delete_many({})
        print("Cleared existing services")
        
        # Insert new services
        for service_data in services_data:
            service = Service(**service_data)
            await db.services.insert_one(service.dict())
            print(f"✅ Added service: {service.title}")
        
        print(f"\n🎉 Successfully seeded {len(services_data)} services!")
        
        # Show summary
        total_services = await db.services.count_documents({})
        featured_services = await db.services.count_documents({"isFeatured": True})
        print(f"📊 Total services: {total_services}")
        print(f"⭐ Featured services: {featured_services}")
        
    except Exception as e:
        print(f"❌ Error seeding services: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_services())