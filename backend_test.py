#!/usr/bin/env python3
"""
Content Management API Authentication and CRUD Testing
Tests admin authentication and all content management endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://galactic-admin.preview.emergentagent.com/api"
PORTAL_URL = "https://galactic-admin.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://galactic-admin.preview.emergentagent.com/api/content"

class ContentManagementAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.content_url = CONTENT_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_items = {
            'site_content': [],
            'news': [],
            'projects': []
        }
        
    def log_test(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_admin_login(self):
        """Test admin login with demo credentials"""
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
                    # Verify JWT token format
                    token_parts = self.admin_token.split('.')
                    if len(token_parts) == 3:
                        self.log_test("Admin Login", True, f"Successfully logged in as admin with valid JWT token")
                        return True
                    else:
                        self.log_test("Admin Login", False, f"Invalid JWT token format: {len(token_parts)} parts")
                else:
                    self.log_test("Admin Login", False, f"Login failed: No access token received")
            else:
                self.log_test("Admin Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_site_content_crud(self):
        """Test Site Content CRUD operations"""
        if not self.admin_token:
            self.log_test("Site Content CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        site_content_data = {
            "section": "hero_section",
            "key": "main_title",
            "title": "Trendyol Galaksisinde Liderlik",
            "content": "E-ticaret dünyasında rehberiniz oluyoruz",
            "order": 1
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/site-content", 
                json=site_content_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    content_id = create_data.get("id")
                    self.created_items['site_content'].append(content_id)
                    self.log_test("Site Content CREATE", True, "Successfully created site content")
                    
                    # READ - Get all site content (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/site-content")
                    if read_response.status_code == 200:
                        content_list = read_response.json()
                        if isinstance(content_list, list):
                            self.log_test("Site Content READ", True, f"Successfully retrieved {len(content_list)} site content items")
                            
                            # UPDATE
                            update_data = {
                                "title": "Updated Trendyol Galaksisinde Liderlik",
                                "content": "Updated: E-ticaret dünyasında rehberiniz oluyoruz"
                            }
                            
                            update_response = self.session.put(
                                f"{self.content_url}/admin/site-content/{content_id}",
                                json=update_data,
                                headers=headers
                            )
                            
                            if update_response.status_code == 200:
                                update_result = update_response.json()
                                if update_result.get("success"):
                                    self.log_test("Site Content UPDATE", True, "Successfully updated site content")
                                    
                                    # DELETE
                                    delete_response = self.session.delete(
                                        f"{self.content_url}/admin/site-content/{content_id}",
                                        headers=headers
                                    )
                                    
                                    if delete_response.status_code == 200:
                                        delete_result = delete_response.json()
                                        if delete_result.get("success"):
                                            self.log_test("Site Content DELETE", True, "Successfully deleted site content")
                                            self.created_items['site_content'].remove(content_id)
                                            return True
                                        else:
                                            self.log_test("Site Content DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                    else:
                                        self.log_test("Site Content DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                else:
                                    self.log_test("Site Content UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                            else:
                                self.log_test("Site Content UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                        else:
                            self.log_test("Site Content READ", False, f"Expected list, got: {type(content_list)}")
                    else:
                        self.log_test("Site Content READ", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("Site Content CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("Site Content CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("Site Content CRUD", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_news_crud(self):
        """Test News CRUD operations"""
        if not self.admin_token:
            self.log_test("News CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        news_data = {
            "title": "Yeni Dijital Pazarlama Stratejileri",
            "content": "2024 yılında e-ticaret sektöründeki en son trend ve stratejiler...",
            "excerpt": "E-ticaret dünyasında başarıya giden yollar",
            "category": "industry_news",
            "isPublished": True
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/news", 
                json=news_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    news_id = create_data.get("id")
                    self.created_items['news'].append(news_id)
                    self.log_test("News CREATE", True, "Successfully created news article")
                    
                    # READ - Get all news (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/news")
                    if read_response.status_code == 200:
                        news_list = read_response.json()
                        if isinstance(news_list, list):
                            self.log_test("News READ", True, f"Successfully retrieved {len(news_list)} news articles")
                            
                            # READ single article
                            single_response = self.session.get(f"{self.content_url}/news/{news_id}")
                            if single_response.status_code == 200:
                                single_article = single_response.json()
                                if single_article.get("id") == news_id:
                                    self.log_test("News READ Single", True, "Successfully retrieved single news article")
                                    
                                    # UPDATE
                                    update_data = {
                                        "title": "Updated Dijital Pazarlama Stratejileri",
                                        "content": "Updated: 2024 yılında e-ticaret sektöründeki en son trend ve stratejiler..."
                                    }
                                    
                                    update_response = self.session.put(
                                        f"{self.content_url}/admin/news/{news_id}",
                                        json=update_data,
                                        headers=headers
                                    )
                                    
                                    if update_response.status_code == 200:
                                        update_result = update_response.json()
                                        if update_result.get("success"):
                                            self.log_test("News UPDATE", True, "Successfully updated news article")
                                            
                                            # DELETE
                                            delete_response = self.session.delete(
                                                f"{self.content_url}/admin/news/{news_id}",
                                                headers=headers
                                            )
                                            
                                            if delete_response.status_code == 200:
                                                delete_result = delete_response.json()
                                                if delete_result.get("success"):
                                                    self.log_test("News DELETE", True, "Successfully deleted news article")
                                                    self.created_items['news'].remove(news_id)
                                                    return True
                                                else:
                                                    self.log_test("News DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                            else:
                                                self.log_test("News DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                        else:
                                            self.log_test("News UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                                    else:
                                        self.log_test("News UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                                else:
                                    self.log_test("News READ Single", False, f"Article ID mismatch: expected {news_id}, got {single_article.get('id')}")
                            else:
                                self.log_test("News READ Single", False, f"HTTP {single_response.status_code}: {single_response.text}")
                        else:
                            self.log_test("News READ", False, f"Expected list, got: {type(news_list)}")
                    else:
                        self.log_test("News READ", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("News CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("News CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("News CRUD", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_projects_crud(self):
        """Test Projects CRUD operations"""
        if not self.admin_token:
            self.log_test("Projects CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        project_data = {
            "clientName": "Demo Mağaza",
            "projectTitle": "E-ticaret Optimizasyon Projesi",
            "description": "Trendyol mağaza performansını %150 artırdık",
            "category": "E-commerce Optimization",
            "status": "completed",
            "results": "Satışlar %150 arttı, ROI %200 gelişti",
            "isPublic": True
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/projects", 
                json=project_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    project_id = create_data.get("id")
                    self.created_items['projects'].append(project_id)
                    self.log_test("Projects CREATE", True, "Successfully created company project")
                    
                    # READ - Get all projects (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/projects")
                    if read_response.status_code == 200:
                        projects_list = read_response.json()
                        if isinstance(projects_list, list):
                            self.log_test("Projects READ", True, f"Successfully retrieved {len(projects_list)} company projects")
                            
                            # READ single project
                            single_response = self.session.get(f"{self.content_url}/projects/{project_id}")
                            if single_response.status_code == 200:
                                single_project = single_response.json()
                                if single_project.get("id") == project_id:
                                    self.log_test("Projects READ Single", True, "Successfully retrieved single company project")
                                    
                                    # UPDATE
                                    update_data = {
                                        "projectTitle": "Updated E-ticaret Optimizasyon Projesi",
                                        "description": "Updated: Trendyol mağaza performansını %150 artırdık"
                                    }
                                    
                                    update_response = self.session.put(
                                        f"{self.content_url}/admin/projects/{project_id}",
                                        json=update_data,
                                        headers=headers
                                    )
                                    
                                    if update_response.status_code == 200:
                                        update_result = update_response.json()
                                        if update_result.get("success"):
                                            self.log_test("Projects UPDATE", True, "Successfully updated company project")
                                            
                                            # DELETE
                                            delete_response = self.session.delete(
                                                f"{self.content_url}/admin/projects/{project_id}",
                                                headers=headers
                                            )
                                            
                                            if delete_response.status_code == 200:
                                                delete_result = delete_response.json()
                                                if delete_result.get("success"):
                                                    self.log_test("Projects DELETE", True, "Successfully deleted company project")
                                                    self.created_items['projects'].remove(project_id)
                                                    return True
                                                else:
                                                    self.log_test("Projects DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                            else:
                                                self.log_test("Projects DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                        else:
                                            self.log_test("Projects UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                                    else:
                                        self.log_test("Projects UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                                else:
                                    self.log_test("Projects READ Single", False, f"Project ID mismatch: expected {project_id}, got {single_project.get('id')}")
                            else:
                                self.log_test("Projects READ Single", False, f"HTTP {single_response.status_code}: {single_response.text}")
                        else:
                            self.log_test("Projects READ", False, f"Expected list, got: {type(projects_list)}")
                    else:
                        self.log_test("Projects READ", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("Projects CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("Projects CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("Projects CRUD", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_demo_data_creation(self):
        """Create specific demo data for main site integration as requested by user"""
        if not self.admin_token:
            self.log_test("Demo Data Creation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        demo_created = 0
        
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
            
            for article in news_articles:
                response = self.session.post(f"{self.content_url}/admin/news", json=article, headers=headers)
                if response.status_code == 200 and response.json().get("success"):
                    demo_created += 1
                    self.created_items['news'].append(response.json().get("id"))
                    self.log_test(f"Demo News: {article['title']}", True, "Successfully created demo news article")
                else:
                    self.log_test(f"Demo News: {article['title']}", False, f"Failed to create: HTTP {response.status_code}")
            
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
            
            response = self.session.post(f"{self.content_url}/admin/projects", json=project_data, headers=headers)
            if response.status_code == 200 and response.json().get("success"):
                demo_created += 1
                self.created_items['projects'].append(response.json().get("id"))
                self.log_test("Demo Project: TechStore", True, "Successfully created demo project")
            else:
                self.log_test("Demo Project: TechStore", False, f"Failed to create: HTTP {response.status_code}")
            
            if demo_created > 0:
                self.log_test("Demo Data Creation", True, f"Successfully created {demo_created} demo items for main site integration")
                return True
            else:
                self.log_test("Demo Data Creation", False, "No demo items were created")
                
        except Exception as e:
            self.log_test("Demo Data Creation", False, f"Request failed: {str(e)}")
        
        return False
    
    def cleanup_test_data(self):
        """Clean up any test data that was created"""
        if not self.admin_token:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        cleaned = 0
        
        # Clean up site content
        for content_id in self.created_items['site_content']:
            try:
                response = self.session.delete(f"{self.content_url}/admin/site-content/{content_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up news
        for news_id in self.created_items['news']:
            try:
                response = self.session.delete(f"{self.content_url}/admin/news/{news_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up projects
        for project_id in self.created_items['projects']:
            try:
                response = self.session.delete(f"{self.content_url}/admin/projects/{project_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} test items")
    
    def run_all_tests(self):
        """Run all content management tests in sequence"""
        print(f"🚀 Starting Content Management API Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"Content URL: {self.content_url}")
        print("=" * 60)
        
        # Test admin authentication
        if not self.test_admin_login():
            print("❌ Admin login failed - cannot proceed with other tests")
            return False
        
        # Test CRUD operations
        self.test_site_content_crud()
        self.test_news_crud()
        self.test_projects_crud()
        
        # Create demo data for admin panel
        self.test_demo_data_creation()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Note about demo data
        demo_items_count = len(self.created_items['site_content']) + len(self.created_items['news']) + len(self.created_items['projects'])
        if demo_items_count > 0:
            print(f"\n📋 DEMO DATA: Created {demo_items_count} demo items for admin panel testing")
            print("   - Site Content items for hero, services, and about sections")
            print("   - News articles covering industry trends and tips")
            print("   - Company projects showcasing successful case studies")
        
        return passed == total

if __name__ == "__main__":
    tester = ContentManagementAPITester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        # Clean up test data
        tester.cleanup_test_data()