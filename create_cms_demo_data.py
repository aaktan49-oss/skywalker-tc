#!/usr/bin/env python3
"""
Create demo data for CMS Extensions (Team, Testimonials, FAQs)
"""

import requests
import json

# Backend URL from frontend .env
BASE_URL = "https://bizops-central-3.preview.emergentagent.com/api"
PORTAL_URL = "https://bizops-central-3.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://bizops-central-3.preview.emergentagent.com/api/content"

def login_admin():
    """Login as admin and get token"""
    login_data = {
        "email": "admin@demo.com",
        "password": "demo123"
    }
    
    response = requests.post(f"{PORTAL_URL}/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    return None

def create_demo_team_members(token):
    """Create demo team members"""
    headers = {"Authorization": f"Bearer {token}"}
    
    team_members = [
        {
            "name": "Ahmet Yılmaz",
            "position": "Kurucu & CEO",
            "department": "Yönetim",
            "bio": "10+ yıllık e-ticaret deneyimi ile Skywalker.tc'yi kurdu. Trendyol ve Amazon uzmanı.",
            "imageUrl": "https://via.placeholder.com/300x300/8B5CF6/FFFFFF?text=AY",
            "email": "ahmet@skywalker.tc",
            "linkedin": "https://linkedin.com/in/ahmetyilmaz",
            "expertise": ["E-ticaret Stratejisi", "Trendyol Optimizasyonu", "Amazon FBA"],
            "order": 1
        },
        {
            "name": "Zeynep Kaya",
            "position": "Pazarlama Müdürü",
            "department": "Pazarlama",
            "bio": "Dijital pazarlama alanında 8 yıllık deneyime sahip. ROI odaklı kampanya yönetimi uzmanı.",
            "imageUrl": "https://via.placeholder.com/300x300/10B981/FFFFFF?text=ZK",
            "email": "zeynep@skywalker.tc",
            "linkedin": "https://linkedin.com/in/zeynepkaya",
            "expertise": ["Google Ads", "Facebook Ads", "Influencer Marketing"],
            "order": 2
        },
        {
            "name": "Mehmet Demir",
            "position": "Teknik Müdür",
            "department": "Teknoloji",
            "bio": "Full-stack developer ve sistem mimarı. E-ticaret platformları geliştirme uzmanı.",
            "imageUrl": "https://via.placeholder.com/300x300/3B82F6/FFFFFF?text=MD",
            "email": "mehmet@skywalker.tc",
            "linkedin": "https://linkedin.com/in/mehmetdemir",
            "expertise": ["React", "Python", "AWS", "MongoDB"],
            "order": 3
        }
    ]
    
    created_count = 0
    for member in team_members:
        response = requests.post(f"{CONTENT_URL}/admin/team", json=member, headers=headers)
        if response.status_code == 200:
            created_count += 1
            print(f"✅ Created team member: {member['name']}")
        else:
            print(f"❌ Failed to create team member: {member['name']} - {response.status_code}")
    
    return created_count

def create_demo_testimonials(token):
    """Create demo testimonials"""
    headers = {"Authorization": f"Bearer {token}"}
    
    testimonials = [
        {
            "clientName": "Ayşe Özkan",
            "clientPosition": "E-ticaret Müdürü",
            "clientCompany": "ModaStore",
            "content": "Skywalker.tc ile çalışmaya başladıktan sonra Trendyol satışlarımız %300 arttı. Profesyonel yaklaşımları ve sonuç odaklı çalışmaları sayesinde rakiplerimizi geride bıraktık.",
            "rating": 5,
            "imageUrl": "https://via.placeholder.com/150x150/8B5CF6/FFFFFF?text=AÖ",
            "projectType": "Trendyol Mağaza Optimizasyonu",
            "order": 1,
            "isFeatured": True
        },
        {
            "clientName": "Can Yılmaz",
            "clientPosition": "Kurucu",
            "clientCompany": "TechGadget",
            "content": "Amazon FBA sürecimizde bize rehberlik ettiler. İlk 6 ayda 50K$ ciro elde ettik. Kesinlikle tavsiye ederim!",
            "rating": 5,
            "imageUrl": "https://via.placeholder.com/150x150/10B981/FFFFFF?text=CY",
            "projectType": "Amazon FBA Danışmanlığı",
            "order": 2,
            "isFeatured": True
        },
        {
            "clientName": "Elif Kara",
            "clientPosition": "Pazarlama Uzmanı",
            "clientCompany": "BeautyWorld",
            "content": "Influencer marketing kampanyalarımızda %400 ROI elde ettik. Skywalker.tc ekibi gerçekten işinin ehli.",
            "rating": 5,
            "imageUrl": "https://via.placeholder.com/150x150/3B82F6/FFFFFF?text=EK",
            "projectType": "Influencer Marketing",
            "order": 3,
            "isFeatured": False
        }
    ]
    
    created_count = 0
    for testimonial in testimonials:
        response = requests.post(f"{CONTENT_URL}/admin/testimonials", json=testimonial, headers=headers)
        if response.status_code == 200:
            created_count += 1
            print(f"✅ Created testimonial: {testimonial['clientName']} - {testimonial['clientCompany']}")
        else:
            print(f"❌ Failed to create testimonial: {testimonial['clientName']} - {response.status_code}")
    
    return created_count

def create_demo_faqs(token):
    """Create demo FAQs"""
    headers = {"Authorization": f"Bearer {token}"}
    
    faqs = [
        {
            "question": "Trendyol mağaza optimizasyonu ne kadar sürer?",
            "answer": "Trendyol mağaza optimizasyonu genellikle 2-4 hafta arasında tamamlanır. Bu süre mağazanızın büyüklüğü, ürün sayısı ve mevcut durumuna göre değişiklik gösterebilir. İlk hafta analiz ve strateji belirleme, ikinci hafta uygulama, üçüncü ve dördüncü haftalarda ise sonuçların takibi yapılır.",
            "category": "Hizmetler",
            "order": 1
        },
        {
            "question": "Amazon FBA için minimum bütçe ne kadar olmalı?",
            "answer": "Amazon FBA'ya başlamak için minimum 10.000-15.000 TL bütçe öneriyoruz. Bu bütçe ürün alımı, Amazon ücretleri, reklam giderleri ve ilk 3 aylık operasyonel giderler için yeterlidir. Tabii ki daha düşük bütçelerle de başlanabilir ancak başarı oranı düşer.",
            "category": "Amazon FBA",
            "order": 2
        },
        {
            "question": "Influencer marketing kampanyalarında ROI nasıl ölçülür?",
            "answer": "Influencer marketing ROI'sini ölçmek için kampanya öncesi ve sonrası satış verilerini karşılaştırırız. Ayrıca özel indirim kodları, UTM parametreleri ve landing page analitiği kullanarak doğrudan dönüşümleri takip ederiz. Ortalama ROI %200-400 arasında değişir.",
            "category": "Pazarlama",
            "order": 3
        },
        {
            "question": "Hangi e-ticaret platformunu seçmeliyim?",
            "answer": "Platform seçimi işinizin büyüklüğüne ve hedeflerinize bağlıdır. Küçük işletmeler için Shopify veya WooCommerce, orta ölçekli işletmeler için Magento, büyük işletmeler için ise özel geliştirme öneriyoruz. Türkiye'de Trendyol ve Hepsiburada gibi pazaryerlerinde de satış yapmanızı tavsiye ederiz.",
            "category": "Genel",
            "order": 4
        },
        {
            "question": "SEO sonuçları ne kadar sürede görülür?",
            "answer": "SEO sonuçları genellikle 3-6 ay arasında görülmeye başlar. İlk 3 ayda teknik SEO ve içerik optimizasyonları yapılır, 3-6 ay arasında organik trafik artışı gözlemlenir. Rekabetçi sektörlerde bu süre 6-12 aya kadar uzayabilir.",
            "category": "SEO",
            "order": 5
        }
    ]
    
    created_count = 0
    for faq in faqs:
        response = requests.post(f"{CONTENT_URL}/admin/faqs", json=faq, headers=headers)
        if response.status_code == 200:
            created_count += 1
            print(f"✅ Created FAQ: {faq['question'][:50]}...")
        else:
            print(f"❌ Failed to create FAQ: {faq['question'][:50]}... - {response.status_code}")
    
    return created_count

def main():
    print("🚀 Creating CMS Demo Data")
    print("=" * 50)
    
    # Login as admin
    token = login_admin()
    if not token:
        print("❌ Failed to login as admin")
        return
    
    print("✅ Admin login successful")
    
    # Create demo data
    team_count = create_demo_team_members(token)
    testimonial_count = create_demo_testimonials(token)
    faq_count = create_demo_faqs(token)
    
    print("\n" + "=" * 50)
    print("📊 DEMO DATA CREATION SUMMARY")
    print("=" * 50)
    print(f"Team Members Created: {team_count}")
    print(f"Testimonials Created: {testimonial_count}")
    print(f"FAQs Created: {faq_count}")
    print(f"Total Items Created: {team_count + testimonial_count + faq_count}")
    
    if team_count + testimonial_count + faq_count > 0:
        print("\n✅ Demo data creation completed successfully!")
        print("🎉 CMS Extensions are ready for use!")
    else:
        print("\n❌ No demo data was created")

if __name__ == "__main__":
    main()