import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [users, setUsers] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [supportTickets, setSupportTickets] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [companyProjects, setCompanyProjects] = useState([]);
  const [partnershipRequests, setPartnershipRequests] = useState([]);
  const [contactMessages, setContactMessages] = useState([]);

  const token = localStorage.getItem('adminToken');
  const portalToken = localStorage.getItem('portalToken');
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  // API call helper
  const apiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
      });
      return await response.json();
    } catch (error) {
      console.error('API call error:', error);
      return { success: false, error: error.message };
    }
  };

  const portalApiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${portalToken}`,
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
      });
      return await response.json();
    } catch (error) {
      console.error('Portal API call error:', error);
      return { success: false, error: error.message };
    }
  };

  // Load functions
  const loadEmployees = async () => {
    try {
      const data = await portalApiCall('/api/portal/employees');
      setEmployees(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading employees:', error);
      setEmployees([]);
    }
  };

  const loadSupportTickets = async () => {
    try {
      const data = await portalApiCall('/api/portal/support/tickets');
      setSupportTickets(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading support tickets:', error);
      setSupportTickets([]);
    }
  };

  const loadCustomers = async () => {
    try {
      const data = await portalApiCall('/api/portal/support/customers');
      setCustomers(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading customers:', error);
      setCustomers([]);
    }
  };

  const loadCompanyProjects = async () => {
    try {
      const data = await portalApiCall('/api/portal/company/projects');
      setCompanyProjects(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading company projects:', error);
      setCompanyProjects([]);
    }
  };

  const loadPartnershipRequests = async () => {
    try {
      const data = await portalApiCall('/api/portal/admin/partner-requests');
      setPartnershipRequests(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading partnership requests:', error);
      setPartnershipRequests([]);
    }
  };

  const loadContactMessages = async () => {
    try {
      const data = await apiCall('/api/admin/contacts');
      setContactMessages(data.items || []);
    } catch (error) {
      console.error('Error loading contact messages:', error);
      setContactMessages([]);
    }
  };

  useEffect(() => {
    switch (activeSection) {
      case 'employees':
        loadEmployees();
        break;
      case 'support-tickets':
        loadSupportTickets();
        break;
      case 'customer-management':
        loadCustomers();
        break;
      case 'company-projects':
        loadCompanyProjects();
        break;
      case 'partnership-requests':
        loadPartnershipRequests();
        break;
      case 'contact-messages':
        loadContactMessages();
        break;
      default:
        break;
    }
  }, [activeSection]);

  const menuItems = [
    { id: 'overview', label: 'Genel Bakış', icon: '📊' },
    { id: 'employees', label: 'Çalışan Yönetimi', icon: '👨‍💻' },
    { id: 'support-tickets', label: 'Destek Talepleri', icon: '🎫' },
    { id: 'customer-management', label: 'Müşteri Yönetimi', icon: '👥' },
    { id: 'company-projects', label: 'Firma Projeleri', icon: '🏗️' },
    { id: 'partnership-requests', label: 'İş Ortağı Talepleri', icon: '🤝' },
    { id: 'contact-messages', label: 'İletişim Mesajları', icon: '📧' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg flex flex-col h-screen">
        <div className="p-6 border-b">
          <h1 className="text-xl font-bold text-gray-800">Admin Panel</h1>
        </div>
        <nav className="flex-1 p-4">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveSection(item.id)}
              className={`w-full text-left p-3 rounded-lg mb-2 flex items-center space-x-3 ${
                activeSection === item.id
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        <div className="max-w-6xl mx-auto">
          
          {/* Overview */}
          {activeSection === 'overview' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Genel Bakış</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">👨‍💻</div>
                  <h3 className="font-semibold text-gray-700">Çalışanlar</h3>
                  <p className="text-2xl font-bold text-blue-600">{employees.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">🎫</div>
                  <h3 className="font-semibold text-gray-700">Destek Talepleri</h3>
                  <p className="text-2xl font-bold text-green-600">{supportTickets.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">👥</div>
                  <h3 className="font-semibold text-gray-700">Müşteriler</h3>
                  <p className="text-2xl font-bold text-purple-600">{customers.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">📧</div>
                  <h3 className="font-semibold text-gray-700">İletişim Mesajları</h3>
                  <p className="text-2xl font-bold text-red-600">{contactMessages.length}</p>
                </div>
              </div>
            </div>
          )}

          {/* Employees */}
          {activeSection === 'employees' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">👨‍💻 Çalışan Yönetimi</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Çalışan Listesi</h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ad Soyad</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefon</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yetkiler</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {employees.length > 0 ? employees.map((employee) => (
                        <tr key={employee.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">
                              {employee.firstName} {employee.lastName}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{employee.email}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{employee.phone || 'N/A'}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {employee.permissions ? employee.permissions.join(', ') : 'N/A'}
                            </div>
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                            <div className="text-4xl mb-2">👨‍💻</div>
                            <div>Henüz çalışan eklenmemiş</div>
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Partnership Requests */}
          {activeSection === 'partnership-requests' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">🤝 İş Ortağı Talepleri</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Talep Listesi</h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Başlık</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategori</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Öncelik</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Durum</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tarih</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {partnershipRequests.length > 0 ? partnershipRequests.map((request) => (
                        <tr key={request.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{request.title}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{request.category}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{request.priority}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              request.status === 'open' ? 'bg-blue-100 text-blue-800' :
                              request.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                              request.status === 'resolved' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {request.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {new Date(request.createdAt).toLocaleDateString('tr-TR')}
                            </div>
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                            <div className="text-4xl mb-2">🤝</div>
                            <div>Henüz talep yok</div>
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Contact Messages */}
          {activeSection === 'contact-messages' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">📧 İletişim Mesajları</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Mesaj Listesi</h2>
                </div>
                <div className="divide-y divide-gray-200">
                  {contactMessages.length > 0 ? contactMessages.map((message) => (
                    <div key={message.id} className="p-6 hover:bg-gray-50">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-lg font-medium text-gray-900">{message.name}</h3>
                          <p className="text-sm text-gray-600">{message.email}</p>
                          <p className="mt-2 text-gray-800">{message.message}</p>
                        </div>
                        <div className="text-right">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            message.status === 'new' ? 'bg-blue-100 text-blue-800' :
                            message.status === 'read' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {message.status}
                          </span>
                          <div className="text-sm text-gray-500 mt-2">
                            {new Date(message.createdAt).toLocaleDateString('tr-TR')}
                          </div>
                        </div>
                      </div>
                    </div>
                  )) : (
                    <div className="p-12 text-center text-gray-500">
                      <div className="text-4xl mb-4">📧</div>
                      <p className="text-lg font-medium mb-2">Henüz mesaj yok</p>
                      <p>İletişim formundan gelen mesajlar burada görüntülenecek.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;