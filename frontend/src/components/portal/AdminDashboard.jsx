import React, { useState, useEffect } from 'react';

const AdminDashboard = ({ user, onLogout }) => {
  const [activeSection, setActiveSection] = useState('overview');
  const [users, setUsers] = useState([]);
  const [collaborations, setCollaborations] = useState([]);
  const [partnerRequests, setPartnerRequests] = useState([]);
  const [logos, setLogos] = useState([]);
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

  useEffect(() => {
    if (activeSection === 'users') {
      loadUsers();
    } else if (activeSection === 'logos') {
      loadLogos();
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

        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;