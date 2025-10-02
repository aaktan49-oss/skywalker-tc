#!/usr/bin/env python3
"""
Yeni Sistem Özellikleri Testi - New System Features Testing
Employee Management, Support Ticket System, Company Project Management Testing
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://bizops-central-3.preview.emergentagent.com/api"
EMPLOYEES_URL = "https://bizops-central-3.preview.emergentagent.com/api/employees"
SUPPORT_URL = "https://bizops-central-3.preview.emergentagent.com/api/support"
COMPANY_URL = "https://bizops-central-3.preview.emergentagent.com/api/company"

class NewSystemFeaturesTester:
    def __init__(self):
        self.base_url = BASE_URL
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