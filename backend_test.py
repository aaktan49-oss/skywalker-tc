#!/usr/bin/env python3
"""
Comprehensive Marketing and Analytics System Testing
Tests all marketing endpoints and features including newsletter, lead capture, analytics, WhatsApp, and enhanced site settings
"""

import requests
import json
import sys
import io
from datetime import datetime
from PIL import Image
import urllib.parse

# Backend URL from frontend .env
BASE_URL = "https://b2b-manager-1.preview.emergentagent.com/api"
PORTAL_URL = "https://b2b-manager-1.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://b2b-manager-1.preview.emergentagent.com/api/content"
FILES_URL = "https://b2b-manager-1.preview.emergentagent.com/api/files"
MARKETING_URL = "https://b2b-manager-1.preview.emergentagent.com/api/marketing"

class MarketingAnalyticsSystemTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.content_url = CONTENT_URL
        self.files_url = FILES_URL
        self.marketing_url = MARKETING_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_items = {
            'site_content': [],
            'news': [],
            'projects': [],
            'files': [],
            'newsletter_subscribers': [],
            'leads': [],
            'page_views': [],
            'analytics_events': []
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
        import time
        unique_key = f"test_title_{int(time.time())}"
        site_content_data = {
            "section": "hero_section",
            "key": unique_key,
            "title": "Test Trendyol Galaksisinde Liderlik",
            "content": "Test: E-ticaret dünyasında rehberiniz oluyoruz",
            "order": 999
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
    
    def create_test_image(self):
        """Create a small test JPG image in memory"""
        try:
            # Create a small 100x100 purple image
            img = Image.new('RGB', (100, 100), color='#8B5CF6')
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=85)
            img_buffer.seek(0)
            return img_buffer
        except Exception as e:
            self.log_test("Create Test Image", False, f"Failed to create test image: {str(e)}")
            return None
    
    def test_file_upload(self):
        """Test file upload functionality"""
        if not self.admin_token:
            self.log_test("File Upload", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Create test image
            test_image = self.create_test_image()
            if not test_image:
                return False
            
            # Test file upload
            files = {
                'file': ('test_image.jpg', test_image, 'image/jpeg')
            }
            data = {
                'category': 'image',
                'description': 'Test image upload'
            }
            
            response = self.session.post(
                f"{self.files_url}/upload",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    file_info = result.get("file", {})
                    file_id = file_info.get("id")
                    if file_id:
                        self.created_items['files'].append(file_id)
                        self.log_test("File Upload", True, f"Successfully uploaded test image (ID: {file_id})")
                        return file_info
                    else:
                        self.log_test("File Upload", False, "No file ID returned")
                else:
                    self.log_test("File Upload", False, f"Upload failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("File Upload", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("File Upload", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_file_list(self):
        """Test file listing functionality"""
        if not self.admin_token:
            self.log_test("File List", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.files_url}/list", headers=headers)
            
            if response.status_code == 200:
                files_list = response.json()
                if isinstance(files_list, list):
                    self.log_test("File List", True, f"Successfully retrieved {len(files_list)} files")
                    return files_list
                else:
                    self.log_test("File List", False, f"Expected list, got: {type(files_list)}")
            else:
                self.log_test("File List", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("File List", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_file_serve(self, filename):
        """Test file serving functionality"""
        try:
            response = self.session.get(f"{self.files_url}/serve/{filename}")
            
            if response.status_code == 200:
                if response.headers.get('content-type', '').startswith('image/'):
                    self.log_test("File Serve", True, f"Successfully served file: {filename}")
                    return True
                else:
                    self.log_test("File Serve", False, f"Unexpected content type: {response.headers.get('content-type')}")
            else:
                self.log_test("File Serve", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("File Serve", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_file_delete(self, file_id):
        """Test file deletion functionality"""
        if not self.admin_token:
            self.log_test("File Delete", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.delete(f"{self.files_url}/{file_id}", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("File Delete", True, f"Successfully deleted file: {file_id}")
                    if file_id in self.created_items['files']:
                        self.created_items['files'].remove(file_id)
                    return True
                else:
                    self.log_test("File Delete", False, f"Delete failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("File Delete", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("File Delete", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_file_upload_error_handling(self):
        """Test file upload error handling"""
        if not self.admin_token:
            self.log_test("File Upload Error Handling", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        error_tests_passed = 0
        
        try:
            # Test 1: Large file (simulate by creating large content)
            large_content = b"x" * (11 * 1024 * 1024)  # 11MB
            files = {'file': ('large_file.jpg', io.BytesIO(large_content), 'image/jpeg')}
            
            response = self.session.post(f"{self.files_url}/upload", files=files, headers=headers)
            if response.status_code == 400 and "size" in response.text.lower():
                self.log_test("Large File Rejection", True, "Correctly rejected large file")
                error_tests_passed += 1
            else:
                self.log_test("Large File Rejection", False, f"Expected 400 error, got {response.status_code}")
            
            # Test 2: Unsupported file format
            files = {'file': ('test.exe', io.BytesIO(b"fake exe content"), 'application/octet-stream')}
            
            response = self.session.post(f"{self.files_url}/upload", files=files, headers=headers)
            if response.status_code == 400 and ("type" in response.text.lower() or "allowed" in response.text.lower()):
                self.log_test("Unsupported Format Rejection", True, "Correctly rejected unsupported file format")
                error_tests_passed += 1
            else:
                self.log_test("Unsupported Format Rejection", False, f"Expected 400 error, got {response.status_code}")
            
            # Test 3: Non-admin access (test without token)
            test_image = self.create_test_image()
            if test_image:
                files = {'file': ('test.jpg', test_image, 'image/jpeg')}
                
                response = self.session.post(f"{self.files_url}/upload", files=files)
                if response.status_code in [401, 403]:
                    self.log_test("Non-Admin Access Rejection", True, "Correctly rejected non-admin upload")
                    error_tests_passed += 1
                else:
                    self.log_test("Non-Admin Access Rejection", False, f"Expected 401/403 error, got {response.status_code}")
            
            if error_tests_passed == 3:
                self.log_test("File Upload Error Handling", True, "All error handling tests passed")
                return True
            else:
                self.log_test("File Upload Error Handling", False, f"Only {error_tests_passed}/3 error tests passed")
                
        except Exception as e:
            self.log_test("File Upload Error Handling", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_site_settings_get(self):
        """Test getting site settings (public endpoint)"""
        try:
            response = self.session.get(f"{self.content_url}/site-settings")
            
            if response.status_code == 200:
                settings = response.json()
                if isinstance(settings, dict):
                    # Check for expected default fields
                    expected_fields = ['siteName', 'siteTagline', 'primaryColor', 'contactEmail']
                    found_fields = [field for field in expected_fields if field in settings]
                    
                    if len(found_fields) >= 3:  # At least 3 out of 4 expected fields
                        self.log_test("Site Settings GET", True, f"Successfully retrieved site settings with {len(found_fields)}/4 expected fields")
                        return settings
                    else:
                        self.log_test("Site Settings GET", False, f"Missing expected fields. Found: {found_fields}")
                else:
                    self.log_test("Site Settings GET", False, f"Expected dict, got: {type(settings)}")
            else:
                self.log_test("Site Settings GET", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Site Settings GET", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_site_settings_update(self):
        """Test updating site settings (admin only)"""
        if not self.admin_token:
            self.log_test("Site Settings Update", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test data as specified in the review request
        update_data = {
            "siteName": "Skywalker.tc",
            "siteTagline": "E-ticaret Galaksisinde Rehberiniz",
            "primaryColor": "#8B5CF6",
            "contactEmail": "admin@skywalker.tc"
        }
        
        try:
            response = self.session.put(
                f"{self.content_url}/admin/site-settings",
                json=update_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Site Settings Update", True, "Successfully updated site settings")
                    
                    # Verify the update by getting settings again
                    verify_response = self.session.get(f"{self.content_url}/site-settings")
                    if verify_response.status_code == 200:
                        updated_settings = verify_response.json()
                        if updated_settings.get("siteName") == update_data["siteName"]:
                            self.log_test("Site Settings Verification", True, "Settings update verified successfully")
                            return True
                        else:
                            self.log_test("Site Settings Verification", False, "Updated settings not reflected")
                    else:
                        self.log_test("Site Settings Verification", False, f"Verification failed: HTTP {verify_response.status_code}")
                else:
                    self.log_test("Site Settings Update", False, f"Update failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Site Settings Update", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Site Settings Update", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_uploads_directory(self):
        """Test if uploads directory exists and is accessible"""
        try:
            # This is a backend test, so we can't directly check the filesystem
            # Instead, we'll test if the file serving endpoint works
            # by trying to access a non-existent file (should return 404)
            response = self.session.get(f"{self.files_url}/serve/nonexistent_file.jpg")
            
            if response.status_code == 404:
                self.log_test("Uploads Directory", True, "File serving endpoint is working (404 for non-existent file)")
                return True
            else:
                self.log_test("Uploads Directory", False, f"Unexpected response for non-existent file: {response.status_code}")
                
        except Exception as e:
            self.log_test("Uploads Directory", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_file_management_tests(self):
        """Run all file management tests"""
        print("\n🗂️  FILE MANAGEMENT TESTS")
        print("=" * 40)
        
        # Test uploads directory
        self.test_uploads_directory()
        
        # Test file upload
        uploaded_file = self.test_file_upload()
        
        # Test file listing
        files_list = self.test_file_list()
        
        # Test file serving (if we have an uploaded file)
        if uploaded_file and uploaded_file.get("url"):
            filename = uploaded_file["url"].split("/")[-1]
            self.test_file_serve(filename)
        
        # Test file deletion (if we have a file ID)
        if uploaded_file and uploaded_file.get("id"):
            self.test_file_delete(uploaded_file["id"])
        
        # Test error handling
        self.test_file_upload_error_handling()
    
    def run_site_settings_tests(self):
        """Run all site settings tests"""
        print("\n⚙️  SITE SETTINGS TESTS")
        print("=" * 40)
        
        # Test getting site settings (public)
        self.test_site_settings_get()
        
        # Test updating site settings (admin)
        self.test_site_settings_update()
    
    def cleanup_test_data(self):
        """Clean up any test data that was created"""
        if not self.admin_token:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        cleaned = 0
        
        # Clean up files
        for file_id in self.created_items.get('files', []):
            try:
                response = self.session.delete(f"{self.files_url}/{file_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up site content
        for content_id in self.created_items.get('site_content', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/site-content/{content_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up news
        for news_id in self.created_items.get('news', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/news/{news_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up projects
        for project_id in self.created_items.get('projects', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/projects/{project_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up team members
        for team_id in self.created_items.get('team', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/team/{team_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up testimonials
        for testimonial_id in self.created_items.get('testimonials', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/testimonials/{testimonial_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        # Clean up FAQs
        for faq_id in self.created_items.get('faqs', []):
            try:
                response = self.session.delete(f"{self.content_url}/admin/faqs/{faq_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} test items")
    
    def test_admin_content_endpoints_authorization(self):
        """Test the specific admin content endpoints that were fixed for authorization"""
        if not self.admin_token:
            self.log_test("Admin Content Authorization", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoints_tested = 0
        endpoints_passed = 0
        
        # Test the three specific endpoints mentioned in the review request
        test_endpoints = [
            ("/content/admin/site-content", "Site Content Admin"),
            ("/content/admin/news", "News Admin"),
            ("/content/admin/projects", "Projects Admin")
        ]
        
        for endpoint, name in test_endpoints:
            try:
                endpoints_tested += 1
                response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test(f"{name} GET Authorization", True, f"Successfully retrieved {len(data)} items with Authorization header")
                        endpoints_passed += 1
                    else:
                        self.log_test(f"{name} GET Authorization", False, f"Expected list response, got: {type(data)}")
                elif response.status_code == 403:
                    self.log_test(f"{name} GET Authorization", False, f"403 Forbidden - Authorization header not working properly")
                else:
                    self.log_test(f"{name} GET Authorization", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"{name} GET Authorization", False, f"Request failed: {str(e)}")
        
        # Test without Authorization header to ensure it fails properly
        try:
            response = self.session.get(f"{self.base_url}/api/content/admin/site-content")
            if response.status_code in [401, 403]:
                self.log_test("No Authorization Header Rejection", True, f"Correctly rejected request without Authorization header (HTTP {response.status_code})")
                endpoints_passed += 1
                endpoints_tested += 1
            else:
                self.log_test("No Authorization Header Rejection", False, f"Expected 401/403, got HTTP {response.status_code}")
                endpoints_tested += 1
        except Exception as e:
            self.log_test("No Authorization Header Rejection", False, f"Request failed: {str(e)}")
            endpoints_tested += 1
        
        success_rate = (endpoints_passed / endpoints_tested) * 100 if endpoints_tested > 0 else 0
        overall_success = endpoints_passed == endpoints_tested
        
        self.log_test("Admin Content Authorization Overall", overall_success, 
                     f"Authorization fix verification: {endpoints_passed}/{endpoints_tested} tests passed ({success_rate:.1f}%)")
        
        return overall_success

    def test_full_admin_panel_workflow(self):
        """Test the complete admin panel workflow that was previously broken"""
        if not self.admin_token:
            self.log_test("Admin Panel Workflow", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        workflow_steps = 0
        workflow_passed = 0
        
        try:
            # Step 1: Load existing site content (this was failing before the fix)
            workflow_steps += 1
            response = self.session.get(f"{self.content_url}/admin/site-content", headers=headers)
            if response.status_code == 200:
                existing_content = response.json()
                self.log_test("Load Existing Site Content", True, f"Successfully loaded {len(existing_content)} existing site content items")
                workflow_passed += 1
            else:
                self.log_test("Load Existing Site Content", False, f"Failed to load: HTTP {response.status_code}")
            
            # Step 2: Load existing news (this was failing before the fix)
            workflow_steps += 1
            response = self.session.get(f"{self.content_url}/admin/news", headers=headers)
            if response.status_code == 200:
                existing_news = response.json()
                self.log_test("Load Existing News", True, f"Successfully loaded {len(existing_news)} existing news articles")
                workflow_passed += 1
            else:
                self.log_test("Load Existing News", False, f"Failed to load: HTTP {response.status_code}")
            
            # Step 3: Load existing projects (this was failing before the fix)
            workflow_steps += 1
            response = self.session.get(f"{self.content_url}/admin/projects", headers=headers)
            if response.status_code == 200:
                existing_projects = response.json()
                self.log_test("Load Existing Projects", True, f"Successfully loaded {len(existing_projects)} existing projects")
                workflow_passed += 1
            else:
                self.log_test("Load Existing Projects", False, f"Failed to load: HTTP {response.status_code}")
            
            # Step 4: Test creating new content (POST should work as it was already using headers)
            workflow_steps += 1
            import time
            unique_key = f"test_auth_fix_{int(time.time())}"
            test_content = {
                "section": "hero_section",
                "key": unique_key,
                "title": "Authorization Fix Test",
                "content": "Testing that admin can now load existing content for editing",
                "order": 999
            }
            
            response = self.session.post(f"{self.content_url}/admin/site-content", json=test_content, headers=headers)
            if response.status_code == 200:
                create_result = response.json()
                if create_result.get("success"):
                    content_id = create_result.get("id")
                    self.created_items['site_content'].append(content_id)
                    self.log_test("Create New Content", True, "Successfully created new content item")
                    workflow_passed += 1
                    
                    # Step 5: Test updating the content (PUT should work)
                    workflow_steps += 1
                    update_data = {"content": "Updated: Testing that admin can now load existing content for editing"}
                    response = self.session.put(f"{self.content_url}/admin/site-content/{content_id}", json=update_data, headers=headers)
                    if response.status_code == 200:
                        self.log_test("Update Content", True, "Successfully updated content item")
                        workflow_passed += 1
                    else:
                        self.log_test("Update Content", False, f"Failed to update: HTTP {response.status_code}")
                    
                    # Step 6: Test deleting the content (DELETE should work)
                    workflow_steps += 1
                    response = self.session.delete(f"{self.content_url}/admin/site-content/{content_id}", headers=headers)
                    if response.status_code == 200:
                        self.log_test("Delete Content", True, "Successfully deleted content item")
                        workflow_passed += 1
                        self.created_items['site_content'].remove(content_id)
                    else:
                        self.log_test("Delete Content", False, f"Failed to delete: HTTP {response.status_code}")
                else:
                    self.log_test("Create New Content", False, f"Create failed: {create_result.get('message', 'Unknown error')}")
            else:
                self.log_test("Create New Content", False, f"Failed to create: HTTP {response.status_code}")
        
        except Exception as e:
            self.log_test("Admin Panel Workflow", False, f"Workflow failed: {str(e)}")
        
        success_rate = (workflow_passed / workflow_steps) * 100 if workflow_steps > 0 else 0
        overall_success = workflow_passed == workflow_steps
        
        self.log_test("Admin Panel Workflow Overall", overall_success, 
                     f"Complete admin panel workflow: {workflow_passed}/{workflow_steps} steps passed ({success_rate:.1f}%)")
        
        return overall_success

    def test_team_crud(self):
        """Test Team Management CRUD operations"""
        if not self.admin_token:
            self.log_test("Team CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        team_data = {
            "name": "Ahmet Yılmaz",
            "position": "Senior E-ticaret Uzmanı",
            "department": "Pazarlama",
            "bio": "5 yıllık e-ticaret deneyimi ile müşterilerimize en iyi hizmeti sunuyor.",
            "imageUrl": "https://via.placeholder.com/300x300/8B5CF6/FFFFFF?text=AY",
            "email": "ahmet@skywalker.tc",
            "linkedin": "https://linkedin.com/in/ahmetyilmaz",
            "expertise": ["Trendyol Optimizasyonu", "Reklam Yönetimi", "SEO"],
            "order": 1
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/team", 
                json=team_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    member_id = create_data.get("id")
                    self.created_items['team'] = getattr(self.created_items, 'team', [])
                    self.created_items['team'].append(member_id)
                    self.log_test("Team CREATE", True, "Successfully created team member")
                    
                    # READ - Get all team members (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/team")
                    if read_response.status_code == 200:
                        team_list = read_response.json()
                        if isinstance(team_list, list):
                            self.log_test("Team READ Public", True, f"Successfully retrieved {len(team_list)} team members")
                            
                            # READ - Get all team members (admin endpoint)
                            admin_read_response = self.session.get(f"{self.content_url}/admin/team", headers=headers)
                            if admin_read_response.status_code == 200:
                                admin_team_list = admin_read_response.json()
                                if isinstance(admin_team_list, list):
                                    self.log_test("Team READ Admin", True, f"Successfully retrieved {len(admin_team_list)} team members (admin)")
                                    
                                    # UPDATE
                                    update_data = {
                                        "bio": "Updated: 5+ yıllık e-ticaret deneyimi ile müşterilerimize en iyi hizmeti sunuyor.",
                                        "expertise": ["Trendyol Optimizasyonu", "Reklam Yönetimi", "SEO", "Analitik"]
                                    }
                                    
                                    update_response = self.session.put(
                                        f"{self.content_url}/admin/team/{member_id}",
                                        json=update_data,
                                        headers=headers
                                    )
                                    
                                    if update_response.status_code == 200:
                                        update_result = update_response.json()
                                        if update_result.get("success"):
                                            self.log_test("Team UPDATE", True, "Successfully updated team member")
                                            
                                            # DELETE
                                            delete_response = self.session.delete(
                                                f"{self.content_url}/admin/team/{member_id}",
                                                headers=headers
                                            )
                                            
                                            if delete_response.status_code == 200:
                                                delete_result = delete_response.json()
                                                if delete_result.get("success"):
                                                    self.log_test("Team DELETE", True, "Successfully deleted team member")
                                                    self.created_items['team'].remove(member_id)
                                                    return True
                                                else:
                                                    self.log_test("Team DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                            else:
                                                self.log_test("Team DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                        else:
                                            self.log_test("Team UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                                    else:
                                        self.log_test("Team UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                                else:
                                    self.log_test("Team READ Admin", False, f"Expected list, got: {type(admin_team_list)}")
                            else:
                                self.log_test("Team READ Admin", False, f"HTTP {admin_read_response.status_code}: {admin_read_response.text}")
                        else:
                            self.log_test("Team READ Public", False, f"Expected list, got: {type(team_list)}")
                    else:
                        self.log_test("Team READ Public", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("Team CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("Team CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("Team CRUD", False, f"Request failed: {str(e)}")
        
        return False

    def test_testimonials_crud(self):
        """Test Testimonials Management CRUD operations"""
        if not self.admin_token:
            self.log_test("Testimonials CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        testimonial_data = {
            "clientName": "Mehmet Demir",
            "clientPosition": "E-ticaret Müdürü",
            "clientCompany": "TechStore E-ticaret",
            "content": "Skywalker.tc ile çalışmaya başladıktan sonra satışlarımız %200 arttı. Profesyonel yaklaşımları ve sonuç odaklı çalışmaları sayesinde Trendyol'da lider konuma geldik.",
            "rating": 5,
            "imageUrl": "https://via.placeholder.com/150x150/10B981/FFFFFF?text=MD",
            "projectType": "Trendyol Optimizasyonu",
            "order": 1,
            "isFeatured": True
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/testimonials", 
                json=testimonial_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    testimonial_id = create_data.get("id")
                    self.created_items['testimonials'] = getattr(self.created_items, 'testimonials', [])
                    self.created_items['testimonials'].append(testimonial_id)
                    self.log_test("Testimonials CREATE", True, "Successfully created testimonial")
                    
                    # READ - Get all testimonials (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/testimonials")
                    if read_response.status_code == 200:
                        testimonials_list = read_response.json()
                        if isinstance(testimonials_list, list):
                            self.log_test("Testimonials READ Public", True, f"Successfully retrieved {len(testimonials_list)} testimonials")
                            
                            # READ - Get featured testimonials only
                            featured_response = self.session.get(f"{self.content_url}/testimonials?featured_only=true")
                            if featured_response.status_code == 200:
                                featured_list = featured_response.json()
                                if isinstance(featured_list, list):
                                    self.log_test("Testimonials READ Featured", True, f"Successfully retrieved {len(featured_list)} featured testimonials")
                                    
                                    # READ - Get all testimonials (admin endpoint)
                                    admin_read_response = self.session.get(f"{self.content_url}/admin/testimonials", headers=headers)
                                    if admin_read_response.status_code == 200:
                                        admin_testimonials_list = admin_read_response.json()
                                        if isinstance(admin_testimonials_list, list):
                                            self.log_test("Testimonials READ Admin", True, f"Successfully retrieved {len(admin_testimonials_list)} testimonials (admin)")
                                            
                                            # UPDATE
                                            update_data = {
                                                "content": "Updated: Skywalker.tc ile çalışmaya başladıktan sonra satışlarımız %250 arttı!",
                                                "rating": 5,
                                                "isFeatured": False
                                            }
                                            
                                            update_response = self.session.put(
                                                f"{self.content_url}/admin/testimonials/{testimonial_id}",
                                                json=update_data,
                                                headers=headers
                                            )
                                            
                                            if update_response.status_code == 200:
                                                update_result = update_response.json()
                                                if update_result.get("success"):
                                                    self.log_test("Testimonials UPDATE", True, "Successfully updated testimonial")
                                                    
                                                    # DELETE
                                                    delete_response = self.session.delete(
                                                        f"{self.content_url}/admin/testimonials/{testimonial_id}",
                                                        headers=headers
                                                    )
                                                    
                                                    if delete_response.status_code == 200:
                                                        delete_result = delete_response.json()
                                                        if delete_result.get("success"):
                                                            self.log_test("Testimonials DELETE", True, "Successfully deleted testimonial")
                                                            self.created_items['testimonials'].remove(testimonial_id)
                                                            return True
                                                        else:
                                                            self.log_test("Testimonials DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                                    else:
                                                        self.log_test("Testimonials DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                                else:
                                                    self.log_test("Testimonials UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                                            else:
                                                self.log_test("Testimonials UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                                        else:
                                            self.log_test("Testimonials READ Admin", False, f"Expected list, got: {type(admin_testimonials_list)}")
                                    else:
                                        self.log_test("Testimonials READ Admin", False, f"HTTP {admin_read_response.status_code}: {admin_read_response.text}")
                                else:
                                    self.log_test("Testimonials READ Featured", False, f"Expected list, got: {type(featured_list)}")
                            else:
                                self.log_test("Testimonials READ Featured", False, f"HTTP {featured_response.status_code}: {featured_response.text}")
                        else:
                            self.log_test("Testimonials READ Public", False, f"Expected list, got: {type(testimonials_list)}")
                    else:
                        self.log_test("Testimonials READ Public", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("Testimonials CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("Testimonials CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("Testimonials CRUD", False, f"Request failed: {str(e)}")
        
        return False

    def test_faqs_crud(self):
        """Test FAQ Management CRUD operations"""
        if not self.admin_token:
            self.log_test("FAQs CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE
        faq_data = {
            "question": "Trendyol mağaza optimizasyonu ne kadar sürer?",
            "answer": "Trendyol mağaza optimizasyonu genellikle 2-4 hafta arasında tamamlanır. Bu süre mağazanızın büyüklüğü, ürün sayısı ve mevcut durumuna göre değişiklik gösterebilir. İlk hafta analiz ve strateji belirleme, ikinci hafta uygulama, üçüncü ve dördüncü haftalarda ise sonuçların takibi yapılır.",
            "category": "Hizmetler",
            "order": 1
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.content_url}/admin/faqs", 
                json=faq_data, 
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_data = create_response.json()
                if create_data.get("success"):
                    faq_id = create_data.get("id")
                    self.created_items['faqs'] = getattr(self.created_items, 'faqs', [])
                    self.created_items['faqs'].append(faq_id)
                    self.log_test("FAQs CREATE", True, "Successfully created FAQ")
                    
                    # READ - Get all FAQs (public endpoint)
                    read_response = self.session.get(f"{self.content_url}/faqs")
                    if read_response.status_code == 200:
                        faqs_list = read_response.json()
                        if isinstance(faqs_list, list):
                            self.log_test("FAQs READ Public", True, f"Successfully retrieved {len(faqs_list)} FAQs")
                            
                            # READ - Get FAQs by category
                            category_response = self.session.get(f"{self.content_url}/faqs?category=Hizmetler")
                            if category_response.status_code == 200:
                                category_list = category_response.json()
                                if isinstance(category_list, list):
                                    self.log_test("FAQs READ by Category", True, f"Successfully retrieved {len(category_list)} FAQs in 'Hizmetler' category")
                                    
                                    # READ - Get all FAQs (admin endpoint)
                                    admin_read_response = self.session.get(f"{self.content_url}/admin/faqs", headers=headers)
                                    if admin_read_response.status_code == 200:
                                        admin_faqs_list = admin_read_response.json()
                                        if isinstance(admin_faqs_list, list):
                                            self.log_test("FAQs READ Admin", True, f"Successfully retrieved {len(admin_faqs_list)} FAQs (admin)")
                                            
                                            # UPDATE
                                            update_data = {
                                                "answer": "Updated: Trendyol mağaza optimizasyonu genellikle 1-3 hafta arasında tamamlanır. Hızlı sonuç odaklı yaklaşımımız sayesinde daha kısa sürede etkili sonuçlar elde edebilirsiniz.",
                                                "category": "Hizmetler ve Süreçler"
                                            }
                                            
                                            update_response = self.session.put(
                                                f"{self.content_url}/admin/faqs/{faq_id}",
                                                json=update_data,
                                                headers=headers
                                            )
                                            
                                            if update_response.status_code == 200:
                                                update_result = update_response.json()
                                                if update_result.get("success"):
                                                    self.log_test("FAQs UPDATE", True, "Successfully updated FAQ")
                                                    
                                                    # DELETE
                                                    delete_response = self.session.delete(
                                                        f"{self.content_url}/admin/faqs/{faq_id}",
                                                        headers=headers
                                                    )
                                                    
                                                    if delete_response.status_code == 200:
                                                        delete_result = delete_response.json()
                                                        if delete_result.get("success"):
                                                            self.log_test("FAQs DELETE", True, "Successfully deleted FAQ")
                                                            self.created_items['faqs'].remove(faq_id)
                                                            return True
                                                        else:
                                                            self.log_test("FAQs DELETE", False, f"Delete failed: {delete_result.get('message', 'Unknown error')}")
                                                    else:
                                                        self.log_test("FAQs DELETE", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                                                else:
                                                    self.log_test("FAQs UPDATE", False, f"Update failed: {update_result.get('message', 'Unknown error')}")
                                            else:
                                                self.log_test("FAQs UPDATE", False, f"HTTP {update_response.status_code}: {update_response.text}")
                                        else:
                                            self.log_test("FAQs READ Admin", False, f"Expected list, got: {type(admin_faqs_list)}")
                                    else:
                                        self.log_test("FAQs READ Admin", False, f"HTTP {admin_read_response.status_code}: {admin_read_response.text}")
                                else:
                                    self.log_test("FAQs READ by Category", False, f"Expected list, got: {type(category_list)}")
                            else:
                                self.log_test("FAQs READ by Category", False, f"HTTP {category_response.status_code}: {category_response.text}")
                        else:
                            self.log_test("FAQs READ Public", False, f"Expected list, got: {type(faqs_list)}")
                    else:
                        self.log_test("FAQs READ Public", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("FAQs CREATE", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
            else:
                self.log_test("FAQs CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("FAQs CRUD", False, f"Request failed: {str(e)}")
        
        return False

    def test_cms_authentication_and_authorization(self):
        """Test authentication and authorization for CMS endpoints"""
        # Test public endpoints without authentication
        public_endpoints = [
            ("/content/team", "Team Public"),
            ("/content/testimonials", "Testimonials Public"),
            ("/content/faqs", "FAQs Public")
        ]
        
        public_tests_passed = 0
        for endpoint, name in public_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test(f"{name} No Auth Required", True, f"Public endpoint accessible without authentication")
                        public_tests_passed += 1
                    else:
                        self.log_test(f"{name} No Auth Required", False, f"Expected list response, got: {type(data)}")
                else:
                    self.log_test(f"{name} No Auth Required", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test(f"{name} No Auth Required", False, f"Request failed: {str(e)}")
        
        # Test admin endpoints without authentication (should fail)
        admin_endpoints = [
            ("/content/admin/team", "Team Admin"),
            ("/content/admin/testimonials", "Testimonials Admin"),
            ("/content/admin/faqs", "FAQs Admin")
        ]
        
        auth_tests_passed = 0
        for endpoint, name in admin_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code in [401, 403]:
                    self.log_test(f"{name} Auth Required", True, f"Correctly rejected request without authentication (HTTP {response.status_code})")
                    auth_tests_passed += 1
                else:
                    self.log_test(f"{name} Auth Required", False, f"Expected 401/403, got HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Auth Required", False, f"Request failed: {str(e)}")
        
        # Test admin endpoints with valid authentication
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            admin_auth_tests_passed = 0
            
            for endpoint, name in admin_endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list):
                            self.log_test(f"{name} With Auth", True, f"Admin endpoint accessible with valid authentication")
                            admin_auth_tests_passed += 1
                        else:
                            self.log_test(f"{name} With Auth", False, f"Expected list response, got: {type(data)}")
                    else:
                        self.log_test(f"{name} With Auth", False, f"HTTP {response.status_code}: {response.text}")
                except Exception as e:
                    self.log_test(f"{name} With Auth", False, f"Request failed: {str(e)}")
            
            total_auth_tests = len(public_endpoints) + len(admin_endpoints) + len(admin_endpoints)
            total_passed = public_tests_passed + auth_tests_passed + admin_auth_tests_passed
            
            self.log_test("CMS Authentication Overall", total_passed == total_auth_tests, 
                         f"Authentication tests: {total_passed}/{total_auth_tests} passed")
            
            return total_passed == total_auth_tests
        else:
            self.log_test("CMS Authentication Overall", False, "No admin token available for authentication tests")
            return False

    def test_cms_data_validation(self):
        """Test data validation for CMS endpoints"""
        if not self.admin_token:
            self.log_test("CMS Data Validation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        validation_tests_passed = 0
        total_validation_tests = 0
        
        # Test Team Member validation
        try:
            total_validation_tests += 1
            # Test missing required fields
            invalid_team_data = {
                "position": "Developer"  # Missing name (required)
            }
            
            response = self.session.post(f"{self.content_url}/admin/team", json=invalid_team_data, headers=headers)
            if response.status_code == 422:  # Validation error
                self.log_test("Team Validation - Missing Required Fields", True, "Correctly rejected team member with missing required fields")
                validation_tests_passed += 1
            else:
                self.log_test("Team Validation - Missing Required Fields", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Team Validation - Missing Required Fields", False, f"Request failed: {str(e)}")
        
        # Test Testimonial validation
        try:
            total_validation_tests += 1
            # Test invalid rating (should be 1-5)
            invalid_testimonial_data = {
                "clientName": "Test Client",
                "clientCompany": "Test Company",
                "content": "Great service!",
                "rating": 6  # Invalid rating (should be 1-5)
            }
            
            response = self.session.post(f"{self.content_url}/admin/testimonials", json=invalid_testimonial_data, headers=headers)
            if response.status_code == 422:  # Validation error
                self.log_test("Testimonial Validation - Invalid Rating", True, "Correctly rejected testimonial with invalid rating")
                validation_tests_passed += 1
            else:
                self.log_test("Testimonial Validation - Invalid Rating", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Testimonial Validation - Invalid Rating", False, f"Request failed: {str(e)}")
        
        # Test FAQ validation
        try:
            total_validation_tests += 1
            # Test empty question
            invalid_faq_data = {
                "question": "",  # Empty question
                "answer": "This is an answer",
                "category": "General"
            }
            
            response = self.session.post(f"{self.content_url}/admin/faqs", json=invalid_faq_data, headers=headers)
            if response.status_code == 422:  # Validation error
                self.log_test("FAQ Validation - Empty Question", True, "Correctly rejected FAQ with empty question")
                validation_tests_passed += 1
            else:
                self.log_test("FAQ Validation - Empty Question", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("FAQ Validation - Empty Question", False, f"Request failed: {str(e)}")
        
        self.log_test("CMS Data Validation Overall", validation_tests_passed == total_validation_tests, 
                     f"Data validation tests: {validation_tests_passed}/{total_validation_tests} passed")
        
        return validation_tests_passed == total_validation_tests

    def test_cms_error_handling(self):
        """Test error handling for invalid IDs in CMS endpoints"""
        if not self.admin_token:
            self.log_test("CMS Error Handling", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        error_tests_passed = 0
        total_error_tests = 0
        
        invalid_id = "invalid-id-12345"
        
        # Test invalid ID handling for each CMS section
        endpoints_to_test = [
            (f"/content/admin/team/{invalid_id}", "PUT", {"name": "Updated Name"}, "Team Update Invalid ID"),
            (f"/content/admin/team/{invalid_id}", "DELETE", None, "Team Delete Invalid ID"),
            (f"/content/admin/testimonials/{invalid_id}", "PUT", {"content": "Updated content"}, "Testimonial Update Invalid ID"),
            (f"/content/admin/testimonials/{invalid_id}", "DELETE", None, "Testimonial Delete Invalid ID"),
            (f"/content/admin/faqs/{invalid_id}", "PUT", {"answer": "Updated answer"}, "FAQ Update Invalid ID"),
            (f"/content/admin/faqs/{invalid_id}", "DELETE", None, "FAQ Delete Invalid ID")
        ]
        
        for endpoint, method, data, test_name in endpoints_to_test:
            try:
                total_error_tests += 1
                
                if method == "PUT":
                    response = self.session.put(f"{self.base_url}{endpoint}", json=data, headers=headers)
                elif method == "DELETE":
                    response = self.session.delete(f"{self.base_url}{endpoint}", headers=headers)
                
                if response.status_code == 404:
                    self.log_test(test_name, True, f"Correctly returned 404 for invalid ID")
                    error_tests_passed += 1
                else:
                    self.log_test(test_name, False, f"Expected 404, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_name, False, f"Request failed: {str(e)}")
        
        self.log_test("CMS Error Handling Overall", error_tests_passed == total_error_tests, 
                     f"Error handling tests: {error_tests_passed}/{total_error_tests} passed")
        
        return error_tests_passed == total_error_tests

    def run_cms_extensions_tests(self):
        """Run all CMS Extensions tests"""
        print("\n🏗️  CMS EXTENSIONS TESTS")
        print("=" * 50)
        
        # Test authentication and authorization
        self.test_cms_authentication_and_authorization()
        
        # Test CRUD operations for each CMS section
        self.test_team_crud()
        self.test_testimonials_crud()
        self.test_faqs_crud()
        
        # Test data validation
        self.test_cms_data_validation()
        
        # Test error handling
        self.test_cms_error_handling()

    def run_all_tests(self):
        """Run all tests including CMS Extensions"""
        print(f"🚀 Starting CMS Extensions Testing")
        print(f"Backend URL: {self.base_url}")
        print(f"Content URL: {self.content_url}")
        print(f"Testing new Team, Testimonials, and FAQ management endpoints")
        print("=" * 70)
        
        # Test admin authentication with demo credentials
        if not self.test_admin_login():
            print("❌ Admin login failed - cannot proceed with CMS tests")
            return False
        
        print(f"✅ Admin login successful with token: {self.admin_token[:20]}...")
        
        # Test CMS Extensions
        self.run_cms_extensions_tests()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 CMS EXTENSIONS TEST SUMMARY")
        print("=" * 70)
        
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
        else:
            print("\n✅ ALL TESTS PASSED!")
            print("🎉 CMS Extensions are working correctly!")
            print("📝 Team, Testimonials, and FAQ management fully functional")
        
        return passed == total

    # ===== MARKETING SYSTEM TESTS =====
    
    def test_newsletter_subscription(self):
        """Test newsletter subscription endpoint"""
        try:
            # Test valid subscription
            subscription_data = {
                "email": "test.newsletter@example.com",
                "name": "Test Newsletter User",
                "source": "website",
                "tags": ["marketing", "test"]
            }
            
            response = self.session.post(f"{self.marketing_url}/newsletter/subscribe", json=subscription_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Newsletter Subscription", True, "Successfully subscribed to newsletter")
                    
                    # Test duplicate subscription
                    duplicate_response = self.session.post(f"{self.marketing_url}/newsletter/subscribe", json=subscription_data)
                    if duplicate_response.status_code == 200:
                        duplicate_result = duplicate_response.json()
                        if not duplicate_result.get("success"):
                            self.log_test("Newsletter Duplicate Prevention", True, "Correctly prevented duplicate subscription")
                        else:
                            self.log_test("Newsletter Duplicate Prevention", False, "Should prevent duplicate subscriptions")
                    
                    return True
                else:
                    self.log_test("Newsletter Subscription", False, f"Subscription failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Newsletter Subscription", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Newsletter Subscription", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_newsletter_unsubscribe(self):
        """Test newsletter unsubscription endpoint"""
        try:
            # First subscribe
            subscription_data = {
                "email": "test.unsubscribe@example.com",
                "name": "Test Unsubscribe User"
            }
            
            subscribe_response = self.session.post(f"{self.marketing_url}/newsletter/subscribe", json=subscription_data)
            if subscribe_response.status_code == 200 and subscribe_response.json().get("success"):
                
                # Now unsubscribe
                unsubscribe_data = {"email": "test.unsubscribe@example.com"}
                response = self.session.post(f"{self.marketing_url}/newsletter/unsubscribe", json=unsubscribe_data)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        self.log_test("Newsletter Unsubscribe", True, "Successfully unsubscribed from newsletter")
                        return True
                    else:
                        self.log_test("Newsletter Unsubscribe", False, f"Unsubscribe failed: {result.get('message', 'Unknown error')}")
                else:
                    self.log_test("Newsletter Unsubscribe", False, f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test("Newsletter Unsubscribe", False, "Failed to create test subscription")
                
        except Exception as e:
            self.log_test("Newsletter Unsubscribe", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_newsletter_admin_list(self):
        """Test admin newsletter subscribers list"""
        if not self.admin_token:
            self.log_test("Newsletter Admin List", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test getting all subscribers
            response = self.session.get(f"{self.marketing_url}/admin/newsletter/subscribers", headers=headers)
            
            if response.status_code == 200:
                subscribers = response.json()
                if isinstance(subscribers, list):
                    self.log_test("Newsletter Admin List", True, f"Successfully retrieved {len(subscribers)} newsletter subscribers")
                    
                    # Test active only filter
                    active_response = self.session.get(f"{self.marketing_url}/admin/newsletter/subscribers?active_only=true", headers=headers)
                    if active_response.status_code == 200:
                        active_subscribers = active_response.json()
                        if isinstance(active_subscribers, list):
                            self.log_test("Newsletter Active Filter", True, f"Successfully filtered {len(active_subscribers)} active subscribers")
                            return True
                        else:
                            self.log_test("Newsletter Active Filter", False, f"Expected list, got: {type(active_subscribers)}")
                    else:
                        self.log_test("Newsletter Active Filter", False, f"HTTP {active_response.status_code}: {active_response.text}")
                else:
                    self.log_test("Newsletter Admin List", False, f"Expected list, got: {type(subscribers)}")
            else:
                self.log_test("Newsletter Admin List", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Newsletter Admin List", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_lead_capture(self):
        """Test lead capture endpoint"""
        try:
            lead_data = {
                "email": "test.lead@example.com",
                "name": "Test Lead User",
                "phone": "+90 555 123 4567",
                "company": "Test Company Ltd",
                "message": "Trendyol mağaza optimizasyonu hakkında bilgi almak istiyorum",
                "source": "contact_form",
                "utm_source": "google",
                "utm_medium": "cpc",
                "utm_campaign": "trendyol_optimization"
            }
            
            response = self.session.post(f"{self.marketing_url}/leads/capture", json=lead_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Lead Capture", True, "Successfully captured lead information")
                    return True
                else:
                    self.log_test("Lead Capture", False, f"Lead capture failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Lead Capture", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Lead Capture", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_leads_admin_list(self):
        """Test admin leads list"""
        if not self.admin_token:
            self.log_test("Leads Admin List", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test getting all leads
            response = self.session.get(f"{self.marketing_url}/admin/leads", headers=headers)
            
            if response.status_code == 200:
                leads = response.json()
                if isinstance(leads, list):
                    self.log_test("Leads Admin List", True, f"Successfully retrieved {len(leads)} leads")
                    
                    # Test unprocessed only filter
                    unprocessed_response = self.session.get(f"{self.marketing_url}/admin/leads?unprocessed_only=true", headers=headers)
                    if unprocessed_response.status_code == 200:
                        unprocessed_leads = unprocessed_response.json()
                        if isinstance(unprocessed_leads, list):
                            self.log_test("Leads Unprocessed Filter", True, f"Successfully filtered {len(unprocessed_leads)} unprocessed leads")
                            return True
                        else:
                            self.log_test("Leads Unprocessed Filter", False, f"Expected list, got: {type(unprocessed_leads)}")
                    else:
                        self.log_test("Leads Unprocessed Filter", False, f"HTTP {unprocessed_response.status_code}: {unprocessed_response.text}")
                else:
                    self.log_test("Leads Admin List", False, f"Expected list, got: {type(leads)}")
            else:
                self.log_test("Leads Admin List", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Leads Admin List", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_lead_processing(self):
        """Test marking leads as processed"""
        if not self.admin_token:
            self.log_test("Lead Processing", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # First create a test lead
            lead_data = {
                "email": "test.process@example.com",
                "name": "Test Process Lead",
                "message": "Test lead for processing"
            }
            
            create_response = self.session.post(f"{self.marketing_url}/leads/capture", json=lead_data)
            if create_response.status_code == 200 and create_response.json().get("success"):
                
                # Get the lead ID from admin list
                leads_response = self.session.get(f"{self.marketing_url}/admin/leads", headers=headers)
                if leads_response.status_code == 200:
                    leads = leads_response.json()
                    test_lead = None
                    for lead in leads:
                        if lead.get("email") == "test.process@example.com":
                            test_lead = lead
                            break
                    
                    if test_lead:
                        lead_id = test_lead.get("id")
                        
                        # Process the lead
                        process_response = self.session.put(f"{self.marketing_url}/admin/leads/{lead_id}/process", headers=headers)
                        
                        if process_response.status_code == 200:
                            result = process_response.json()
                            if result.get("success"):
                                self.log_test("Lead Processing", True, "Successfully marked lead as processed")
                                return True
                            else:
                                self.log_test("Lead Processing", False, f"Processing failed: {result.get('message', 'Unknown error')}")
                        else:
                            self.log_test("Lead Processing", False, f"HTTP {process_response.status_code}: {process_response.text}")
                    else:
                        self.log_test("Lead Processing", False, "Could not find test lead in admin list")
                else:
                    self.log_test("Lead Processing", False, "Failed to retrieve leads list")
            else:
                self.log_test("Lead Processing", False, "Failed to create test lead")
                
        except Exception as e:
            self.log_test("Lead Processing", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_page_view_tracking(self):
        """Test page view analytics tracking"""
        try:
            page_view_data = {
                "path": "/",
                "sessionId": "test_session_123",
                "userId": "test_user_456",
                "loadTime": 1.25,
                "device": "desktop",
                "browser": "Chrome",
                "country": "TR"
            }
            
            response = self.session.post(f"{self.marketing_url}/analytics/page-view", json=page_view_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Page View Tracking", True, "Successfully tracked page view")
                    return True
                else:
                    self.log_test("Page View Tracking", False, f"Tracking failed: {result}")
            else:
                self.log_test("Page View Tracking", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Page View Tracking", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_event_tracking(self):
        """Test analytics event tracking"""
        try:
            event_data = {
                "eventType": "button_click",
                "eventCategory": "engagement",
                "eventLabel": "contact_form_submit",
                "eventValue": 1.0,
                "userId": "test_user_456",
                "sessionId": "test_session_123",
                "metadata": {
                    "button_text": "İletişime Geç",
                    "page": "/iletisim"
                }
            }
            
            response = self.session.post(f"{self.marketing_url}/analytics/event", json=event_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Event Tracking", True, "Successfully tracked analytics event")
                    return True
                else:
                    self.log_test("Event Tracking", False, f"Tracking failed: {result}")
            else:
                self.log_test("Event Tracking", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Event Tracking", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_analytics_dashboard(self):
        """Test analytics dashboard data"""
        if not self.admin_token:
            self.log_test("Analytics Dashboard", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test default dashboard (30 days)
            response = self.session.get(f"{self.marketing_url}/admin/analytics/dashboard", headers=headers)
            
            if response.status_code == 200:
                dashboard_data = response.json()
                expected_fields = ["total_page_views", "newsletter_subscribers", "new_leads", "top_pages", "period_days"]
                
                if all(field in dashboard_data for field in expected_fields):
                    self.log_test("Analytics Dashboard", True, f"Successfully retrieved dashboard data with all expected fields")
                    
                    # Test custom period
                    custom_response = self.session.get(f"{self.marketing_url}/admin/analytics/dashboard?days=7", headers=headers)
                    if custom_response.status_code == 200:
                        custom_data = custom_response.json()
                        if custom_data.get("period_days") == 7:
                            self.log_test("Analytics Custom Period", True, "Successfully retrieved 7-day analytics data")
                            return True
                        else:
                            self.log_test("Analytics Custom Period", False, f"Expected 7 days, got {custom_data.get('period_days')}")
                    else:
                        self.log_test("Analytics Custom Period", False, f"HTTP {custom_response.status_code}: {custom_response.text}")
                else:
                    missing_fields = [field for field in expected_fields if field not in dashboard_data]
                    self.log_test("Analytics Dashboard", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Analytics Dashboard", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Analytics Dashboard", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_whatsapp_message(self):
        """Test WhatsApp message link generation"""
        if not self.admin_token:
            self.log_test("WhatsApp Message", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            whatsapp_data = {
                "phone": "+90 555 123 4567",
                "message": "Merhaba! Trendyol mağaza optimizasyonu hakkında bilgi almak istiyorum."
            }
            
            response = self.session.post(f"{self.marketing_url}/whatsapp/send-message", json=whatsapp_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("whatsapp_url"):
                    whatsapp_url = result["whatsapp_url"]
                    if "wa.me" in whatsapp_url and "905551234567" in whatsapp_url:
                        self.log_test("WhatsApp Message", True, "Successfully generated WhatsApp link with correct phone format")
                        return True
                    else:
                        self.log_test("WhatsApp Message", False, f"Invalid WhatsApp URL format: {whatsapp_url}")
                else:
                    self.log_test("WhatsApp Message", False, f"Failed to generate link: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("WhatsApp Message", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("WhatsApp Message", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_sitemap_generation(self):
        """Test sitemap generation"""
        try:
            response = self.session.get(f"{self.marketing_url}/sitemap")
            
            if response.status_code == 200:
                sitemap_data = response.json()
                if "urls" in sitemap_data and isinstance(sitemap_data["urls"], list):
                    urls = sitemap_data["urls"]
                    
                    # Check for expected static URLs
                    expected_paths = ["/", "/haber", "/projelerimiz", "/takimim", "/referanslar", "/sss", "/iletisim"]
                    found_paths = [url["loc"] for url in urls if url["loc"] in expected_paths]
                    
                    if len(found_paths) >= 5:  # At least 5 out of 7 expected paths
                        self.log_test("Sitemap Generation", True, f"Successfully generated sitemap with {len(urls)} URLs including {len(found_paths)} expected paths")
                        return True
                    else:
                        self.log_test("Sitemap Generation", False, f"Missing expected paths. Found: {found_paths}")
                else:
                    self.log_test("Sitemap Generation", False, f"Invalid sitemap format: {sitemap_data}")
            else:
                self.log_test("Sitemap Generation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Sitemap Generation", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_enhanced_site_settings(self):
        """Test enhanced site settings with all new fields"""
        if not self.admin_token:
            self.log_test("Enhanced Site Settings", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test comprehensive site settings update
            enhanced_settings = {
                "siteName": "Skywalker.tc",
                "siteDescription": "Trendyol E-ticaret Danışmanlık ve Pazarlama Hizmetleri",
                "contactEmail": "info@skywalker.tc",
                "contactPhone": "+90 555 123 45 67",
                
                # SEO fields
                "metaTitle": "Skywalker.tc - Trendyol E-ticaret Uzmanları",
                "metaDescription": "Trendyol mağaza optimizasyonu, reklam yönetimi ve e-ticaret danışmanlığı hizmetleri",
                "metaKeywords": ["trendyol", "e-ticaret", "optimizasyon", "reklam"],
                
                # Analytics IDs
                "googleAnalyticsId": "GA-123456789",
                "facebookPixelId": "FB-987654321",
                "googleTagManagerId": "GTM-ABCD123",
                
                # Verification codes
                "googleVerificationCode": "google-site-verification=abc123",
                "metaVerificationCode": "meta-domain-verification=def456",
                
                # Social media settings
                "ogTitle": "Skywalker.tc - E-ticaret Galaksisinde Rehberiniz",
                "ogDescription": "Trendyol'da başarıya ulaşmanız için profesyonel danışmanlık",
                "twitterSite": "@skywalker_tc",
                
                # Business settings
                "whatsappNumber": "+90 555 123 45 67",
                "liveChatEnabled": True,
                "newsletterEnabled": True,
                "cookieConsentEnabled": True
            }
            
            # Update site settings
            response = self.session.put(f"{self.content_url}/admin/site-settings", json=enhanced_settings, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Enhanced Site Settings Update", True, "Successfully updated enhanced site settings")
                    
                    # Verify the update by getting settings
                    verify_response = self.session.get(f"{self.content_url}/site-settings")
                    if verify_response.status_code == 200:
                        updated_settings = verify_response.json()
                        
                        # Check key enhanced fields
                        enhanced_fields = ["metaTitle", "googleAnalyticsId", "whatsappNumber", "ogTitle"]
                        found_fields = [field for field in enhanced_fields if field in updated_settings and updated_settings[field]]
                        
                        if len(found_fields) >= 3:  # At least 3 out of 4 enhanced fields
                            self.log_test("Enhanced Site Settings Verification", True, f"Verified {len(found_fields)}/4 enhanced fields are saved correctly")
                            return True
                        else:
                            self.log_test("Enhanced Site Settings Verification", False, f"Enhanced fields not properly saved. Found: {found_fields}")
                    else:
                        self.log_test("Enhanced Site Settings Verification", False, f"Verification failed: HTTP {verify_response.status_code}")
                else:
                    self.log_test("Enhanced Site Settings Update", False, f"Update failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Enhanced Site Settings Update", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Enhanced Site Settings", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_data_validation(self):
        """Test data validation for marketing endpoints"""
        validation_tests_passed = 0
        total_validation_tests = 0
        
        try:
            # Test 1: Newsletter subscription with invalid email
            total_validation_tests += 1
            invalid_email_data = {"email": "invalid-email", "name": "Test User"}
            response = self.session.post(f"{self.marketing_url}/newsletter/subscribe", json=invalid_email_data)
            if response.status_code == 422:  # Pydantic validation error
                self.log_test("Newsletter Email Validation", True, "Correctly rejected invalid email format")
                validation_tests_passed += 1
            else:
                self.log_test("Newsletter Email Validation", False, f"Expected 422, got {response.status_code}")
            
            # Test 2: Lead capture with missing required email
            total_validation_tests += 1
            missing_email_data = {"name": "Test User", "message": "Test message"}
            response = self.session.post(f"{self.marketing_url}/leads/capture", json=missing_email_data)
            if response.status_code == 422:
                self.log_test("Lead Email Required Validation", True, "Correctly rejected missing email field")
                validation_tests_passed += 1
            else:
                self.log_test("Lead Email Required Validation", False, f"Expected 422, got {response.status_code}")
            
            # Test 3: Analytics event with missing eventType
            total_validation_tests += 1
            missing_event_type = {"eventCategory": "test", "eventLabel": "test"}
            response = self.session.post(f"{self.marketing_url}/analytics/event", json=missing_event_type)
            if response.status_code == 422:
                self.log_test("Event Type Required Validation", True, "Correctly rejected missing eventType field")
                validation_tests_passed += 1
            else:
                self.log_test("Event Type Required Validation", False, f"Expected 422, got {response.status_code}")
            
            success_rate = (validation_tests_passed / total_validation_tests) * 100 if total_validation_tests > 0 else 0
            overall_success = validation_tests_passed == total_validation_tests
            
            self.log_test("Data Validation Overall", overall_success, 
                         f"Validation tests: {validation_tests_passed}/{total_validation_tests} passed ({success_rate:.1f}%)")
            
            return overall_success
            
        except Exception as e:
            self.log_test("Data Validation", False, f"Validation tests failed: {str(e)}")
        
        return False
    
    def test_authentication_security(self):
        """Test authentication requirements for admin endpoints"""
        security_tests_passed = 0
        total_security_tests = 0
        
        try:
            # Test admin endpoints without authentication
            admin_endpoints = [
                f"{self.marketing_url}/admin/newsletter/subscribers",
                f"{self.marketing_url}/admin/leads",
                f"{self.marketing_url}/admin/analytics/dashboard"
            ]
            
            for endpoint in admin_endpoints:
                total_security_tests += 1
                response = self.session.get(endpoint)  # No auth headers
                if response.status_code in [401, 403]:
                    endpoint_name = endpoint.split("/")[-1]
                    self.log_test(f"Auth Required - {endpoint_name}", True, f"Correctly blocked unauthorized access (HTTP {response.status_code})")
                    security_tests_passed += 1
                else:
                    endpoint_name = endpoint.split("/")[-1]
                    self.log_test(f"Auth Required - {endpoint_name}", False, f"Expected 401/403, got {response.status_code}")
            
            # Test WhatsApp endpoint without auth
            total_security_tests += 1
            whatsapp_data = {"phone": "+90 555 123 4567", "message": "Test"}
            response = self.session.post(f"{self.marketing_url}/whatsapp/send-message", json=whatsapp_data)
            if response.status_code in [401, 403]:
                self.log_test("Auth Required - WhatsApp", True, f"Correctly blocked unauthorized WhatsApp access (HTTP {response.status_code})")
                security_tests_passed += 1
            else:
                self.log_test("Auth Required - WhatsApp", False, f"Expected 401/403, got {response.status_code}")
            
            success_rate = (security_tests_passed / total_security_tests) * 100 if total_security_tests > 0 else 0
            overall_success = security_tests_passed == total_security_tests
            
            self.log_test("Authentication Security Overall", overall_success, 
                         f"Security tests: {security_tests_passed}/{total_security_tests} passed ({success_rate:.1f}%)")
            
            return overall_success
            
        except Exception as e:
            self.log_test("Authentication Security", False, f"Security tests failed: {str(e)}")
        
        return False
    
    def run_marketing_system_tests(self):
        """Run comprehensive marketing and analytics system tests"""
        print("\n🚀 MARKETING & ANALYTICS SYSTEM TESTS")
        print("=" * 50)
        
        # Test authentication first
        if not self.test_admin_login():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        marketing_tests = []
        
        # Newsletter System Tests
        print("\n📧 NEWSLETTER SYSTEM TESTS")
        print("-" * 30)
        marketing_tests.append(self.test_newsletter_subscription())
        marketing_tests.append(self.test_newsletter_unsubscribe())
        marketing_tests.append(self.test_newsletter_admin_list())
        
        # Lead Capture Tests
        print("\n🎯 LEAD CAPTURE SYSTEM TESTS")
        print("-" * 30)
        marketing_tests.append(self.test_lead_capture())
        marketing_tests.append(self.test_leads_admin_list())
        marketing_tests.append(self.test_lead_processing())
        
        # Analytics Tests
        print("\n📊 ANALYTICS SYSTEM TESTS")
        print("-" * 30)
        marketing_tests.append(self.test_page_view_tracking())
        marketing_tests.append(self.test_event_tracking())
        marketing_tests.append(self.test_analytics_dashboard())
        
        # Additional Marketing Features
        print("\n💬 ADDITIONAL MARKETING FEATURES")
        print("-" * 30)
        marketing_tests.append(self.test_whatsapp_message())
        marketing_tests.append(self.test_sitemap_generation())
        
        # Enhanced Site Settings
        print("\n⚙️ ENHANCED SITE SETTINGS TESTS")
        print("-" * 30)
        marketing_tests.append(self.test_enhanced_site_settings())
        
        # Data Validation & Security
        print("\n🔒 DATA VALIDATION & SECURITY TESTS")
        print("-" * 30)
        marketing_tests.append(self.test_data_validation())
        marketing_tests.append(self.test_authentication_security())
        
        # Calculate results
        passed = sum(marketing_tests)
        total = len(marketing_tests)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"\n📈 MARKETING SYSTEM TEST RESULTS")
        print("=" * 40)
        print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL MARKETING TESTS PASSED!")
            print("✅ Newsletter system functional")
            print("✅ Lead capture system operational")
            print("✅ Analytics tracking working")
            print("✅ WhatsApp integration ready")
            print("✅ Enhanced site settings working")
            print("✅ Data validation and security verified")
        else:
            print(f"\n⚠️ {total - passed} tests failed - see details above")
        
        return passed == total

if __name__ == "__main__":
    tester = AdminPanelAuthorizationTester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        # Clean up test data
        tester.cleanup_test_data()