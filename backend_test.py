#!/usr/bin/env python3
"""
Admin Panel Authorization Bug Fix Testing
Tests the authorization bug fix for admin panel content loading endpoints
"""

import requests
import json
import sys
import io
from datetime import datetime
from PIL import Image

# Backend URL from frontend .env
BASE_URL = "https://b2b-manager-1.preview.emergentagent.com/api"
PORTAL_URL = "https://b2b-manager-1.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://b2b-manager-1.preview.emergentagent.com/api/content"
FILES_URL = "https://b2b-manager-1.preview.emergentagent.com/api/files"

class AdminPanelAuthorizationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.content_url = CONTENT_URL
        self.files_url = FILES_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_items = {
            'site_content': [],
            'news': [],
            'projects': [],
            'files': []
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
        for file_id in self.created_items['files']:
            try:
                response = self.session.delete(f"{self.files_url}/{file_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
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

    def run_all_tests(self):
        """Run all admin panel authorization bug fix tests"""
        print(f"🚀 Starting Admin Panel Authorization Bug Fix Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"Content URL: {self.content_url}")
        print(f"Testing Authorization: Bearer <token> header format")
        print("=" * 70)
        
        # Test admin authentication with demo credentials
        if not self.test_admin_login():
            print("❌ Admin login failed - cannot proceed with authorization tests")
            return False
        
        print(f"✅ Admin login successful with token: {self.admin_token[:20]}...")
        
        # Test the specific authorization endpoints that were fixed
        print("\n🔐 TESTING AUTHORIZATION BUG FIX")
        print("=" * 50)
        self.test_admin_content_endpoints_authorization()
        
        # Test the complete admin panel workflow
        print("\n📋 TESTING COMPLETE ADMIN PANEL WORKFLOW")
        print("=" * 50)
        self.test_full_admin_panel_workflow()
        
        # Test CRUD operations to ensure everything works end-to-end
        print("\n🔄 TESTING CRUD OPERATIONS")
        print("=" * 50)
        self.test_site_content_crud()
        self.test_news_crud()
        self.test_projects_crud()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 AUTHORIZATION BUG FIX TEST SUMMARY")
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
            print("🎉 Authorization bug fix is working correctly!")
            print("📝 Admin panel can now load existing content for editing")
        
        return passed == total

if __name__ == "__main__":
    tester = AdminPanelAuthorizationTester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        # Clean up test data
        tester.cleanup_test_data()