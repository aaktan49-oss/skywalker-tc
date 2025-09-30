#!/usr/bin/env python3
"""
Create Demo Data for Main Site Integration
Creates specific demo news and projects as requested by user
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://b2b-manager-1.preview.emergentagent.com/api"
PORTAL_URL = "https://b2b-manager-1.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://b2b-manager-1.preview.emergentagent.com/api/content"

class DemoDataCreator:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.content_url = CONTENT_URL
        self.session = requests.Session()
        self.admin_token = None
        self.created_items = []
        
    def log_result(self, action, success, message, details=None):
        """Log result"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {action} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def login_admin(self):
        """Login as admin to get token"""
        login_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.admin_token = data["access_token"]
                    self.log_result("Admin Login", True, "Successfully logged in as admin")
                    return True
                else:
                    self.log_result("Admin Login", False, "No access token received")
            else:
                self.log_result("Admin Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Admin Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def create_demo_data(self):
        """Create specific demo data for main site integration"""
        if not self.admin_token:
            self.log_result("Demo Data Creation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        created_count = 0
        
        try:
            # Create specific demo news articles as requested
            news_articles = [
                {
                    "title": "2025 E-ticaret Trendleri Açıklandı!",
                    "content": "Skywalker.tc olarak 2025 yılında e-ticaret sektöründe bizi bekleyen trendleri analiz ettik. Yapay zeka destekli kişiselleştirme, omnichannel deneyimler ve sürdürülebilir e-ticaret çözümleri ön plana çıkıyor. Müşterilerimizi bu değişime hazırlamak için yeni stratejiler geliştiriyoruz.",
                    "excerpt": "2025'te e-ticaret dünyasını şekillendirecek ana trendler ve bizim bu konudaki hazırlıklarımız",
                    "category": "industry_news",
                    "imageUrl": "https://via.placeholder.com/600x300/6B46C1/FFFFFF?text=E-ticaret+2025",
                    "isPublished": True
                },
                {
                    "title": "Müşteri Başarı Hikayesi: %200 Büyüme",
                    "content": "Bir e-ticaret müşterimiz Skywalker.tc danışmanlığı ile sadece 6 ayda %200 büyüme elde etti. Trendyol optimizasyonu, reklam stratejileri ve müşteri deneyimi iyileştirmeleri ile rakiplerine fark attı.",
                    "excerpt": "6 ayda %200 büyüme sağlayan başarı hikayemiz",
                    "category": "success_stories",
                    "imageUrl": "https://via.placeholder.com/600x300/10B981/FFFFFF?text=Başarı+Hikayesi",
                    "isPublished": True
                },
                {
                    "title": "Skywalker.tc Yeni Ofisine Taşındı",
                    "content": "Büyüyen ekibimiz ve artan müşteri portföyümüz ile birlikte Skywalker.tc yeni ve daha büyük ofisine taşındı. 50 kişilik kapasiteli yeni ofisimizde müşterilerimize daha iyi hizmet vermeye devam edeceğiz.",
                    "excerpt": "Büyüyen ekibimiz için yeni ofis",
                    "category": "company_news",
                    "imageUrl": "https://via.placeholder.com/600x300/3B82F6/FFFFFF?text=Yeni+Ofis",
                    "isPublished": True
                }
            ]
            
            print("\n🗞️ Creating Demo News Articles:")
            print("=" * 50)
            
            for article in news_articles:
                response = self.session.post(f"{self.content_url}/admin/news", json=article, headers=headers)
                if response.status_code == 200 and response.json().get("success"):
                    created_count += 1
                    article_id = response.json().get("id")
                    self.created_items.append({"type": "news", "id": article_id, "title": article["title"]})
                    self.log_result("News Article", True, f"Created: {article['title']}")
                else:
                    self.log_result("News Article", False, f"Failed to create: {article['title']} - HTTP {response.status_code}")
            
            # Create specific demo project as requested
            project_data = {
                "clientName": "TechStore E-ticaret",
                "clientEmail": "info@techstore.com",
                "projectTitle": "Trendyol Mağaza Optimizasyonu ve ROI Artırımı",
                "description": "TechStore için kapsamlı Trendyol optimizasyonu gerçekleştirdik. SEO, görsel iyileştirme, fiyat stratejisi ve reklam yönetimi ile mağaza performansını maksimize ettik.",
                "category": "E-commerce Optimization",
                "status": "completed",
                "results": "Satışlar %180 arttı, CTR %250 iyileşti, ROAS %300 yükseldi",
                "imageUrl": "https://via.placeholder.com/400x300/8B5CF6/FFFFFF?text=TechStore+Projesi",
                "tags": ["trendyol", "optimization", "roas"],
                "isPublic": True
            }
            
            print("\n🏗️ Creating Demo Project:")
            print("=" * 50)
            
            response = self.session.post(f"{self.content_url}/admin/projects", json=project_data, headers=headers)
            if response.status_code == 200 and response.json().get("success"):
                created_count += 1
                project_id = response.json().get("id")
                self.created_items.append({"type": "project", "id": project_id, "title": project_data["projectTitle"]})
                self.log_result("Project", True, f"Created: {project_data['projectTitle']}")
            else:
                self.log_result("Project", False, f"Failed to create project - HTTP {response.status_code}")
            
            return created_count > 0
                
        except Exception as e:
            self.log_result("Demo Data Creation", False, f"Request failed: {str(e)}")
        
        return False
    
    def verify_demo_data(self):
        """Verify that demo data was created successfully"""
        print("\n🔍 Verifying Demo Data:")
        print("=" * 50)
        
        try:
            # Check news articles
            news_response = self.session.get(f"{self.content_url}/news")
            if news_response.status_code == 200:
                news_list = news_response.json()
                self.log_result("News Verification", True, f"Found {len(news_list)} published news articles")
                for article in news_list:
                    print(f"   📰 {article['title']} ({article['category']})")
            else:
                self.log_result("News Verification", False, f"HTTP {news_response.status_code}")
            
            # Check projects
            projects_response = self.session.get(f"{self.content_url}/projects")
            if projects_response.status_code == 200:
                projects_list = projects_response.json()
                self.log_result("Projects Verification", True, f"Found {len(projects_list)} public projects")
                for project in projects_list:
                    print(f"   🏗️ {project['projectTitle']} - {project['clientName']}")
            else:
                self.log_result("Projects Verification", False, f"HTTP {projects_response.status_code}")
                
        except Exception as e:
            self.log_result("Verification", False, f"Request failed: {str(e)}")
    
    def run(self):
        """Run the demo data creation process"""
        print("🚀 Creating Demo Data for Main Site Integration")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print(f"Content URL: {self.content_url}")
        print("=" * 60)
        
        # Login as admin
        if not self.login_admin():
            print("❌ Cannot proceed without admin login")
            return False
        
        # Create demo data
        if self.create_demo_data():
            print(f"\n✅ Successfully created {len(self.created_items)} demo items!")
            
            # Verify the data
            self.verify_demo_data()
            
            print("\n📋 DEMO DATA SUMMARY:")
            print("=" * 50)
            for item in self.created_items:
                print(f"   {item['type'].upper()}: {item['title']}")
            
            print("\n🎯 Demo data is now available for:")
            print("   - NewsSection component on main site")
            print("   - PortfolioSection component on main site")
            print("   - Admin panel content management")
            
            return True
        else:
            print("❌ Failed to create demo data")
            return False

if __name__ == "__main__":
    creator = DemoDataCreator()
    success = creator.run()
    sys.exit(0 if success else 1)