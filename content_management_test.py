#!/usr/bin/env python3
"""
Content Management API Endpoint Testing
Tests all content management endpoints including site content, news, and projects
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://galactic-admin.preview.emergentagent.com/api"

class ContentManagementTester:
    def __init__(self):
        self.base_url = BASE_URL
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
    
    def admin_login(self):
        """Login as admin to get authentication token"""
        login_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            # Try portal login first
            response = self.session.post(f"{self.base_url}/portal/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.admin_token = data["access_token"]
                    self.log_test("Admin Login", True, "Successfully logged in as admin")
                    return True
                else:
                    self.log_test("Admin Login", False, "No access token received")
            else:
                self.log_test("Admin Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def get_auth_headers(self):
        """Get authorization headers for admin requests"""
        if not self.admin_token:
            return {}
        return {"Authorization": f"Bearer {self.admin_token}"}
    
    # Site Content Management Tests
    def test_get_site_content_public(self):
        """Test GET /api/content/site-content (public endpoint)"""
        try:
            response = self.session.get(f"{self.base_url}/content/site-content")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Site Content (Public)", True, f"Successfully retrieved {len(data)} site content items")
                    return True
                else:
                    self.log_test("Get Site Content (Public)", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("Get Site Content (Public)", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Site Content (Public)", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_site_content(self):
        """Test POST /api/content/admin/site-content (admin only)"""
        if not self.admin_token:
            self.log_test("Create Site Content", False, "No admin token available")
            return False
        
        content_data = {
            "section": "hero_section",
            "key": "main_title",
            "title": "Trendyol Galaksisinde Liderlik",
            "content": "E-ticaret dünyasında rehberiniz oluyoruz",
            "order": 1
        }
        
        try:
            headers = self.get_auth_headers()
            response = self.session.post(f"{self.base_url}/content/admin/site-content", json=content_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    content_id = data.get("id")
                    if content_id:
                        self.created_items['site_content'].append(content_id)
                    self.log_test("Create Site Content", True, "Successfully created site content")
                    return True
                else:
                    self.log_test("Create Site Content", False, f"Creation failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Site Content", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Site Content", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_update_site_content(self):
        """Test PUT /api/content/admin/site-content/{id} (admin only)"""
        if not self.admin_token or not self.created_items['site_content']:
            self.log_test("Update Site Content", False, "No admin token or site content ID available")
            return False
        
        content_id = self.created_items['site_content'][0]
        update_data = {
            "title": "Trendyol Galaksisinde Liderlik - Güncellenmiş",
            "content": "E-ticaret dünyasında rehberiniz oluyoruz - Yeni içerik"
        }
        
        try:
            headers = self.get_auth_headers()
            response = self.session.put(f"{self.base_url}/content/admin/site-content/{content_id}", json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Site Content", True, "Successfully updated site content")
                    return True
                else:
                    self.log_test("Update Site Content", False, f"Update failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Update Site Content", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Update Site Content", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_delete_site_content(self):
        """Test DELETE /api/content/admin/site-content/{id} (admin only)"""
        if not self.admin_token or not self.created_items['site_content']:
            self.log_test("Delete Site Content", False, "No admin token or site content ID available")
            return False
        
        content_id = self.created_items['site_content'][0]
        
        try:
            headers = self.get_auth_headers()
            response = self.session.delete(f"{self.base_url}/content/admin/site-content/{content_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Delete Site Content", True, "Successfully deleted site content")
                    return True
                else:
                    self.log_test("Delete Site Content", False, f"Deletion failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Delete Site Content", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Delete Site Content", False, f"Request failed: {str(e)}")
        
        return False
    
    # News System Tests
    def test_get_news_public(self):
        """Test GET /api/content/news (public endpoint)"""
        try:
            response = self.session.get(f"{self.base_url}/content/news")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get News (Public)", True, f"Successfully retrieved {len(data)} news articles")
                    return True
                else:
                    self.log_test("Get News (Public)", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("Get News (Public)", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get News (Public)", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_news_article(self):
        """Test POST /api/content/admin/news (admin only)"""
        if not self.admin_token:
            self.log_test("Create News Article", False, "No admin token available")
            return False
        
        news_data = {
            "title": "Yeni Dijital Pazarlama Stratejileri",
            "content": "2024 yılında e-ticaret sektöründeki en son trend ve stratejiler...",
            "excerpt": "E-ticaret dünyasında başarıya giden yollar",
            "category": "industry_news",
            "isPublished": True
        }
        
        try:
            headers = self.get_auth_headers()
            response = self.session.post(f"{self.base_url}/content/admin/news", json=news_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    news_id = data.get("id")
                    if news_id:
                        self.created_items['news'].append(news_id)
                    self.log_test("Create News Article", True, "Successfully created news article")
                    return True
                else:
                    self.log_test("Create News Article", False, f"Creation failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Create News Article", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create News Article", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_get_news_article_detail(self):
        """Test GET /api/content/news/{id} (public endpoint)"""
        if not self.created_items['news']:
            self.log_test("Get News Article Detail", False, "No news article ID available")
            return False
        
        news_id = self.created_items['news'][0]
        
        try:
            response = self.session.get(f"{self.base_url}/content/news/{news_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("id") == news_id:
                    self.log_test("Get News Article Detail", True, "Successfully retrieved news article detail")
                    return True
                else:
                    self.log_test("Get News Article Detail", False, f"Unexpected article data: {data}")
            else:
                self.log_test("Get News Article Detail", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get News Article Detail", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_update_news_article(self):
        """Test PUT /api/content/admin/news/{id} (admin only)"""
        if not self.admin_token or not self.created_items['news']:
            self.log_test("Update News Article", False, "No admin token or news article ID available")
            return False
        
        news_id = self.created_items['news'][0]
        update_data = {
            "title": "Yeni Dijital Pazarlama Stratejileri - Güncellenmiş",
            "content": "2024 yılında e-ticaret sektöründeki en son trend ve stratejiler - Güncellenmiş içerik..."
        }
        
        try:
            headers = self.get_auth_headers()
            response = self.session.put(f"{self.base_url}/content/admin/news/{news_id}", json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update News Article", True, "Successfully updated news article")
                    return True
                else:
                    self.log_test("Update News Article", False, f"Update failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Update News Article", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Update News Article", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_delete_news_article(self):
        """Test DELETE /api/content/admin/news/{id} (admin only)"""
        if not self.admin_token or not self.created_items['news']:
            self.log_test("Delete News Article", False, "No admin token or news article ID available")
            return False
        
        news_id = self.created_items['news'][0]
        
        try:
            headers = self.get_auth_headers()
            response = self.session.delete(f"{self.base_url}/content/admin/news/{news_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Delete News Article", True, "Successfully deleted news article")
                    return True
                else:
                    self.log_test("Delete News Article", False, f"Deletion failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Delete News Article", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Delete News Article", False, f"Request failed: {str(e)}")
        
        return False
    
    # Company Projects Tests
    def test_get_projects_public(self):
        """Test GET /api/content/projects (public endpoint)"""
        try:
            response = self.session.get(f"{self.base_url}/content/projects")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Projects (Public)", True, f"Successfully retrieved {len(data)} company projects")
                    return True
                else:
                    self.log_test("Get Projects (Public)", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("Get Projects (Public)", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Projects (Public)", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_company_project(self):
        """Test POST /api/content/admin/projects (admin only)"""
        if not self.admin_token:
            self.log_test("Create Company Project", False, "No admin token available")
            return False
        
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
            headers = self.get_auth_headers()
            response = self.session.post(f"{self.base_url}/content/admin/projects", json=project_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    project_id = data.get("id")
                    if project_id:
                        self.created_items['projects'].append(project_id)
                    self.log_test("Create Company Project", True, "Successfully created company project")
                    return True
                else:
                    self.log_test("Create Company Project", False, f"Creation failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Company Project", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Company Project", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_get_project_detail(self):
        """Test GET /api/content/projects/{id} (public endpoint)"""
        if not self.created_items['projects']:
            self.log_test("Get Project Detail", False, "No project ID available")
            return False
        
        project_id = self.created_items['projects'][0]
        
        try:
            response = self.session.get(f"{self.base_url}/content/projects/{project_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("id") == project_id:
                    self.log_test("Get Project Detail", True, "Successfully retrieved project detail")
                    return True
                else:
                    self.log_test("Get Project Detail", False, f"Unexpected project data: {data}")
            else:
                self.log_test("Get Project Detail", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Project Detail", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_update_company_project(self):
        """Test PUT /api/content/admin/projects/{id} (admin only)"""
        if not self.admin_token or not self.created_items['projects']:
            self.log_test("Update Company Project", False, "No admin token or project ID available")
            return False
        
        project_id = self.created_items['projects'][0]
        update_data = {
            "projectTitle": "E-ticaret Optimizasyon Projesi - Güncellenmiş",
            "results": "Satışlar %200 arttı, ROI %300 gelişti - Güncellenmiş sonuçlar"
        }
        
        try:
            headers = self.get_auth_headers()
            response = self.session.put(f"{self.base_url}/content/admin/projects/{project_id}", json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Company Project", True, "Successfully updated company project")
                    return True
                else:
                    self.log_test("Update Company Project", False, f"Update failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Update Company Project", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Update Company Project", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_delete_company_project(self):
        """Test DELETE /api/content/admin/projects/{id} (admin only)"""
        if not self.admin_token or not self.created_items['projects']:
            self.log_test("Delete Company Project", False, "No admin token or project ID available")
            return False
        
        project_id = self.created_items['projects'][0]
        
        try:
            headers = self.get_auth_headers()
            response = self.session.delete(f"{self.base_url}/content/admin/projects/{project_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Delete Company Project", True, "Successfully deleted company project")
                    return True
                else:
                    self.log_test("Delete Company Project", False, f"Deletion failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_test("Delete Company Project", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Delete Company Project", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all content management tests in sequence"""
        print(f"🚀 Starting Content Management API Tests")
        print(f"Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Admin authentication
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Site Content Management Tests
        print("\n📄 SITE CONTENT MANAGEMENT TESTS")
        print("-" * 40)
        self.test_get_site_content_public()
        self.test_create_site_content()
        self.test_update_site_content()
        self.test_delete_site_content()
        
        # News System Tests
        print("\n📰 NEWS SYSTEM TESTS")
        print("-" * 40)
        self.test_get_news_public()
        self.test_create_news_article()
        self.test_get_news_article_detail()
        self.test_update_news_article()
        self.test_delete_news_article()
        
        # Company Projects Tests
        print("\n🏢 COMPANY PROJECTS TESTS")
        print("-" * 40)
        self.test_get_projects_public()
        self.test_create_company_project()
        self.test_get_project_detail()
        self.test_update_company_project()
        self.test_delete_company_project()
        
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
        
        return passed == total

if __name__ == "__main__":
    tester = ContentManagementTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)