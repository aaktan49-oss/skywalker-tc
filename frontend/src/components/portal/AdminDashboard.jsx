import React, { useState, useEffect } from 'react';

const AdminDashboard = ({ user, onLogout }) => {
  const [activeSection, setActiveSection] = useState('overview');
  const [users, setUsers] = useState([]);
  const [collaborations, setCollaborations] = useState([]);
  const [partnerRequests, setPartnerRequests] = useState([]);
  const [logos, setLogos] = useState([]);
  const [siteContent, setSiteContent] = useState([]);
  const [news, setNews] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newCollaboration, setNewCollaboration] = useState({
    title: '',
    description: '',
    category: '',
    prBoxImage: '',
    requirements: '',
    budget: ''
  });
  const [newLogo, setNewLogo] = useState({
    name: '',
    logoUrl: '',
    order: 0
  });
  const [newSiteContent, setNewSiteContent] = useState({
    section: 'hero_section',
    key: '',
    title: '',
    content: '',
    imageUrl: '',
    order: 0
  });
  const [newNews, setNewNews] = useState({
    title: '',
    content: '',
    excerpt: '',
    imageUrl: '',
    category: 'company_news',
    isPublished: true
  });
  const [newProject, setNewProject] = useState({
    clientName: '',
    clientEmail: '',
    projectTitle: '',
    description: '',
    category: '',
    startDate: '',
    endDate: '',
    status: 'completed',
    results: '',
    imageUrl: '',
    images: [],
    tags: [],
    isPublic: true
  });

  const API_BASE = process.env.REACT_APP_BACKEND_URL;
  const token = localStorage.getItem('portal_token');

  const apiCall = async (endpoint, method = 'GET', data = null) => {
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (method !== 'GET' && data) {
      config.body = JSON.stringify(data);
    }

    // Add authorization via query parameter for now
    const url = `${API_BASE}${endpoint}${endpoint.includes('?') ? '&' : '?'}Authorization=Bearer ${token}`;
    
    const response = await fetch(url, config);
    return response.json();
  };

  const loadUsers = async () => {
    try {
      const data = await apiCall('/api/portal/admin/users');
      setUsers(data.items || []);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const loadLogos = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/portal/logos`);
      const data = await response.json();
      setLogos(data || []);
    } catch (error) {
      console.error('Error loading logos:', error);
    }
  };

  const loadSiteContent = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/admin/site-content?Authorization=Bearer ${token}`);
      const data = await response.json();
      setSiteContent(data || []);
    } catch (error) {
      console.error('Error loading site content:', error);
    }
  };

  const loadNews = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/admin/news?Authorization=Bearer ${token}`);
      const data = await response.json();
      setNews(data || []);
    } catch (error) {
      console.error('Error loading news:', error);
    }
  };

  const loadProjects = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/admin/projects?Authorization=Bearer ${token}`);
      const data = await response.json();
      setProjects(data || []);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const createCollaboration = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await apiCall('/api/portal/admin/collaborations', 'POST', newCollaboration);
      if (result.success) {
        alert('İşbirliği başarıyla oluşturuldu!');
        setNewCollaboration({
          title: '',
          description: '',
          category: '',
          prBoxImage: '',
          requirements: '',
          budget: ''
        });
      }
    } catch (error) {
      console.error('Error creating collaboration:', error);
      alert('İşbirliği oluşturulurken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createLogo = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await apiCall('/api/portal/admin/logos', 'POST', newLogo);
      if (result.success) {
        alert('Logo başarıyla eklendi!');
        setNewLogo({ name: '', logoUrl: '', order: 0 });
        loadLogos();
      }
    } catch (error) {
      console.error('Error creating logo:', error);
      alert('Logo eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createSiteContent = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const response = await fetch(`${API_BASE}/api/content/admin/site-content`, {
        method: 'POST',
        headers,
        body: JSON.stringify(newSiteContent)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Site içeriği başarıyla eklendi!');
        setNewSiteContent({ section: 'hero_section', key: '', title: '', content: '', imageUrl: '', order: 0 });
        loadSiteContent();
      } else {
        alert(result.detail || 'İçerik eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating site content:', error);
      alert('İçerik eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createNews = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const response = await fetch(`${API_BASE}/api/content/admin/news`, {
        method: 'POST',
        headers,
        body: JSON.stringify(newNews)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Haber başarıyla eklendi!');
        setNewNews({ title: '', content: '', excerpt: '', imageUrl: '', category: 'company_news', isPublished: true });
        loadNews();
      } else {
        alert(result.detail || 'Haber eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating news:', error);
      alert('Haber eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const projectData = {
        ...newProject,
        tags: newProject.tags.filter(tag => tag.trim() !== ''),
        images: newProject.images.filter(img => img.trim() !== '')
      };
      
      const response = await fetch(`${API_BASE}/api/content/admin/projects`, {
        method: 'POST',
        headers,
        body: JSON.stringify(projectData)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Proje başarıyla eklendi!');
        setNewProject({
          clientName: '', clientEmail: '', projectTitle: '', description: '', category: '',
          startDate: '', endDate: '', status: 'completed', results: '', imageUrl: '',
          images: [], tags: [], isPublic: true
        });
        loadProjects();
      } else {
        alert(result.detail || 'Proje eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating project:', error);
      alert('Proje eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const deleteLogo = async (logoId) => {
    if (!window.confirm('Bu logoyu silmek istediğinize emin misiniz?')) return;

    try {
      const result = await apiCall(`/api/portal/admin/logos/${logoId}`, 'DELETE');
      if (result.success) {
        alert('Logo başarıyla silindi!');
        loadLogos();
      }
    } catch (error) {
      console.error('Error deleting logo:', error);
      alert('Logo silinirken hata oluştu.');
    }
  };

  const deleteSiteContent = async (contentId) => {
    if (!window.confirm('Bu içeriği silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/site-content/${contentId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('İçerik başarıyla silindi!');
        loadSiteContent();
      } else {
        alert(result.detail || 'İçerik silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting site content:', error);
      alert('İçerik silinirken hata oluştu.');
    }
  };

  const deleteNews = async (newsId) => {
    if (!window.confirm('Bu haberi silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/news/${newsId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Haber başarıyla silindi!');
        loadNews();
      } else {
        alert(result.detail || 'Haber silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting news:', error);
      alert('Haber silinirken hata oluştu.');
    }
  };

  const deleteProject = async (projectId) => {
    if (!window.confirm('Bu projeyi silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/projects/${projectId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Proje başarıyla silindi!');
        loadProjects();
      } else {
        alert(result.detail || 'Proje silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting project:', error);
      alert('Proje silinirken hata oluştu.');
    }
  };

  useEffect(() => {
    if (activeSection === 'users') {
      loadUsers();
    } else if (activeSection === 'logos') {
      loadLogos();
    } else if (activeSection === 'site-content') {
      loadSiteContent();
    } else if (activeSection === 'news') {
      loadNews();
    } else if (activeSection === 'projects') {
      loadProjects();
    }
  }, [activeSection]);

  const menuItems = [
    { id: 'overview', label: 'Genel Bakış', icon: '📊' },
    { id: 'users', label: 'Kullanıcı Yönetimi', icon: '👥' },
    { id: 'collaborations', label: 'İşbirlikleri', icon: '🤝' },
    { id: 'partner-requests', label: 'İş Ortağı Talepleri', icon: '📝' },
    { id: 'logos', label: 'Logo Yönetimi', icon: '🏢' },
    { id: 'site-content', label: 'Site İçerikleri', icon: '📄' },
    { id: 'news', label: 'Haberler', icon: '📰' },
    { id: 'projects', label: 'Projelerimiz', icon: '🚀' },
    { id: 'settings', label: 'Ayarlar', icon: '⚙️' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold text-gray-800">Admin Panel</h2>
          <p className="text-sm text-gray-600">Hoşgeldin, {user.firstName}</p>
        </div>
        
        <nav className="mt-6">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveSection(item.id)}
              className={`w-full flex items-center px-6 py-3 text-left hover:bg-purple-50 transition-colors ${
                activeSection === item.id ? 'bg-purple-100 text-purple-700 border-r-2 border-purple-600' : 'text-gray-700'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-6 left-6">
          <button
            onClick={onLogout}
            className="flex items-center text-gray-600 hover:text-red-600 transition-colors"
          >
            <span className="mr-2">🚪</span>
            Çıkış Yap
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        <div className="max-w-6xl mx-auto">
          
          {/* Overview */}
          {activeSection === 'overview' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Genel Bakış</h1>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <span className="text-2xl">👥</span>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-semibold text-gray-900">Toplam Kullanıcı</h3>
                      <p className="text-2xl font-bold text-blue-600">{users.length}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <span className="text-2xl">🤝</span>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-semibold text-gray-900">Aktif İşbirlikleri</h3>
                      <p className="text-2xl font-bold text-green-600">{collaborations.length}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-yellow-100 rounded-lg">
                      <span className="text-2xl">📝</span>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-semibold text-gray-900">Bekleyen Talepler</h3>
                      <p className="text-2xl font-bold text-yellow-600">{partnerRequests.length}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <span className="text-2xl">🏢</span>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-semibold text-gray-900">Şirket Logoları</h3>
                      <p className="text-2xl font-bold text-purple-600">{logos.length}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Son Aktiviteler</h2>
                <div className="space-y-3">
                  <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-green-600 mr-3">✅</span>
                    <div>
                      <p className="font-medium">Sistem başarıyla çalışıyor</p>
                      <p className="text-sm text-gray-600">Tüm API endpoint'leri aktif</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Users Management */}
          {activeSection === 'users' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Kullanıcı Yönetimi</h1>
              
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Kullanıcı
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Rol
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Durum
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Kayıt Tarihi
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {user.firstName} {user.lastName}
                            </div>
                            <div className="text-sm text-gray-500">{user.email}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            user.role === 'admin' ? 'bg-red-100 text-red-800' :
                            user.role === 'influencer' ? 'bg-blue-100 text-blue-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            user.isApproved ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {user.isApproved ? 'Onaylandı' : 'Beklemede'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(user.createdAt).toLocaleDateString('tr-TR')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Collaborations */}
          {activeSection === 'collaborations' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">İşbirlikleri</h1>
              
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni İşbirliği Oluştur</h2>
                
                <form onSubmit={createCollaboration} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Başlık
                      </label>
                      <input
                        type="text"
                        value={newCollaboration.title}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, title: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Kategori
                      </label>
                      <select
                        value={newCollaboration.category}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, category: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="">Seçiniz</option>
                        <option value="moda">Moda</option>
                        <option value="kozmetik">Kozmetik</option>
                        <option value="teknoloji">Teknoloji</option>
                        <option value="spor">Spor</option>
                        <option value="yasam">Yaşam Tarzı</option>
                        <option value="yiyecek">Yiyecek & İçecek</option>
                      </select>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Açıklama
                    </label>
                    <textarea
                      value={newCollaboration.description}
                      onChange={(e) => setNewCollaboration({ ...newCollaboration, description: e.target.value })}
                      required
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        PR Kutu Görseli (URL)
                      </label>
                      <input
                        type="url"
                        value={newCollaboration.prBoxImage}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, prBoxImage: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Bütçe
                      </label>
                      <input
                        type="text"
                        value={newCollaboration.budget}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, budget: e.target.value })}
                        placeholder="Örn: 5000-10000 TL"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Gereksinimler
                    </label>
                    <textarea
                      value={newCollaboration.requirements}
                      onChange={(e) => setNewCollaboration({ ...newCollaboration, requirements: e.target.value })}
                      rows="2"
                      placeholder="İşbirliği için gerekli koşullar"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                  >
                    {loading ? 'Oluşturuluyor...' : 'İşbirliği Oluştur'}
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Logo Management */}
          {activeSection === 'logos' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Logo Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Logo Ekle</h2>
                  
                  <form onSubmit={createLogo} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Şirket Adı
                      </label>
                      <input
                        type="text"
                        value={newLogo.name}
                        onChange={(e) => setNewLogo({ ...newLogo, name: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Logo URL
                      </label>
                      <input
                        type="url"
                        value={newLogo.logoUrl}
                        onChange={(e) => setNewLogo({ ...newLogo, logoUrl: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Sıra
                      </label>
                      <input
                        type="number"
                        value={newLogo.order}
                        onChange={(e) => setNewLogo({ ...newLogo, order: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Ekleniyor...' : 'Logo Ekle'}
                    </button>
                  </form>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut Logolar</h2>
                  
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {logos.map((logo) => (
                      <div key={logo.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center">
                          <img 
                            src={logo.logoUrl} 
                            alt={logo.name}
                            className="w-12 h-8 object-contain mr-3"
                            onError={(e) => {
                              e.target.src = 'https://via.placeholder.com/150x60/6B46C1/FFFFFF?text=LOGO';
                            }}
                          />
                          <div>
                            <p className="font-medium">{logo.name}</p>
                            <p className="text-sm text-gray-600">Sıra: {logo.order}</p>
                          </div>
                        </div>
                        <button
                          onClick={() => deleteLogo(logo.id)}
                          className="text-red-600 hover:text-red-800 transition-colors"
                        >
                          🗑️
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Site Content Management */}
          {activeSection === 'site-content' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Site İçerik Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni İçerik Ekle</h2>
                  
                  <form onSubmit={createSiteContent} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Bölüm</label>
                        <select
                          value={newSiteContent.section}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, section: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="hero_section">Hero Section</option>
                          <option value="services">Hizmetler</option>
                          <option value="about">Hakkımızda</option>
                          <option value="team">Takım</option>
                          <option value="testimonials">Referanslar</option>
                          <option value="faq">S.S.S.</option>
                          <option value="contact">İletişim</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Anahtar</label>
                        <input
                          type="text"
                          value={newSiteContent.key}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, key: e.target.value })}
                          required
                          placeholder="main_title, description vb."
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Başlık</label>
                      <input
                        type="text"
                        value={newSiteContent.title}
                        onChange={(e) => setNewSiteContent({ ...newSiteContent, title: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">İçerik</label>
                      <textarea
                        value={newSiteContent.content}
                        onChange={(e) => setNewSiteContent({ ...newSiteContent, content: e.target.value })}
                        rows="3"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Görsel URL</label>
                        <input
                          type="url"
                          value={newSiteContent.imageUrl}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, imageUrl: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Sıra</label>
                        <input
                          type="number"
                          value={newSiteContent.order}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, order: parseInt(e.target.value) })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Ekleniyor...' : 'İçerik Ekle'}
                    </button>
                  </form>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut İçerikler</h2>
                  
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {siteContent.map((content) => (
                      <div key={content.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">{content.title || content.key}</p>
                          <p className="text-sm text-gray-600">{content.section} - Sıra: {content.order}</p>
                          {content.content && (
                            <p className="text-sm text-gray-500 mt-1 truncate">{content.content}</p>
                          )}
                        </div>
                        <button
                          onClick={() => deleteSiteContent(content.id)}
                          className="text-red-600 hover:text-red-800 transition-colors"
                        >
                          🗑️
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* News Management */}
          {activeSection === 'news' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Haber Yönetimi</h1>
              
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Haber Ekle</h2>
                
                <form onSubmit={createNews} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Başlık</label>
                      <input
                        type="text"
                        value={newNews.title}
                        onChange={(e) => setNewNews({ ...newNews, title: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Kategori</label>
                      <select
                        value={newNews.category}
                        onChange={(e) => setNewNews({ ...newNews, category: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="company_news">Şirket Haberleri</option>
                        <option value="success_stories">Başarı Hikayeleri</option>
                        <option value="industry_news">Sektör Haberleri</option>
                        <option value="announcements">Duyurular</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Durum</label>
                      <select
                        value={newNews.isPublished}
                        onChange={(e) => setNewNews({ ...newNews, isPublished: e.target.value === 'true' })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="true">Yayınlandı</option>
                        <option value="false">Taslak</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Özet</label>
                    <textarea
                      value={newNews.excerpt}
                      onChange={(e) => setNewNews({ ...newNews, excerpt: e.target.value })}
                      rows="2"
                      placeholder="Kısa özet..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">İçerik</label>
                    <textarea
                      value={newNews.content}
                      onChange={(e) => setNewNews({ ...newNews, content: e.target.value })}
                      required
                      rows="5"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Görsel URL</label>
                    <input
                      type="url"
                      value={newNews.imageUrl}
                      onChange={(e) => setNewNews({ ...newNews, imageUrl: e.target.value })}
                      placeholder="https://example.com/image.jpg"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                  >
                    {loading ? 'Ekleniyor...' : 'Haber Ekle'}
                  </button>
                </form>
              </div>

              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Mevcut Haberler</h2>
                </div>
                <div className="divide-y divide-gray-200">
                  {news && news.length > 0 ? news.map((article) => (
                    <div key={article.id} className="p-6">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 mb-2">{article.title}</h3>
                          <div className="flex items-center space-x-4 mb-3">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              article.category === 'company_news' ? 'bg-blue-100 text-blue-800' :
                              article.category === 'success_stories' ? 'bg-green-100 text-green-800' :
                              article.category === 'industry_news' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-purple-100 text-purple-800'
                            }`}>
                              {article.category === 'company_news' ? 'Şirket Haberi' :
                               article.category === 'success_stories' ? 'Başarı Hikayesi' :
                               article.category === 'industry_news' ? 'Sektör Haberi' : 'Duyuru'}
                            </span>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              article.isPublished ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {article.isPublished ? 'Yayında' : 'Taslak'}
                            </span>
                            <span className="text-sm text-gray-500">
                              {new Date(article.createdAt).toLocaleDateString('tr-TR')}
                            </span>
                          </div>
                          {article.excerpt && (
                            <p className="text-gray-600 mb-2">{article.excerpt}</p>
                          )}
                          <p className="text-sm text-gray-500 line-clamp-2">{article.content}</p>
                        </div>
                        <button
                          onClick={() => deleteNews(article.id)}
                          className="ml-4 text-red-600 hover:text-red-800 transition-colors"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Projects Management */}
          {activeSection === 'projects' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Proje Yönetimi</h1>
              
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Proje Ekle</h2>
                
                <form onSubmit={createProject} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Müşteri Adı</label>
                      <input
                        type="text"
                        value={newProject.clientName}
                        onChange={(e) => setNewProject({ ...newProject, clientName: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Müşteri Email</label>
                      <input
                        type="email"
                        value={newProject.clientEmail}
                        onChange={(e) => setNewProject({ ...newProject, clientEmail: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Proje Başlığı</label>
                    <input
                      type="text"
                      value={newProject.projectTitle}
                      onChange={(e) => setNewProject({ ...newProject, projectTitle: e.target.value })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Kategori</label>
                      <input
                        type="text"
                        value={newProject.category}
                        onChange={(e) => setNewProject({ ...newProject, category: e.target.value })}
                        required
                        placeholder="E-commerce Optimization, Social Media vb."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Durum</label>
                      <select
                        value={newProject.status}
                        onChange={(e) => setNewProject({ ...newProject, status: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="completed">Tamamlandı</option>
                        <option value="in_progress">Devam Ediyor</option>
                        <option value="planned">Planlandı</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Açıklama</label>
                    <textarea
                      value={newProject.description}
                      onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                      required
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Sonuçlar</label>
                    <textarea
                      value={newProject.results}
                      onChange={(e) => setNewProject({ ...newProject, results: e.target.value })}
                      rows="2"
                      placeholder="Satışlar %150 arttı, ROI %200 gelişti"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Başlama Tarihi</label>
                      <input
                        type="date"
                        value={newProject.startDate}
                        onChange={(e) => setNewProject({ ...newProject, startDate: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Bitiş Tarihi</label>
                      <input
                        type="date"
                        value={newProject.endDate}
                        onChange={(e) => setNewProject({ ...newProject, endDate: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Ana Görsel URL</label>
                    <input
                      type="url"
                      value={newProject.imageUrl}
                      onChange={(e) => setNewProject({ ...newProject, imageUrl: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div className="flex items-center space-x-4">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={newProject.isPublic}
                        onChange={(e) => setNewProject({ ...newProject, isPublic: e.target.checked })}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-700">Herkese açık (portfolio'da göster)</span>
                    </label>
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                  >
                    {loading ? 'Ekleniyor...' : 'Proje Ekle'}
                  </button>
                </form>
              </div>

              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Mevcut Projeler</h2>
                </div>
                <div className="divide-y divide-gray-200">
                  {projects.map((project) => (
                    <div key={project.id} className="p-6">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">{project.projectTitle}</h3>
                            <div className="flex items-center space-x-2">
                              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                project.status === 'completed' ? 'bg-green-100 text-green-800' :
                                project.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-blue-100 text-blue-800'
                              }`}>
                                {project.status === 'completed' ? 'Tamamlandı' :
                                 project.status === 'in_progress' ? 'Devam Ediyor' : 'Planlandı'}
                              </span>
                              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                project.isPublic ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                              }`}>
                                {project.isPublic ? 'Herkese Açık' : 'Özel'}
                              </span>
                            </div>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">
                            <span className="font-semibold">Müşteri:</span> {project.clientName} | 
                            <span className="font-semibold"> Kategori:</span> {project.category}
                          </p>
                          <p className="text-gray-600 mb-2">{project.description}</p>
                          {project.results && (
                            <p className="text-sm text-green-600 mb-2">
                              <span className="font-semibold">Sonuçlar:</span> {project.results}
                            </p>
                          )}
                          <div className="flex items-center text-xs text-gray-500 space-x-4">
                            {project.startDate && (
                              <span>Başlama: {new Date(project.startDate).toLocaleDateString('tr-TR')}</span>
                            )}
                            {project.endDate && (
                              <span>Bitiş: {new Date(project.endDate).toLocaleDateString('tr-TR')}</span>
                            )}
                          </div>
                        </div>
                        <button
                          onClick={() => deleteProject(project.id)}
                          className="ml-4 text-red-600 hover:text-red-800 transition-colors"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  ))}
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