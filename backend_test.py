#!/usr/bin/env python3
"""
Projects API Endpoint Debug Testing - Turkish Review Request
Debug GET /api/content/projects endpoint validation errors and database data analysis
"""

import requests
import json
import sys
import io
from datetime import datetime
from PIL import Image
import urllib.parse
import pymongo
from pymongo import MongoClient

# Backend URL from frontend .env
BASE_URL = "https://skywalker-portal-1.preview.emergentagent.com/api"
PORTAL_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/portal"
CONTENT_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/content"
FILES_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/files"
MARKETING_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/marketing"
PAYMENTS_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/payments"
SMS_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/sms"
EMPLOYEES_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/employees"
SUPPORT_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/support"
COMPANY_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/company"

class ProjectsAPIDebugTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.content_url = CONTENT_URL
        self.files_url = FILES_URL
        self.marketing_url = MARKETING_URL
        self.payments_url = PAYMENTS_URL
        self.sms_url = SMS_URL
        self.employees_url = EMPLOYEES_URL
        self.support_url = SUPPORT_URL
        self.company_url = COMPANY_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_items = {
            'employees': [],
            'support_tickets': [],
            'company_projects': [],
            'customer_profiles': [],
            'ticket_responses': [],
            'meeting_notes': [],
            'recurring_tasks': []
        }
        # MongoDB connection for direct database analysis
        self.mongo_client = None
        self.db = None
        
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
    
    # ===== KULLANICI YÖNETİM SİSTEMİ ANALİZİ =====
    
    def analyze_existing_users(self):
        """Mevcut kullanıcıları analiz et ve role distribution'ını hesapla"""
        if not self.admin_token:
            self.log_test("Kullanıcı Analizi", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Portal kullanıcılarını al
            response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
            
            if response.status_code == 200:
                users_data = response.json()
                users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                
                if isinstance(users, list):
                    # Role distribution analizi
                    role_distribution = {}
                    sample_users = {"admin": [], "influencer": [], "partner": []}
                    
                    for user in users:
                        role = user.get("role", "unknown")
                        role_distribution[role] = role_distribution.get(role, 0) + 1
                        
                        # Her role'den örnek kullanıcı topla
                        if role in sample_users and len(sample_users[role]) < 3:
                            sample_users[role].append({
                                "email": user.get("email", "N/A"),
                                "name": user.get("name", "N/A"),
                                "company": user.get("company", user.get("companyName", "N/A")),
                                "isApproved": user.get("isApproved", False),
                                "createdAt": user.get("createdAt", "N/A")
                            })
                    
                    total_users = len(users)
                    
                    # Sonuçları logla
                    self.log_test("Kullanıcı Role Dağılımı", True, 
                                f"Toplam {total_users} kullanıcı analiz edildi")
                    
                    print("\n📊 ROLE DISTRIBUTION ANALİZİ:")
                    print("=" * 40)
                    for role, count in role_distribution.items():
                        percentage = (count / total_users * 100) if total_users > 0 else 0
                        print(f"  {role.upper()}: {count} kullanıcı ({percentage:.1f}%)")
                    
                    print("\n👥 ÖRNEK KULLANICI VERİLERİ:")
                    print("=" * 40)
                    for role, user_list in sample_users.items():
                        if user_list:
                            print(f"\n{role.upper()} Kullanıcıları:")
                            for i, user in enumerate(user_list, 1):
                                print(f"  {i}. {user['email']} - {user['name']}")
                                if user['company'] != "N/A":
                                    print(f"     Şirket: {user['company']}")
                                print(f"     Onaylı: {'Evet' if user['isApproved'] else 'Hayır'}")
                    
                    return {
                        "total_users": total_users,
                        "role_distribution": role_distribution,
                        "sample_users": sample_users
                    }
                else:
                    self.log_test("Kullanıcı Analizi", False, f"Beklenmeyen veri formatı: {type(users)}")
            else:
                self.log_test("Kullanıcı Analizi", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Kullanıcı Analizi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_admin_users_list(self):
        """Admin role'ündeki kullanıcıları listele"""
        if not self.admin_token:
            self.log_test("Admin Kullanıcı Listesi", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
            
            if response.status_code == 200:
                users_data = response.json()
                users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                
                admin_users = [user for user in users if user.get("role") == "admin"]
                
                self.log_test("Admin Kullanıcı Listesi", True, 
                            f"{len(admin_users)} admin kullanıcı bulundu")
                
                print("\n👑 ADMIN KULLANICILARI:")
                print("=" * 30)
                for i, admin in enumerate(admin_users, 1):
                    print(f"  {i}. {admin.get('email', 'N/A')} - {admin.get('name', 'N/A')}")
                    print(f"     Oluşturulma: {admin.get('createdAt', 'N/A')}")
                    print(f"     Son Giriş: {admin.get('lastLogin', 'Hiç giriş yapmamış')}")
                
                return admin_users
            else:
                self.log_test("Admin Kullanıcı Listesi", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Kullanıcı Listesi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_admin_authentication(self):
        """Admin authentication'ın çalıştığını doğrula"""
        # Portal admin ile test
        portal_admin_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=portal_admin_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.log_test("Portal Admin Authentication", True, 
                                "Portal admin girişi başarılı (admin@demo.com)")
                    
                    # Ana admin ile de test
                    main_admin_data = {
                        "username": "admin",
                        "password": "admin123"
                    }
                    
                    main_response = self.session.post(f"{self.base_url}/admin/login", json=main_admin_data)
                    
                    if main_response.status_code == 200:
                        main_data = main_response.json()
                        if main_data.get("access_token"):
                            self.log_test("Main Admin Authentication", True, 
                                        "Ana admin girişi başarılı (admin/admin123)")
                            return True
                        else:
                            self.log_test("Main Admin Authentication", False, "Ana admin token alınamadı")
                    else:
                        self.log_test("Main Admin Authentication", False, 
                                    f"Ana admin giriş başarısız: HTTP {main_response.status_code}")
                else:
                    self.log_test("Portal Admin Authentication", False, "Portal admin token alınamadı")
            else:
                self.log_test("Portal Admin Authentication", False, 
                            f"Portal admin giriş başarısız: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_role_based_endpoints(self):
        """Role-based endpoint'lerin hangi role ile çalıştığını test et"""
        if not self.admin_token:
            self.log_test("Role-based Endpoint Testi", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoint_results = {}
        
        # Portal admin endpoints
        portal_endpoints = [
            ("/api/portal/admin/users", "Kullanıcı Yönetimi"),
            ("/api/portal/admin/collaborations", "İşbirliği Yönetimi"),
            ("/api/portal/admin/logos", "Logo Yönetimi")
        ]
        
        # Main admin endpoints  
        main_endpoints = [
            ("/api/admin/dashboard", "Ana Dashboard"),
            ("/api/admin/contacts", "İletişim Mesajları"),
            ("/api/admin/influencers", "Influencer Başvuruları")
        ]
        
        try:
            print("\n🔐 ROLE-BASED ENDPOINT TESTLERİ:")
            print("=" * 45)
            
            # Portal endpoints test
            print("\nPortal Admin Endpoints:")
            for endpoint, description in portal_endpoints:
                try:
                    response = self.session.get(f"https://skywalker-portal-1.preview.emergentagent.com{endpoint}", 
                                              headers=headers)
                    
                    if response.status_code == 200:
                        endpoint_results[endpoint] = "✅ Çalışıyor"
                        print(f"  ✅ {description}: HTTP 200 - Erişim başarılı")
                    elif response.status_code == 403:
                        endpoint_results[endpoint] = "❌ Yetki yok"
                        print(f"  ❌ {description}: HTTP 403 - Yetki yok")
                    else:
                        endpoint_results[endpoint] = f"⚠️ HTTP {response.status_code}"
                        print(f"  ⚠️ {description}: HTTP {response.status_code}")
                        
                except Exception as e:
                    endpoint_results[endpoint] = f"❌ Hata: {str(e)}"
                    print(f"  ❌ {description}: Hata - {str(e)}")
            
            # Main admin endpoints test (farklı token gerekebilir)
            print("\nMain Admin Endpoints:")
            for endpoint, description in main_endpoints:
                try:
                    response = self.session.get(f"https://skywalker-portal-1.preview.emergentagent.com{endpoint}", 
                                              headers=headers)
                    
                    if response.status_code == 200:
                        endpoint_results[endpoint] = "✅ Çalışıyor"
                        print(f"  ✅ {description}: HTTP 200 - Erişim başarılı")
                    elif response.status_code == 403:
                        endpoint_results[endpoint] = "❌ Yetki yok"
                        print(f"  ❌ {description}: HTTP 403 - Yetki yok")
                    else:
                        endpoint_results[endpoint] = f"⚠️ HTTP {response.status_code}"
                        print(f"  ⚠️ {description}: HTTP {response.status_code}")
                        
                except Exception as e:
                    endpoint_results[endpoint] = f"❌ Hata: {str(e)}"
                    print(f"  ❌ {description}: Hata - {str(e)}")
            
            working_endpoints = len([k for k, v in endpoint_results.items() if "✅" in v])
            total_endpoints = len(endpoint_results)
            
            self.log_test("Role-based Endpoint Testi", True, 
                        f"{working_endpoints}/{total_endpoints} endpoint çalışıyor")
            
            return endpoint_results
            
        except Exception as e:
            self.log_test("Role-based Endpoint Testi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def analyze_role_migration_requirements(self, user_analysis):
        """Role migration gereksinimleri analizi"""
        if not user_analysis:
            self.log_test("Migration Analizi", False, "Kullanıcı analizi verisi bulunamadı")
            return False
        
        try:
            role_distribution = user_analysis.get("role_distribution", {})
            total_users = user_analysis.get("total_users", 0)
            
            print("\n🔄 ROLE MIGRATION GEREKSİNİMLERİ:")
            print("=" * 45)
            
            # Mevcut role'ları analiz et
            current_roles = list(role_distribution.keys())
            print(f"Mevcut Role'lar: {', '.join(current_roles)}")
            
            # Migration senaryoları
            migration_scenarios = []
            
            if "admin" in role_distribution:
                admin_count = role_distribution["admin"]
                migration_scenarios.append({
                    "from": "admin",
                    "to": "super_admin",
                    "affected_users": admin_count,
                    "reason": "Admin yetkilerini genişletmek için"
                })
            
            if "influencer" in role_distribution:
                influencer_count = role_distribution["influencer"]
                migration_scenarios.append({
                    "from": "influencer",
                    "to": "content_creator",
                    "affected_users": influencer_count,
                    "reason": "Daha geniş içerik üretici kategorisi için"
                })
            
            if "partner" in role_distribution:
                partner_count = role_distribution["partner"]
                migration_scenarios.append({
                    "from": "partner",
                    "to": "business_partner",
                    "affected_users": partner_count,
                    "reason": "İş ortaklığı kategorisini netleştirmek için"
                })
            
            print("\nÖnerilen Migration Senaryoları:")
            total_affected = 0
            for scenario in migration_scenarios:
                print(f"  • {scenario['from']} → {scenario['to']}")
                print(f"    Etkilenen kullanıcı: {scenario['affected_users']}")
                print(f"    Sebep: {scenario['reason']}")
                total_affected += scenario['affected_users']
                print()
            
            migration_percentage = (total_affected / total_users * 100) if total_users > 0 else 0
            
            self.log_test("Migration Analizi", True, 
                        f"Toplam {total_affected} kullanıcı (%{migration_percentage:.1f}) migration gerektirebilir")
            
            return {
                "total_affected_users": total_affected,
                "migration_percentage": migration_percentage,
                "scenarios": migration_scenarios
            }
            
        except Exception as e:
            self.log_test("Migration Analizi", False, f"Analiz başarısız: {str(e)}")
        
        return False
    
    def test_admin_login(self):
        """Test admin login with admin/admin123 credentials"""
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/login", json=login_data)
            
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

    # ===== EMPLOYEE MANAGEMENT SYSTEM TESTS =====
    
    def test_get_employees(self):
        """Test GET /api/employees/ endpoint"""
        if not self.admin_token:
            self.log_test("Get Employees", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.employees_url}/", headers=headers)
            
            if response.status_code == 200:
                employees = response.json()
                if isinstance(employees, list):
                    self.log_test("Get Employees", True, f"Successfully retrieved {len(employees)} employees")
                    return employees
                else:
                    self.log_test("Get Employees", False, f"Expected list, got: {type(employees)}")
            else:
                self.log_test("Get Employees", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Employees", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_employee(self):
        """Test POST /api/employees/ with sample employee data"""
        if not self.admin_token:
            self.log_test("Create Employee", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Sample employee data as specified in review request
        employee_data = {
            "email": "calisan@skywalker.com",
            "password": "calisan123",
            "firstName": "Test",
            "lastName": "Çalışan",
            "phone": "+90 555 111 22 33",
            "permissions": ["contacts", "collaborations"]
        }
        
        try:
            response = self.session.post(f"{self.employees_url}/", json=employee_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    employee_id = result.get("employeeId")
                    self.created_items['employees'].append(employee_id)
                    self.log_test("Create Employee", True, f"Successfully created employee: {employee_id}")
                    return employee_id
                else:
                    self.log_test("Create Employee", False, f"Creation failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Employee", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Employee", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_employee_permissions_available(self):
        """Test GET /api/employees/permissions/available endpoint"""
        if not self.admin_token:
            self.log_test("Employee Permissions Available", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.employees_url}/permissions/available", headers=headers)
            
            if response.status_code == 200:
                permissions = response.json()
                if isinstance(permissions, list):
                    permission_keys = [p.get("key") for p in permissions]
                    expected_permissions = ["contacts", "collaborations", "users", "content", "analytics", "settings"]
                    
                    # Check if expected permissions are available
                    found_permissions = [p for p in expected_permissions if p in permission_keys]
                    
                    self.log_test("Employee Permissions Available", True, 
                                f"Successfully retrieved {len(permissions)} permissions. Found: {', '.join(found_permissions)}")
                    return permissions
                else:
                    self.log_test("Employee Permissions Available", False, f"Expected list, got: {type(permissions)}")
            else:
                self.log_test("Employee Permissions Available", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Employee Permissions Available", False, f"Request failed: {str(e)}")
        
        return False

    # ===== SUPPORT TICKET SYSTEM TESTS =====
    
    def test_get_support_tickets(self):
        """Test GET /api/support/tickets endpoint"""
        if not self.admin_token:
            self.log_test("Get Support Tickets", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.support_url}/tickets", headers=headers)
            
            if response.status_code == 200:
                tickets = response.json()
                if isinstance(tickets, list):
                    self.log_test("Get Support Tickets", True, f"Successfully retrieved {len(tickets)} support tickets")
                    return tickets
                else:
                    self.log_test("Get Support Tickets", False, f"Expected list, got: {type(tickets)}")
            else:
                self.log_test("Get Support Tickets", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Support Tickets", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_support_ticket(self):
        """Test POST /api/support/tickets with sample ticket data"""
        if not self.admin_token:
            self.log_test("Create Support Ticket", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Sample ticket data as specified in review request
        ticket_data = {
            "customerId": "test-customer-1",
            "customerEmail": "musteri@test.com",
            "customerName": "Test Müşteri",
            "subject": "Test Destek Talebi",
            "description": "Bu bir test destek talebidir",
            "category": "technical",
            "priority": "medium"
        }
        
        try:
            response = self.session.post(f"{self.support_url}/tickets", json=ticket_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    ticket_id = result.get("ticketId")
                    ticket_number = result.get("ticketNumber")
                    self.created_items['support_tickets'].append(ticket_id)
                    self.log_test("Create Support Ticket", True, 
                                f"Successfully created support ticket: {ticket_number} (ID: {ticket_id})")
                    return ticket_id
                else:
                    self.log_test("Create Support Ticket", False, f"Creation failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Support Ticket", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Support Ticket", False, f"Request failed: {str(e)}")
        
        return False

    # ===== COMPANY PROJECT MANAGEMENT TESTS =====
    
    def test_get_company_projects(self):
        """Test GET /api/company/projects endpoint"""
        if not self.admin_token:
            self.log_test("Get Company Projects", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.company_url}/projects", headers=headers)
            
            if response.status_code == 200:
                projects = response.json()
                if isinstance(projects, list):
                    self.log_test("Get Company Projects", True, f"Successfully retrieved {len(projects)} company projects")
                    return projects
                else:
                    self.log_test("Get Company Projects", False, f"Expected list, got: {type(projects)}")
            else:
                self.log_test("Get Company Projects", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Company Projects", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_company_project(self):
        """Test POST /api/company/projects with sample project data"""
        if not self.admin_token:
            self.log_test("Create Company Project", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Sample project data as specified in review request
        project_data = {
            "companyId": "test-company-1",
            "projectName": "Test Proje",
            "description": "Test projesi açıklaması",
            "status": "active",
            "budget": 25000
        }
        
        try:
            response = self.session.post(f"{self.company_url}/projects", json=project_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    project_id = result.get("projectId")
                    self.created_items['company_projects'].append(project_id)
                    self.log_test("Create Company Project", True, f"Successfully created company project: {project_id}")
                    return project_id
                else:
                    self.log_test("Create Company Project", False, f"Creation failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Company Project", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Company Project", False, f"Request failed: {str(e)}")
        
        return False

    # ===== DATABASE COLLECTIONS VERIFICATION =====
    
    def verify_database_collections(self):
        """Verify that new database collections exist by testing endpoints"""
        collections_status = {}
        
        # Test support_tickets collection
        tickets = self.test_get_support_tickets()
        collections_status['support_tickets'] = tickets is not False
        
        # Test company_projects collection  
        projects = self.test_get_company_projects()
        collections_status['company_projects'] = projects is not False
        
        # Test other collections through their endpoints
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Test customer_profiles via support customers endpoint
            try:
                response = self.session.get(f"{self.support_url}/customers", headers=headers)
                collections_status['customer_profiles'] = response.status_code == 200
            except:
                collections_status['customer_profiles'] = False
            
            # Test meeting_notes via company meetings endpoint
            try:
                response = self.session.get(f"{self.company_url}/meetings", headers=headers)
                collections_status['meeting_notes'] = response.status_code == 200
            except:
                collections_status['meeting_notes'] = False
            
            # Test recurring_tasks via company tasks endpoint
            try:
                response = self.session.get(f"{self.company_url}/tasks", headers=headers)
                collections_status['recurring_tasks'] = response.status_code == 200
            except:
                collections_status['recurring_tasks'] = False
        
        # Log results
        working_collections = [name for name, status in collections_status.items() if status]
        total_collections = len(collections_status)
        
        self.log_test("Database Collections Verification", True, 
                    f"Verified {len(working_collections)}/{total_collections} collections: {', '.join(working_collections)}")
        
        return collections_status

    # ===== IYZICO PAYMENT GATEWAY TESTS =====
    
    def test_payment_creation(self):
        """Test Iyzico payment creation with Turkish market data"""
        if not self.admin_token:
            self.log_test("Payment Creation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Turkish market payment data
        payment_data = {
            "conversationId": f"conv-{int(datetime.now().timestamp())}",
            "price": "100.0",
            "paidPrice": "100.0",
            "currency": "TRY",
            "installment": 1,
            "basketId": f"basket-{int(datetime.now().timestamp())}",
            "paymentChannel": "WEB",
            "paymentGroup": "PRODUCT",
            "paymentCard": {
                "cardHolderName": "Ahmet Yılmaz",
                "cardNumber": "5528790000000008",
                "expireMonth": "12",
                "expireYear": "2030",
                "cvc": "123",
                "registerCard": "0"
            },
            "buyer": {
                "id": "buyer123",
                "name": "Ahmet",
                "surname": "Yılmaz",
                "gsmNumber": "+905551234567",
                "email": "ahmet.yilmaz@example.com",
                "identityNumber": "12345678901",
                "lastLoginDate": "2024-01-15 10:05:50",
                "registrationDate": "2024-01-01 12:43:35",
                "registrationAddress": "İstanbul",
                "ip": "85.34.78.112",
                "city": "İstanbul",
                "country": "Turkey",
                "zipCode": "34000"
            },
            "shippingAddress": {
                "contactName": "Ahmet Yılmaz",
                "city": "İstanbul",
                "country": "Turkey",
                "address": "Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1",
                "zipCode": "34000"
            },
            "billingAddress": {
                "contactName": "Ahmet Yılmaz",
                "city": "İstanbul",
                "country": "Turkey",
                "address": "Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1",
                "zipCode": "34000"
            },
            "basketItems": [
                {
                    "id": "item1",
                    "name": "E-ticaret Danışmanlık Hizmeti",
                    "category1": "Hizmet",
                    "category2": "Danışmanlık",
                    "itemType": "VIRTUAL",
                    "price": "100.0"
                }
            ],
            "service_type": "consultancy",
            "description": "E-ticaret danışmanlık hizmeti ödemesi"
        }
        
        try:
            response = self.session.post(
                f"{self.payments_url}/create",
                json=payment_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    self.created_items['payment_transactions'] = getattr(self.created_items, 'payment_transactions', [])
                    self.created_items['payment_transactions'].append(transaction_id)
                    self.log_test("Payment Creation", True, f"Successfully created payment transaction: {transaction_id}")
                    return transaction_id
                else:
                    self.log_test("Payment Creation", False, f"Payment failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Payment Creation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Creation", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_payment_transaction_retrieval(self, transaction_id):
        """Test payment transaction retrieval"""
        if not self.admin_token or not transaction_id:
            self.log_test("Payment Transaction Retrieval", False, "No admin token or transaction ID available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(
                f"{self.payments_url}/transaction/{transaction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_data = result.get("data", {})
                    self.log_test("Payment Transaction Retrieval", True, f"Successfully retrieved transaction: {transaction_data.get('id', 'N/A')}")
                    return transaction_data
                else:
                    self.log_test("Payment Transaction Retrieval", False, f"Retrieval failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 404:
                self.log_test("Payment Transaction Retrieval", False, "Transaction not found")
            else:
                self.log_test("Payment Transaction Retrieval", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Transaction Retrieval", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_payment_admin_endpoints(self):
        """Test admin payment management endpoints"""
        if not self.admin_token:
            self.log_test("Payment Admin Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test admin transactions endpoint
            response = self.session.get(
                f"{self.payments_url}/admin/transactions",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transactions = result.get("data", {}).get("transactions", [])
                    self.log_test("Payment Admin Transactions", True, f"Successfully retrieved {len(transactions)} payment transactions")
                else:
                    self.log_test("Payment Admin Transactions", False, f"Failed to get transactions: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Payment Admin Transactions", False, f"HTTP {response.status_code}: {response.text}")
            
            # Test admin stats endpoint
            response = self.session.get(
                f"{self.payments_url}/admin/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    stats = result.get("data", {})
                    total_transactions = stats.get("total_transactions", 0)
                    success_rate = stats.get("success_rate", 0)
                    self.log_test("Payment Admin Stats", True, f"Successfully retrieved payment stats: {total_transactions} transactions, {success_rate}% success rate")
                    return True
                else:
                    self.log_test("Payment Admin Stats", False, f"Failed to get stats: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Payment Admin Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Admin Endpoints", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_payment_error_handling(self):
        """Test payment error handling and validation"""
        if not self.admin_token:
            self.log_test("Payment Error Handling", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test invalid payment data
        invalid_payment_data = {
            "conversationId": "test-invalid",
            "price": "invalid_price",  # Invalid price format
            "currency": "USD",  # Wrong currency for Turkish market
            "buyer": {
                "email": "invalid-email"  # Invalid email format
            }
        }
        
        try:
            response = self.session.post(
                f"{self.payments_url}/create",
                json=invalid_payment_data,
                headers=headers
            )
            
            if response.status_code in [400, 422]:
                self.log_test("Payment Validation Error", True, f"Correctly rejected invalid payment data with HTTP {response.status_code}")
                return True
            else:
                self.log_test("Payment Validation Error", False, f"Expected validation error, got HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Payment Error Handling", False, f"Request failed: {str(e)}")
        
        return False

    # ===== NETGSM SMS GATEWAY TESTS =====
    
    def test_single_sms_sending(self):
        """Test single SMS sending with Turkish phone number"""
        if not self.admin_token:
            self.log_test("Single SMS Sending", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        sms_data = {
            "phoneNumber": "+905551234567",
            "message": "Merhaba! Bu Skywalker.tc'den test SMS'idir. İyi günler!",
            "priority": "high"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/send",
                json=sms_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    self.created_items['sms_transactions'] = getattr(self.created_items, 'sms_transactions', [])
                    self.created_items['sms_transactions'].append(transaction_id)
                    self.log_test("Single SMS Sending", True, f"Successfully sent SMS: {transaction_id}")
                    return transaction_id
                else:
                    self.log_test("Single SMS Sending", False, f"SMS sending failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Single SMS Sending", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Single SMS Sending", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_bulk_sms_operations(self):
        """Test bulk SMS operations"""
        if not self.admin_token:
            self.log_test("Bulk SMS Operations", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        bulk_sms_data = {
            "recipients": [
                "+905551234567",
                "+905551234568",
                "+905551234569"
            ],
            "message": "Toplu SMS testi - Skywalker.tc'den selamlar!",
            "batchSize": 10,
            "priority": "normal"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/send/bulk",
                json=bulk_sms_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    batch_id = result.get("batch_id")
                    recipient_count = result.get("recipient_count", 0)
                    self.log_test("Bulk SMS Operations", True, f"Successfully queued bulk SMS: {batch_id} for {recipient_count} recipients")
                    return batch_id
                else:
                    self.log_test("Bulk SMS Operations", False, f"Bulk SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Bulk SMS Operations", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Bulk SMS Operations", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_customer_response_sms(self):
        """Test customer response SMS endpoint"""
        if not self.admin_token:
            self.log_test("Customer Response SMS", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        customer_response_data = {
            "phoneNumber": "+905551234567",
            "customerName": "Ahmet Yılmaz",
            "portalLink": "https://skywalker.tc/portal",
            "requestId": "req-12345"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/customer/response",
                json=customer_response_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    self.log_test("Customer Response SMS", True, f"Successfully sent customer response SMS: {transaction_id}")
                    return transaction_id
                else:
                    self.log_test("Customer Response SMS", False, f"Customer response SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Customer Response SMS", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Customer Response SMS", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_influencer_collaboration_sms(self):
        """Test influencer collaboration SMS endpoint"""
        if not self.admin_token:
            self.log_test("Influencer Collaboration SMS", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        collaboration_data = {
            "phoneNumbers": [
                "+905551234567",
                "+905551234568"
            ],
            "collaborationId": "collab-12345",
            "portalLink": "https://skywalker.tc/portal"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/influencer/collaboration",
                json=collaboration_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    batch_id = result.get("batch_id")
                    successful_sends = result.get("successful_sends", 0)
                    self.log_test("Influencer Collaboration SMS", True, f"Successfully sent collaboration SMS: {batch_id}, {successful_sends} sent")
                    return batch_id
                else:
                    self.log_test("Influencer Collaboration SMS", False, f"Collaboration SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Influencer Collaboration SMS", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Influencer Collaboration SMS", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_sms_admin_endpoints(self):
        """Test SMS admin management endpoints"""
        if not self.admin_token:
            self.log_test("SMS Admin Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test admin SMS transactions endpoint
            response = self.session.get(
                f"{self.sms_url}/admin/transactions",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transactions = result.get("data", {}).get("transactions", [])
                    self.log_test("SMS Admin Transactions", True, f"Successfully retrieved {len(transactions)} SMS transactions")
                else:
                    self.log_test("SMS Admin Transactions", False, f"Failed to get SMS transactions: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Admin Transactions", False, f"HTTP {response.status_code}: {response.text}")
            
            # Test admin SMS stats endpoint
            response = self.session.get(
                f"{self.sms_url}/admin/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    stats = result.get("data", {})
                    total_sms = stats.get("total_sms", 0)
                    success_rate = stats.get("success_rate", 0)
                    self.log_test("SMS Admin Stats", True, f"Successfully retrieved SMS stats: {total_sms} SMS sent, {success_rate}% success rate")
                    return True
                else:
                    self.log_test("SMS Admin Stats", False, f"Failed to get SMS stats: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Admin Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Admin Endpoints", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_sms_service_status(self):
        """Test SMS service status check"""
        if not self.admin_token:
            self.log_test("SMS Service Status", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(
                f"{self.sms_url}/service/status",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                status_data = result.get("data", {})
                service_status = status_data.get("status", "unknown")
                self.log_test("SMS Service Status", True, f"SMS service status: {service_status}")
                return True
            else:
                self.log_test("SMS Service Status", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Service Status", False, f"Request failed: {str(e)}")
        
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
    
    def run_payment_gateway_tests(self):
        """Run all Iyzico payment gateway tests"""
        print("\n💳 IYZICO PAYMENT GATEWAY TESTS")
        print("=" * 50)
        
        # Test payment creation with Turkish market data
        transaction_id = self.test_payment_creation()
        
        # Test payment transaction retrieval
        if transaction_id:
            self.test_payment_transaction_retrieval(transaction_id)
        
        # Test admin payment management endpoints
        self.test_payment_admin_endpoints()
        
        # Test payment error handling and validation
        self.test_payment_error_handling()
    
    def run_sms_gateway_tests(self):
        """Run all NetGSM SMS gateway tests"""
        print("\n📱 NETGSM SMS GATEWAY TESTS")
        print("=" * 45)
        
        # Test single SMS sending
        self.test_single_sms_sending()
        
        # Test bulk SMS operations
        self.test_bulk_sms_operations()
        
        # Test business-specific SMS endpoints
        self.test_customer_response_sms()
        self.test_influencer_collaboration_sms()
        
        # Test admin SMS management endpoints
        self.test_sms_admin_endpoints()
        
        # Test SMS service status check
        self.test_sms_service_status()
    
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

    def test_admin_influencer_requests(self):
        """Test admin panel influencer applications endpoint"""
        if not self.admin_token:
            self.log_test("Admin Influencer Requests", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test getting influencer applications
            response = self.session.get(
                f"{self.base_url}/admin/influencers",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "items" in result:
                    applications = result["items"]
                    self.log_test("Admin Influencer Requests", True, f"Successfully retrieved {len(applications)} influencer applications")
                    return applications
                else:
                    self.log_test("Admin Influencer Requests", False, f"Unexpected response format: {type(result)}")
            else:
                self.log_test("Admin Influencer Requests", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Influencer Requests", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_partnership_requests_system(self):
        """Test partnership requests functionality"""
        if not self.admin_token:
            self.log_test("Partnership Requests System", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test if partnership request endpoint exists
            response = self.session.post(
                f"{self.base_url}/partnership/request",
                json={"test": "data"},
                headers=headers
            )
            
            if response.status_code == 404:
                self.log_test("Partnership Requests System", False, "Partnership request endpoints not implemented yet - this is expected for current system state")
                return False
            elif response.status_code == 422:
                # Endpoint exists but validation failed (expected)
                self.log_test("Partnership Requests System", True, "Partnership request endpoint exists and validates input correctly")
                return True
            elif response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Partnership Requests System", True, "Partnership request system working")
                    return True
                else:
                    self.log_test("Partnership Requests System", False, f"Partnership request failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Partnership Requests System", False, f"Unexpected response: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Partnership Requests System", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_services_management_api(self):
        """Test services management API endpoints"""
        if not self.admin_token:
            self.log_test("Services Management API", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test admin services endpoint
            response = self.session.get(
                f"{self.base_url}/services/admin/all",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    services_data = result.get("data", {})
                    services = services_data.get("services", [])
                    total = services_data.get("total", 0)
                    self.log_test("Services Admin API", True, f"Successfully retrieved {len(services)} services (total: {total})")
                    
                    # Test public services endpoint
                    public_response = self.session.get(f"{self.base_url}/services/")
                    
                    if public_response.status_code == 200:
                        public_services = public_response.json()
                        if isinstance(public_services, list):
                            self.log_test("Services Public API", True, f"Successfully retrieved {len(public_services)} public services")
                            
                            # Test service types endpoint
                            types_response = self.session.get(f"{self.base_url}/services/types")
                            
                            if types_response.status_code == 200:
                                types_result = types_response.json()
                                if types_result.get("success"):
                                    service_types = types_result.get("data", [])
                                    self.log_test("Service Types API", True, f"Successfully retrieved {len(service_types)} service types")
                                    return True
                                else:
                                    self.log_test("Service Types API", False, f"Types API failed: {types_result.get('message', 'Unknown error')}")
                            else:
                                self.log_test("Service Types API", False, f"HTTP {types_response.status_code}: {types_response.text}")
                        else:
                            self.log_test("Services Public API", False, f"Expected list, got: {type(public_services)}")
                    else:
                        self.log_test("Services Public API", False, f"HTTP {public_response.status_code}: {public_response.text}")
                else:
                    self.log_test("Services Admin API", False, f"Admin API failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Services Admin API", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Services Management API", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_critical_features_tests(self):
        """Run tests for critical features as requested in review"""
        print("\n🔥 CRITICAL FEATURES TESTING (Review Request)")
        print("=" * 60)
        
        # Test influencer collaboration system
        self.test_admin_influencer_requests()
        
        # Test partnership requests system
        self.test_partnership_requests_system()
        
        # Test payment system
        self.run_payment_gateway_tests()
        
        # Test SMS system
        self.run_sms_gateway_tests()
        
        # Test services management
        self.test_services_management_api()
        
        # Test contact form endpoint (as requested in review)
        self.run_contact_form_tests()

    def test_contact_form_submission(self):
        """Test contact form submission endpoint with Turkish sample data"""
        print("\n📧 CONTACT FORM SUBMISSION TEST")
        print("=" * 40)
        
        # Test data as specified in the review request
        contact_data = {
            "name": "Test Kullanıcı",
            "email": "test@example.com",
            "message": "Test mesajı",
            "phone": "+90 555 123 45 67",
            "company": "Test Şirketi",
            "service": "SEO Optimizasyonu"
        }
        
        try:
            # Test POST /api/contact/submit endpoint
            response = self.session.post(
                f"{self.base_url}/contact/submit",
                json=contact_data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message_id = result.get("data", {}).get("id")
                    self.log_test("Contact Form Submission", True, f"Successfully submitted contact form (ID: {message_id})")
                    
                    # Verify response format
                    expected_message = "Mesajınız başarıyla gönderildi! 24 saat içinde size dönüş yapacağız."
                    if result.get("message") == expected_message:
                        self.log_test("Contact Form Response Format", True, "Response message format is correct")
                    else:
                        self.log_test("Contact Form Response Format", False, f"Expected: '{expected_message}', Got: '{result.get('message')}'")
                    
                    return message_id
                else:
                    self.log_test("Contact Form Submission", False, f"Submission failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Contact Form Submission", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Form Submission", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_contact_form_validation(self):
        """Test contact form validation for required fields"""
        print("\n✅ CONTACT FORM VALIDATION TEST")
        print("=" * 40)
        
        validation_tests = [
            {
                "name": "Missing Name Field",
                "data": {
                    "email": "test@example.com",
                    "message": "Test message"
                },
                "should_fail": True
            },
            {
                "name": "Missing Email Field", 
                "data": {
                    "name": "Test User",
                    "message": "Test message"
                },
                "should_fail": True
            },
            {
                "name": "Missing Message Field",
                "data": {
                    "name": "Test User",
                    "email": "test@example.com"
                },
                "should_fail": True
            },
            {
                "name": "Invalid Email Format",
                "data": {
                    "name": "Test User",
                    "email": "invalid-email",
                    "message": "Test message"
                },
                "should_fail": True
            },
            {
                "name": "Valid Minimal Data",
                "data": {
                    "name": "Test User",
                    "email": "test@example.com", 
                    "message": "Test message"
                },
                "should_fail": False
            },
            {
                "name": "Valid Complete Data",
                "data": {
                    "name": "Test Kullanıcı",
                    "email": "test@example.com",
                    "message": "Test mesajı",
                    "phone": "+90 555 123 45 67",
                    "company": "Test Şirketi",
                    "service": "SEO Optimizasyonu"
                },
                "should_fail": False
            }
        ]
        
        passed_tests = 0
        total_tests = len(validation_tests)
        
        for test in validation_tests:
            try:
                response = self.session.post(
                    f"{self.base_url}/contact/submit",
                    json=test["data"]
                )
                
                if test["should_fail"]:
                    if response.status_code in [400, 422]:
                        self.log_test(f"Validation: {test['name']}", True, f"Correctly rejected invalid data (HTTP {response.status_code})")
                        passed_tests += 1
                    else:
                        self.log_test(f"Validation: {test['name']}", False, f"Expected validation error, got HTTP {response.status_code}")
                else:
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            self.log_test(f"Validation: {test['name']}", True, "Correctly accepted valid data")
                            passed_tests += 1
                        else:
                            self.log_test(f"Validation: {test['name']}", False, f"Valid data rejected: {result.get('message')}")
                    else:
                        self.log_test(f"Validation: {test['name']}", False, f"Valid data rejected with HTTP {response.status_code}")
                        
            except Exception as e:
                self.log_test(f"Validation: {test['name']}", False, f"Request failed: {str(e)}")
        
        self.log_test("Contact Form Validation Summary", passed_tests == total_tests, f"Passed {passed_tests}/{total_tests} validation tests")
        return passed_tests == total_tests
    
    def test_contact_messages_collection_verification(self):
        """Verify contact messages are saved to database collection"""
        if not self.admin_token:
            self.log_test("Contact Messages Collection Verification", False, "No admin token available")
            return False
        
        print("\n🗄️  CONTACT MESSAGES COLLECTION VERIFICATION")
        print("=" * 50)
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Get contact messages from admin endpoint
            response = self.session.get(
                f"{self.base_url}/admin/contacts",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if hasattr(result, 'get') and result.get("items") is not None:
                    messages = result.get("items", [])
                    total_messages = result.get("total", 0)
                    self.log_test("Contact Messages Collection Access", True, f"Successfully retrieved {len(messages)} contact messages (total: {total_messages})")
                    
                    # Look for our test message
                    test_message_found = False
                    for message in messages:
                        if (message.get("name") == "Test Kullanıcı" and 
                            message.get("email") == "test@example.com" and
                            message.get("company") == "Test Şirketi"):
                            test_message_found = True
                            self.log_test("Test Message in Collection", True, f"Found test message with ID: {message.get('id')}")
                            
                            # Verify all fields are saved correctly
                            field_checks = [
                                ("name", "Test Kullanıcı"),
                                ("email", "test@example.com"),
                                ("message", "Test mesajı"),
                                ("phone", "+90 555 123 45 67"),
                                ("company", "Test Şirketi"),
                                ("service", "SEO Optimizasyonu"),
                                ("status", "new")
                            ]
                            
                            all_fields_correct = True
                            for field_name, expected_value in field_checks:
                                actual_value = message.get(field_name)
                                if actual_value != expected_value:
                                    self.log_test(f"Field Check: {field_name}", False, f"Expected: '{expected_value}', Got: '{actual_value}'")
                                    all_fields_correct = False
                                else:
                                    self.log_test(f"Field Check: {field_name}", True, f"Correct value: '{actual_value}'")
                            
                            if all_fields_correct:
                                self.log_test("All Field Verification", True, "All contact message fields saved correctly")
                            break
                    
                    if not test_message_found:
                        self.log_test("Test Message in Collection", False, "Test message not found in database")
                        
                    return True
                else:
                    self.log_test("Contact Messages Collection Access", False, f"Unexpected response format: {type(result)}")
            else:
                self.log_test("Contact Messages Collection Access", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Messages Database Verification", False, f"Request failed: {str(e)}")
        
        return False

    def run_user_management_analysis(self):
        """Kullanıcı yönetim sistemi analizi çalıştır"""
        print("🚀 KULLANICI YÖNETİM SİSTEMİ ANALİZİ BAŞLATILIYOR")
        print("=" * 60)
        
        # Admin girişi yap
        if not self.test_admin_login():
            print("❌ Admin authentication olmadan devam edilemiyor")
            return False
        
        print("\n1️⃣ MEVCUT KULLANICI ROLLERİ ANALİZİ")
        print("-" * 40)
        user_analysis = self.analyze_existing_users()
        
        print("\n2️⃣ ADMIN KULLANICI TESTİ")
        print("-" * 30)
        admin_users = self.test_admin_users_list()
        
        print("\n3️⃣ ADMIN AUTHENTICATION DOĞRULAMASİ")
        print("-" * 40)
        self.test_admin_authentication()
        
        print("\n4️⃣ ROLE-BASED ENDPOINT TESTİ")
        print("-" * 35)
        endpoint_results = self.test_role_based_endpoints()
        
        print("\n5️⃣ ROLE MIGRATION GEREKSİNİMLERİ")
        print("-" * 40)
        if user_analysis:
            migration_analysis = self.analyze_role_migration_requirements(user_analysis)
        
        # Final özet
        self.print_user_management_summary()
        
        return True
    
    def print_user_management_summary(self):
        """Kullanıcı yönetim sistemi analizi özeti"""
        print("\n" + "=" * 60)
        print("📋 KULLANICI YÖNETİM SİSTEMİ ANALİZ ÖZETİ")
        print("=" * 60)
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Başarılı Testler: {passed_tests}/{total_tests} (%{success_rate:.1f})")
        
        # Başarısız testleri göster
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ Başarısız Testler ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['message']}")
        
        print(f"\n🕒 Test Tamamlanma Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    def run_user_management_analysis(self):
        """Kullanıcı yönetim sistemi analizi çalıştır"""
        print("🚀 KULLANICI YÖNETİM SİSTEMİ ANALİZİ BAŞLATILIYOR")
        print("=" * 60)
        
        # Admin girişi yap
        if not self.test_admin_login():
            print("❌ Admin authentication olmadan devam edilemiyor")
            return False
        
        print("\n1️⃣ MEVCUT KULLANICI ROLLERİ ANALİZİ")
        print("-" * 40)
        user_analysis = self.analyze_existing_users()
        
        print("\n2️⃣ ADMIN KULLANICI TESTİ")
        print("-" * 30)
        admin_users = self.test_admin_users_list()
        
        print("\n3️⃣ ADMIN AUTHENTICATION DOĞRULAMASİ")
        print("-" * 40)
        self.test_admin_authentication()
        
        print("\n4️⃣ ROLE-BASED ENDPOINT TESTİ")
        print("-" * 35)
        endpoint_results = self.test_role_based_endpoints()
        
        print("\n5️⃣ ROLE MIGRATION GEREKSİNİMLERİ")
        print("-" * 40)
        if user_analysis:
            migration_analysis = self.analyze_role_migration_requirements(user_analysis)
        
        # Final özet
        self.print_user_management_summary()
        
        return True
    
    def print_user_management_summary(self):
        """Kullanıcı yönetim sistemi analizi özeti"""
        print("\n" + "=" * 60)
        print("📋 KULLANICI YÖNETİM SİSTEMİ ANALİZ ÖZETİ")
        print("=" * 60)
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Başarılı Testler: {passed_tests}/{total_tests} (%{success_rate:.1f})")
        
        # Başarısız testleri göster
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ Başarısız Testler ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['message']}")
        
        print(f"\n🕒 Test Tamamlanma Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)


if __name__ == "__main__":
    print("🔍 KULLANICI YÖNETİM SİSTEMİ ANALİZİ")
    print("=" * 50)
    print("Mevcut kullanıcı yönetim sistemi analizi başlatılıyor...")
    print("Bu analiz şunları içerir:")
    print("• Mevcut kullanıcı rolleri analizi")
    print("• Role distribution hesaplama")
    print("• Admin kullanıcı testi")
    print("• Role-based endpoint testleri")
    print("• Migration gereksinimleri analizi")
    print("=" * 50)
    
    analyzer = UserManagementSystemAnalyzer()
    success = analyzer.run_user_management_analysis()
    
    if success:
        print("\n🎉 Kullanıcı yönetim sistemi analizi başarıyla tamamlandı!")
    else:
        print("\n⚠️ Analiz sırasında bazı sorunlar yaşandı.")
        
    print("\nDetaylı sonuçlar yukarıda gösterilmiştir.")
    def test_user_approval_debug(self):
        """Debug user approval functionality as requested in Turkish review"""
        print("\n🔍 KULLANICI ONAY HATA DEBUG TESTİ")
        print("=" * 45)
        
        if not self.admin_token:
            self.log_test("User Approval Debug", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # 1. Get all users to find unapproved ones
            print("1️⃣ Onaylanmamış kullanıcıları bulma...")
            response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
            
            if response.status_code != 200:
                self.log_test("Get Users for Approval", False, f"HTTP {response.status_code}: {response.text}")
                return False
            
            users_data = response.json()
            users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
            
            # Find unapproved users
            unapproved_users = [user for user in users if not user.get("isApproved", True)]
            
            print(f"   Toplam kullanıcı: {len(users)}")
            print(f"   Onaylanmamış kullanıcı: {len(unapproved_users)}")
            
            if not unapproved_users:
                # Create a test user for approval testing
                print("2️⃣ Test kullanıcısı oluşturuluyor...")
                test_user_data = {
                    "email": "test.approval@example.com",
                    "password": "test123",
                    "name": "Test Approval User",
                    "role": "partner",
                    "company": "Test Approval Company",
                    "phone": "+90 555 999 8877"
                }
                
                register_response = self.session.post(f"{self.portal_url}/register", json=test_user_data)
                if register_response.status_code == 200:
                    print("   ✅ Test kullanıcısı oluşturuldu")
                    
                    # Get users again to find the new user
                    response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
                    if response.status_code == 200:
                        users_data = response.json()
                        users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                        unapproved_users = [user for user in users if not user.get("isApproved", True)]
                else:
                    print(f"   ❌ Test kullanıcısı oluşturulamadı: HTTP {register_response.status_code}")
            
            if not unapproved_users:
                self.log_test("User Approval Debug", False, "Onaylanmamış kullanıcı bulunamadı")
                return False
            
            # 3. Try to approve the first unapproved user
            test_user = unapproved_users[0]
            user_id = test_user.get("id")
            user_email = test_user.get("email", "N/A")
            
            print(f"3️⃣ Kullanıcı onaylama testi: {user_email} (ID: {user_id})")
            
            # Test the approval endpoint
            approval_response = self.session.put(
                f"{self.portal_url}/admin/users/{user_id}/approve",
                headers=headers
            )
            
            print(f"   Approval Response Status: {approval_response.status_code}")
            print(f"   Approval Response Text: {approval_response.text}")
            
            if approval_response.status_code == 200:
                approval_data = approval_response.json()
                if approval_data.get("success"):
                    self.log_test("User Approval", True, f"Kullanıcı başarıyla onaylandı: {user_email}")
                    
                    # 4. Verify the approval in database
                    print("4️⃣ Database durumu kontrol ediliyor...")
                    verify_response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        verify_users = verify_data.get("users", []) if isinstance(verify_data, dict) else verify_data
                        
                        approved_user = next((u for u in verify_users if u.get("id") == user_id), None)
                        if approved_user and approved_user.get("isApproved"):
                            self.log_test("Database Update Verification", True, "Database'de onay durumu güncellendi")
                            print("   ✅ Database update başarılı")
                        else:
                            self.log_test("Database Update Verification", False, "Database'de onay durumu güncellenemedi")
                            print("   ❌ Database update başarısız")
                    
                    return True
                else:
                    self.log_test("User Approval", False, f"Onay başarısız: {approval_data.get('message', 'Bilinmeyen hata')}")
            else:
                error_message = approval_response.text
                self.log_test("User Approval", False, f"HTTP {approval_response.status_code}: {error_message}")
                
                # 5. Check backend logs for detailed error
                print("5️⃣ Backend log analizi...")
                try:
                    import subprocess
                    log_result = subprocess.run(
                        ["tail", "-n", "20", "/var/log/supervisor/backend.err.log"],
                        capture_output=True, text=True
                    )
                    if log_result.stdout:
                        print("   Backend Error Logs:")
                        print("   " + "\n   ".join(log_result.stdout.split("\n")[-10:]))
                except Exception as e:
                    print(f"   Log okuma hatası: {str(e)}")
                
                return False
                
        except Exception as e:
            self.log_test("User Approval Debug", False, f"Test başarısız: {str(e)}")
            print(f"   Exception: {str(e)}")
        
        return False
    
    def test_database_user_queries(self):
        """Test database user queries directly"""
        print("\n🗄️ DATABASE USER QUERY TESTİ")
        print("=" * 35)
        
        if not self.admin_token:
            self.log_test("Database Query Test", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test getting users with different filters
            print("1️⃣ Tüm kullanıcıları getirme...")
            response = self.session.get(f"{self.portal_url}/admin/users", headers=headers)
            
            if response.status_code == 200:
                users_data = response.json()
                users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                
                print(f"   Toplam kullanıcı sayısı: {len(users)}")
                
                # Analyze approval status
                approved_count = len([u for u in users if u.get("isApproved", False)])
                unapproved_count = len(users) - approved_count
                
                print(f"   Onaylı kullanıcı: {approved_count}")
                print(f"   Onaylanmamış kullanıcı: {unapproved_count}")
                
                # Show sample user data structure
                if users:
                    sample_user = users[0]
                    print("   Örnek kullanıcı veri yapısı:")
                    for key, value in sample_user.items():
                        print(f"     {key}: {value}")
                
                self.log_test("Database Query Test", True, f"{len(users)} kullanıcı başarıyla alındı")
                return True
            else:
                self.log_test("Database Query Test", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Database Query Test", False, f"Test başarısız: {str(e)}")
        
        return False

    def run_user_approval_debug_tests(self):
        """Run user approval debug tests as requested in Turkish review"""
        print("🚀 KULLANICI ONAY DEBUG TESTLERİ BAŞLATILIYOR")
        print("=" * 60)
        
        # Authentication
        if not self.test_admin_login():
            print("❌ Admin login failed - stopping tests")
            return False
        
        # User Approval Debug Tests (Turkish Review Request)
        print("\n🔍 KULLANICI ONAY DEBUG TESTLERİ")
        print("=" * 45)
        
        self.test_database_user_queries()
        self.test_user_approval_debug()
        
        # Final Results
        self.print_final_results()
        
        return True
                                ("phone", "+90 555 123 45 67"),
                                ("company", "Test Şirketi"),
                                ("service", "SEO Optimizasyonu")
                            ]
                            
                            all_fields_correct = True
                            for field, expected_value in field_checks:
                                if message.get(field) != expected_value:
                                    self.log_test(f"Field Verification: {field}", False, f"Expected '{expected_value}', got '{message.get(field)}'")
                                    all_fields_correct = False
                                else:
                                    self.log_test(f"Field Verification: {field}", True, f"Correctly saved: '{expected_value}'")
                            
                            if all_fields_correct:
                                self.log_test("All Fields Verification", True, "All contact form fields saved correctly")
                                return True
                            break
                    
                    if not test_message_found:
                        self.log_test("Test Message in Collection", False, "Test message not found in collection")
                        
                else:
                    self.log_test("Contact Messages Collection Access", False, f"Unexpected response format: {type(result)}")
            else:
                self.log_test("Contact Messages Collection Access", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Messages Collection Verification", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_contact_form_tests(self):
        """Run all contact form tests"""
        print("\n📧 CONTACT FORM ENDPOINT TESTS")
        print("=" * 45)
        
        # Test contact form submission with sample data
        message_id = self.test_contact_form_submission()
        
        # Test contact form validation
        self.test_contact_form_validation()
        
        # Verify messages are saved to collection
        self.test_contact_messages_collection_verification()
        
        return message_id is not False

    # ===== COLLABORATION ENDPOINTS TESTS =====
    
    def test_admin_authentication_for_collaborations(self):
        """Test admin authentication specifically for collaboration endpoints"""
        login_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            # Try portal admin login endpoint
            response = self.session.post(f"{self.portal_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.admin_token = data["access_token"]
                    user_role = data.get("user", {}).get("role", "unknown")
                    # Verify JWT token format
                    token_parts = self.admin_token.split('.')
                    if len(token_parts) == 3 and user_role == "admin":
                        self.log_test("Admin Authentication (admin@demo.com/demo123)", True, f"Successfully logged in as portal admin with valid JWT token")
                        return True
                    else:
                        self.log_test("Admin Authentication (admin@demo.com/demo123)", False, f"Invalid JWT token format or role: {len(token_parts)} parts, role: {user_role}")
                else:
                    self.log_test("Admin Authentication (admin@demo.com/demo123)", False, f"Login failed: No access token received")
            else:
                self.log_test("Admin Authentication (admin@demo.com/demo123)", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Authentication (admin@demo.com/demo123)", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_get_collaborations_endpoint(self):
        """Test GET /api/portal/admin/collaborations endpoint"""
        if not self.admin_token:
            self.log_test("GET Collaborations Endpoint", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/collaborations", headers=headers)
            
            if response.status_code == 200:
                collaborations = response.json()
                if isinstance(collaborations, list):
                    self.log_test("GET Collaborations Endpoint", True, f"Successfully retrieved {len(collaborations)} collaborations")
                    return collaborations
                else:
                    self.log_test("GET Collaborations Endpoint", False, f"Expected list, got: {type(collaborations)}")
            else:
                self.log_test("GET Collaborations Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET Collaborations Endpoint", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_create_collaboration_endpoint(self):
        """Test POST /api/portal/admin/collaborations endpoint with sample data"""
        if not self.admin_token:
            self.log_test("Create Collaboration Endpoint", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Sample collaboration data as specified in the review request
        collaboration_data = {
            "title": "Test İşbirliği",
            "description": "Bu bir test işbirliğidir",
            "category": "moda",
            "requirements": "Test gereksinimleri",
            "budget": 5000,
            "priority": "high",
            "maxInfluencers": 2,
            "status": "draft",
            "targetCategories": ["moda", "lifestyle"],
            "minFollowers": 1000,
            "maxFollowers": 100000,
            "deliverables": ["Instagram post", "Story paylaşımı"],
            "deadline": "2024-02-15T00:00:00Z"
        }
        
        try:
            response = self.session.post(
                f"{self.portal_url}/admin/collaborations",
                json=collaboration_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    collaboration_id = result.get("id")
                    self.created_items['collaborations'] = getattr(self.created_items, 'collaborations', [])
                    self.created_items['collaborations'].append(collaboration_id)
                    self.log_test("Create Collaboration Endpoint", True, f"Successfully created collaboration: {collaboration_id}")
                    return collaboration_id
                else:
                    self.log_test("Create Collaboration Endpoint", False, f"Creation failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Create Collaboration Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Collaboration Endpoint", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_collaboration_data_persistence(self, collaboration_id):
        """Test that created collaboration is persisted in database"""
        if not self.admin_token or not collaboration_id:
            self.log_test("Collaboration Data Persistence", False, "No admin token or collaboration ID available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Get all collaborations and check if our created one is there
            response = self.session.get(f"{self.portal_url}/admin/collaborations", headers=headers)
            
            if response.status_code == 200:
                collaborations = response.json()
                if isinstance(collaborations, list):
                    # Look for our collaboration
                    found_collaboration = None
                    for collab in collaborations:
                        if collab.get("id") == collaboration_id:
                            found_collaboration = collab
                            break
                    
                    if found_collaboration:
                        # Verify the data matches what we created
                        expected_title = "Test İşbirliği"
                        if found_collaboration.get("title") == expected_title:
                            self.log_test("Collaboration Data Persistence", True, f"Collaboration successfully persisted with correct data: {expected_title}")
                            return True
                        else:
                            self.log_test("Collaboration Data Persistence", False, f"Data mismatch - expected title: {expected_title}, got: {found_collaboration.get('title')}")
                    else:
                        self.log_test("Collaboration Data Persistence", False, f"Created collaboration {collaboration_id} not found in database")
                else:
                    self.log_test("Collaboration Data Persistence", False, f"Expected list, got: {type(collaborations)}")
            else:
                self.log_test("Collaboration Data Persistence", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Collaboration Data Persistence", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_mongodb_collaborations_collection(self):
        """Test that collaborations collection exists in MongoDB and count documents"""
        # Since we can't directly access MongoDB from this test environment,
        # we'll use the API to verify the collection exists and has data
        if not self.admin_token:
            self.log_test("MongoDB Collaborations Collection", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/collaborations", headers=headers)
            
            if response.status_code == 200:
                collaborations = response.json()
                if isinstance(collaborations, list):
                    collaboration_count = len(collaborations)
                    self.log_test("MongoDB Collaborations Collection", True, f"Collaborations collection verified - found {collaboration_count} documents")
                    return collaboration_count
                else:
                    self.log_test("MongoDB Collaborations Collection", False, f"Unexpected response format: {type(collaborations)}")
            elif response.status_code == 404:
                self.log_test("MongoDB Collaborations Collection", False, "Collaborations collection or endpoint not found")
            else:
                self.log_test("MongoDB Collaborations Collection", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("MongoDB Collaborations Collection", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_collaboration_response_format(self):
        """Test collaboration response format and data structure"""
        if not self.admin_token:
            self.log_test("Collaboration Response Format", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/collaborations", headers=headers)
            
            if response.status_code == 200:
                collaborations = response.json()
                if isinstance(collaborations, list):
                    if len(collaborations) > 0:
                        # Check the structure of the first collaboration
                        first_collab = collaborations[0]
                        expected_fields = ["id", "title", "description", "category", "status", "createdAt"]
                        found_fields = [field for field in expected_fields if field in first_collab]
                        
                        if len(found_fields) >= 4:  # At least 4 out of 6 expected fields
                            self.log_test("Collaboration Response Format", True, f"Response format valid - found {len(found_fields)}/6 expected fields: {found_fields}")
                            return True
                        else:
                            self.log_test("Collaboration Response Format", False, f"Missing expected fields. Found: {found_fields}, Expected: {expected_fields}")
                    else:
                        self.log_test("Collaboration Response Format", True, "Response format valid - empty list (no collaborations yet)")
                        return True
                else:
                    self.log_test("Collaboration Response Format", False, f"Expected list, got: {type(collaborations)}")
            else:
                self.log_test("Collaboration Response Format", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Collaboration Response Format", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_collaboration_tests(self):
        """Run all collaboration endpoint tests"""
        print("\n🤝 INFLUENCER COLLABORATION ENDPOINTS TESTS")
        print("=" * 60)
        
        # Test 1: Admin Authentication
        if not self.test_admin_authentication_for_collaborations():
            print("❌ Admin authentication failed - cannot proceed with collaboration tests")
            return
        
        # Test 2: GET collaborations endpoint
        existing_collaborations = self.test_get_collaborations_endpoint()
        
        # Test 3: Response format validation
        self.test_collaboration_response_format()
        
        # Test 4: Create new collaboration
        collaboration_id = self.test_create_collaboration_endpoint()
        
        # Test 5: Data persistence verification
        if collaboration_id:
            self.test_collaboration_data_persistence(collaboration_id)
        
        # Test 6: MongoDB collection verification
        self.test_mongodb_collaborations_collection()

    def run_all_tests(self):
        """Run comprehensive backend testing focusing on critical features"""
        print(f"🚀 STARTING COMPREHENSIVE BACKEND TESTING")
        print(f"Backend URL: {self.base_url}")
        print(f"Portal URL: {self.portal_url}")
        print(f"Payments URL: {self.payments_url}")
        print(f"SMS URL: {self.sms_url}")
        print(f"Testing critical features: Collaboration Endpoints, Payment Gateway, SMS Gateway, Influencer System, Partnership Requests, Services Management")
        print("=" * 80)
        
        # Test admin authentication with demo credentials
        if not self.test_admin_login():
            print("❌ Admin login failed - cannot proceed with tests")
            return False
        
        print(f"✅ Admin login successful with token: {self.admin_token[:20]}...")
        
        # Run collaboration tests first (as requested in review)
        self.run_collaboration_tests()
        
        # Run critical features tests as requested in review
        self.run_critical_features_tests()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BACKEND TEST SUMMARY")
        print("=" * 80)
        
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
            print("🎉 Payment & SMS Gateway integrations are working correctly!")
            print("💳 Iyzico Payment Gateway fully functional")
            print("📱 NetGSM SMS Gateway fully functional")
        
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

    def run_comprehensive_tests(self):
        """Run comprehensive tests for all new system features"""
        print("🚀 YENİ SİSTEM ÖZELLİKLERİ TESTİ BAŞLADI")
        print("=" * 60)
        
        # Test admin login first
        if not self.test_admin_login():
            print("❌ Admin girişi başarısız - testler durduruluyor")
            return False
        
        print("\n👥 EMPLOYEE MANAGEMENT SYSTEM TESTS:")
        print("-" * 45)
        
        # Test Employee Management System
        employees = self.test_get_employees()
        employee_id = self.test_create_employee()
        permissions = self.test_employee_permissions_available()
        
        print("\n🎫 SUPPORT TICKET SYSTEM TESTS:")
        print("-" * 35)
        
        # Test Support Ticket System
        tickets = self.test_get_support_tickets()
        ticket_id = self.test_create_support_ticket()
        
        print("\n🏢 COMPANY PROJECT MANAGEMENT TESTS:")
        print("-" * 40)
        
        # Test Company Project Management
        projects = self.test_get_company_projects()
        project_id = self.test_create_company_project()
        
        print("\n💾 DATABASE COLLECTIONS VERIFICATION:")
        print("-" * 40)
        
        # Verify Database Collections
        collections_status = self.verify_database_collections()
        
        return True


if __name__ == "__main__":
    # Run the new system features tests
    tester = NewSystemFeaturesTester()
    
    # Run comprehensive tests
    tester.run_comprehensive_tests()
    
    print("\n" + "=" * 60)
    print("📋 TEST SONUÇLARI:")
    print("=" * 60)
    
    passed_tests = len([r for r in tester.test_results if r["success"]])
    total_tests = len(tester.test_results)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"✅ Başarılı: {passed_tests}")
    print(f"❌ Başarısız: {total_tests - passed_tests}")
    print(f"📊 Başarı Oranı: {success_rate:.1f}%")
    
    if success_rate < 80:
        print("\n⚠️  UYARI: Düşük başarı oranı tespit edildi!")
        failed_tests = [r for r in tester.test_results if not r["success"]]
        print("Başarısız testler:")
        for test in failed_tests[:5]:  # Show first 5 failed tests
            print(f"  - {test['test']}: {test['message']}")
    
    # Show created items summary
    if any(tester.created_items.values()):
        print("\n📦 OLUŞTURULAN TEST VERİLERİ:")
        print("-" * 30)
        for item_type, items in tester.created_items.items():
            if items:
                print(f"  {item_type}: {len(items)} adet")
    
    print("\n🎯 YENİ SİSTEM ÖZELLİKLERİ TESTİ TAMAMLANDI!")
    print("=" * 60)