import React, { useState, useEffect } from 'react';
import FileUploader from '../FileUploader';

const AdminDashboard = ({ user, onLogout }) => {
  const [activeSection, setActiveSection] = useState('overview');
  const [users, setUsers] = useState([]);
  const [influencerApplications, setInfluencerApplications] = useState([]);
  const [collaborations, setCollaborations] = useState([]);
  const [partnerRequests, setPartnerRequests] = useState([]);
  const [logos, setLogos] = useState([]);
  const [siteContent, setSiteContent] = useState([]);
  const [siteSettings, setSiteSettings] = useState({});
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [news, setNews] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newCollaboration, setNewCollaboration] = useState({
    title: '',
    description: '',
    requirements: '',
    deliverables: [],
    category: '',
    budget: '',
    deadline: '',
    priority: 'medium',
    tags: [],
    minFollowers: '',
    maxFollowers: '',
    targetCategories: [],
    targetLocations: [],
    imageUrl: '',
    maxInfluencers: 1
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

  const loadInfluencerApplications = async () => {
    try {
      const result = await apiCall('/api/admin/influencer-requests', 'GET');
      setInfluencerApplications(result || []);
    } catch (error) {
      console.error('Error loading influencer applications:', error);
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
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/site-content`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setSiteContent(data || []);
    } catch (error) {
      console.error('Error loading site content:', error);
    }
  };

  const loadNews = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/news`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setNews(data || []);
    } catch (error) {
      console.error('Error loading news:', error);
    }
  };

  const loadProjects = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/projects`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setProjects(data || []);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const loadSiteSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/site-settings`);
      const data = await response.json();
      setSiteSettings(data || {});
    } catch (error) {
      console.error('Error loading site settings:', error);
    }
  };

  const loadUploadedFiles = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/files/list`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setUploadedFiles(data || []);
    } catch (error) {
      console.error('Error loading uploaded files:', error);
    }
  };

  const createCollaboration = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      
      // Prepare collaboration data
      const collaborationData = {
        ...newCollaboration,
        deliverables: newCollaboration.deliverables.filter(d => d.trim() !== ''),
        tags: newCollaboration.tags.filter(t => t.trim() !== ''),
        targetCategories: newCollaboration.targetCategories.filter(c => c.trim() !== ''),
        targetLocations: newCollaboration.targetLocations.filter(l => l.trim() !== ''),
        budget: newCollaboration.budget ? parseFloat(newCollaboration.budget) : null,
        minFollowers: newCollaboration.minFollowers ? parseInt(newCollaboration.minFollowers) : null,
        maxFollowers: newCollaboration.maxFollowers ? parseInt(newCollaboration.maxFollowers) : null,
        deadline: newCollaboration.deadline ? new Date(newCollaboration.deadline).toISOString() : null
      };
      
      const response = await fetch(`${API_BASE}/api/portal/admin/collaborations`, {
        method: 'POST',
        headers,
        body: JSON.stringify(collaborationData)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('İşbirliği başarıyla oluşturuldu!');
        setNewCollaboration({
          title: '',
          description: '',
          requirements: '',
          deliverables: [],
          category: '',
          budget: '',
          deadline: '',
          priority: 'medium',
          tags: [],
          minFollowers: '',
          maxFollowers: '',
          targetCategories: [],
          targetLocations: [],
          imageUrl: '',
          maxInfluencers: 1
        });
        loadCollaborations();
      } else {
        alert(result.detail || 'İşbirliği oluşturulurken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating collaboration:', error);
      alert('İşbirliği oluşturulurken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const loadCollaborations = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/portal/admin/collaborations`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setCollaborations(data || []);
    } catch (error) {
      console.error('Error loading collaborations:', error);
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

  const approveUser = async (userId) => {
    // Get user details for confirmation
    const user = users.find(u => u.id === userId);
    const userName = user ? `${user.firstName} ${user.lastName}` : 'Bu kullanıcı';
    const companyInfo = user && user.role === 'partner' && user.company ? ` (${user.company})` : '';
    
    if (!window.confirm(`${userName}${companyInfo} kullanıcısını onaylamak istediğinize emin misiniz?`)) return;

    try {
      const result = await apiCall(`/api/portal/admin/users/${userId}/approve`, 'PUT');
      if (result.success) {
        alert(`${userName}${companyInfo} başarıyla onaylandı!`);
        loadUsers();
      } else {
        alert(result.detail || 'Kullanıcı onaylanırken hata oluştu.');
      }
    } catch (error) {
      console.error('Error approving user:', error);
      alert('Kullanıcı onaylanırken hata oluştu.');
    }
  };

  const rejectUser = async (userId) => {
    // Get user details for confirmation
    const user = users.find(u => u.id === userId);
    const userName = user ? `${user.firstName} ${user.lastName}` : 'Bu kullanıcı';
    const companyInfo = user && user.role === 'partner' && user.company ? ` (${user.company})` : '';
    
    if (!window.confirm(`${userName}${companyInfo} kullanıcısını reddetmek istediğinize emin misiniz?`)) return;

    try {
      const result = await apiCall(`/api/portal/admin/users/${userId}/reject`, 'PUT');
      if (result.success) {
        alert(`${userName}${companyInfo} başarıyla reddedildi!`);
        loadUsers();
      } else {
        alert(result.detail || 'Kullanıcı reddedilirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error rejecting user:', error);
      alert('Kullanıcı reddedilirken hata oluştu.');
    }
  };

  const approveInfluencerApplication = async (applicationId) => {
    if (!window.confirm('Bu başvuruyu onaylamak istediğinize emin misiniz?')) return;

    try {
      const result = await apiCall(`/api/admin/influencer-requests/${applicationId}/approve`, 'PUT');
      if (result.success) {
        alert('Başvuru başarıyla onaylandı!');
        loadInfluencerApplications();
      } else {
        alert(result.detail || 'Başvuru onaylanırken hata oluştu.');
      }
    } catch (error) {
      console.error('Error approving application:', error);
      alert('Başvuru onaylanırken hata oluştu.');
    }
  };

  const rejectInfluencerApplication = async (applicationId) => {
    if (!window.confirm('Bu başvuruyu reddetmek istediğinize emin misiniz?')) return;

    try {
      const result = await apiCall(`/api/admin/influencer-requests/${applicationId}/reject`, 'PUT');
      if (result.success) {
        alert('Başvuru başarıyla reddedildi!');
        loadInfluencerApplications();
      } else {
        alert(result.detail || 'Başvuru reddedilirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error rejecting application:', error);
      alert('Başvuru reddedilirken hata oluştu.');
    }
  };

  const convertToPortalUser = async (application) => {
    if (!window.confirm('Bu başvuruyu portal kullanıcısına dönüştürmek istediğinize emin misiniz? Otomatik şifre oluşturulacak.')) return;

    try {
      const result = await apiCall(`/api/admin/influencer-requests/${application.id}/convert`, 'POST');
      if (result.success) {
        alert(`Portal kullanıcısı oluşturuldu! Email: ${application.email}, Şifre: ${result.password}`);
        loadInfluencerApplications();
        loadUsers();
      } else {
        alert(result.detail || 'Portal kullanıcısı oluşturulurken hata oluştu.');
      }
    } catch (error) {
      console.error('Error converting to portal user:', error);
      alert('Portal kullanıcısı oluşturulurken hata oluştu.');
    }
  };

  const deleteInfluencerApplication = async (applicationId) => {
    if (!window.confirm('Bu başvuruyu silmek istediğinize emin misiniz?')) return;

    try {
      const result = await apiCall(`/api/admin/influencer-requests/${applicationId}`, 'DELETE');
      if (result.success) {
        alert('Başvuru başarıyla silindi!');
        loadInfluencerApplications();
      } else {
        alert(result.detail || 'Başvuru silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting application:', error);
      alert('Başvuru silinirken hata oluştu.');
    }
  };

  const saveSiteSettings = async () => {
    setLoading(true);
    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const response = await fetch(`${API_BASE}/api/content/admin/site-settings`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(siteSettings)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Site ayarları başarıyla kaydedildi!');
        loadSiteSettings();
      } else {
        alert(result.detail || 'Site ayarları kaydedilirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error saving site settings:', error);
      alert('Site ayarları kaydedilirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const deleteFile = async (fileId) => {
    if (!window.confirm('Bu dosyayı silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/files/${fileId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Dosya başarıyla silindi!');
        loadUploadedFiles();
      } else {
        alert(result.detail || 'Dosya silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Dosya silinirken hata oluştu.');
    }
  };

  useEffect(() => {
    if (activeSection === 'users') {
      loadUsers();
    } else if (activeSection === 'influencer-applications') {
      loadInfluencerApplications();
    } else if (activeSection === 'collaborations') {
      loadCollaborations();
    } else if (activeSection === 'logos') {
      loadLogos();
    } else if (activeSection === 'site-content') {
      loadSiteContent();
    } else if (activeSection === 'site-settings') {
      loadSiteSettings();
    } else if (activeSection === 'file-manager') {
      loadUploadedFiles();
    } else if (activeSection === 'news') {
      loadNews();
    } else if (activeSection === 'projects') {
      loadProjects();
    }
  }, [activeSection]);

  const menuItems = [
    { id: 'overview', label: 'Genel Bakış', icon: '📊' },
    { id: 'users', label: 'Kullanıcı Yönetimi', icon: '👥' },
    { id: 'influencer-applications', label: 'Influencer Başvuruları', icon: '⭐' },
    { id: 'collaborations', label: 'İşbirlikleri', icon: '🤝' },
    { id: 'partner-requests', label: 'İş Ortağı Talepleri', icon: '📝' },
    { id: 'logos', label: 'Logo Yönetimi', icon: '🏢' },
    { id: 'site-content', label: 'Site İçerikleri', icon: '📄' },
    { id: 'site-settings', label: 'Site Ayarları', icon: '⚙️' },
    { id: 'file-manager', label: 'Dosya Yönetimi', icon: '📁' },
    { id: 'news', label: 'Haberler', icon: '📰' },
    { id: 'projects', label: 'Projelerimiz', icon: '🚀' }
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
                        Kullanıcı / Firma
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Rol & Detaylar
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Durum
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Kayıt Tarihi
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        İşlemler
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users && users.length > 0 ? users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {user.firstName} {user.lastName}
                              {user.role === 'partner' && user.company && (
                                <span className="ml-2 text-sm font-semibold text-blue-600">
                                  ({user.company})
                                </span>
                              )}
                            </div>
                            <div className="text-sm text-gray-500">{user.email}</div>
                            {user.phone && (
                              <div className="text-xs text-gray-400">📞 {user.phone}</div>
                            )}
                            {user.role === 'partner' && user.company && (
                              <div className="text-xs text-blue-600 font-medium">
                                🏢 {user.company}
                              </div>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full mb-2 ${
                              user.role === 'admin' ? 'bg-red-100 text-red-800' :
                              user.role === 'influencer' ? 'bg-blue-100 text-blue-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {user.role === 'admin' ? 'Admin' : 
                               user.role === 'influencer' ? 'Influencer' : 'İş Ortağı'}
                            </span>
                            
                            {/* Influencer Details */}
                            {user.role === 'influencer' && (
                              <div className="text-xs text-gray-600 space-y-1">
                                {user.instagram && <div>📱 {user.instagram}</div>}
                                {user.followersCount && <div>👥 {user.followersCount}</div>}
                                {user.category && <div>🏷️ {user.category}</div>}
                              </div>
                            )}
                            
                            {/* Partner Details */}
                            {user.role === 'partner' && (
                              <div className="text-xs text-gray-600 space-y-1">
                                {user.company && <div>🏢 {user.company}</div>}
                                {user.businessType && <div>💼 {user.businessType}</div>}
                              </div>
                            )}
                          </div>
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
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          {!user.isApproved ? (
                            <div className="flex space-x-2">
                              <button
                                onClick={() => approveUser(user.id)}
                                className="bg-green-600 text-white px-3 py-1 text-xs rounded-md hover:bg-green-700 transition-colors"
                              >
                                ✅ Onayla
                              </button>
                              <button
                                onClick={() => rejectUser(user.id)}
                                className="bg-red-600 text-white px-3 py-1 text-xs rounded-md hover:bg-red-700 transition-colors"
                              >
                                ❌ Reddet
                              </button>
                            </div>
                          ) : (
                            <span className="text-green-600 text-xs">✅ Onaylı</span>
                          )}
                        </td>
                      </tr>
                    )) : (
                      <tr>
                        <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                          <div className="text-4xl mb-4">👥</div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz kullanıcı yok</h3>
                          <p>Portal kayıtları henüz başlamadı.</p>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Influencer Applications */}
          {activeSection === 'influencer-applications' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Influencer Başvuruları</h1>
              <p className="text-gray-600 mb-6">Ana sitedeki influencer başvuru formundan gelen başvurular</p>
              
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Başvuru Listesi</h2>
                </div>
                
                <div className="divide-y divide-gray-200">
                  {influencerApplications && influencerApplications.length > 0 ? influencerApplications.map((application) => (
                    <div key={application.id} className="p-6 hover:bg-gray-50 transition-colors">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-3">
                            <div>
                              <h3 className="text-lg font-semibold text-gray-900">
                                {application.firstName} {application.lastName}
                              </h3>
                              {application.companyName && (
                                <p className="text-sm font-medium text-blue-600 mt-1">
                                  🏢 {application.companyName}
                                </p>
                              )}
                            </div>
                            <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${
                              application.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              application.status === 'approved' ? 'bg-green-100 text-green-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {application.status === 'pending' ? 'Beklemede' :
                               application.status === 'approved' ? 'Onaylandı' : 'Reddedildi'}
                            </span>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-600">
                            <div>
                              <strong>Email:</strong> {application.email}
                            </div>
                            <div>
                              <strong>Telefon:</strong> {application.phone || 'Belirtilmemiş'}
                            </div>
                            <div>
                              <strong>Instagram:</strong> {application.instagram || 'Belirtilmemiş'}
                            </div>
                            <div>
                              <strong>Takipçi:</strong> {application.followersRange || 'Belirtilmemiş'}
                            </div>
                            <div>
                              <strong>Kategori:</strong> {application.category || 'Belirtilmemiş'}
                            </div>
                            <div>
                              <strong>Deneyim:</strong> {application.experience || 'Belirtilmemiş'}
                            </div>
                          </div>
                          
                          {application.message && (
                            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                              <p className="text-sm text-gray-600">
                                <strong>Mesaj:</strong> {application.message}
                              </p>
                            </div>
                          )}
                          
                          <div className="mt-3 flex items-center text-xs text-gray-500 space-x-4">
                            <span>
                              Başvuru Tarihi: {new Date(application.createdAt).toLocaleDateString('tr-TR')}
                            </span>
                            {application.city && <span>Şehir: {application.city}</span>}
                          </div>
                        </div>
                        
                        <div className="ml-6 flex flex-col space-y-2">
                          {application.status === 'pending' && (
                            <>
                              <button
                                onClick={() => approveInfluencerApplication(application.id)}
                                className="bg-green-600 text-white px-4 py-2 text-sm rounded-md hover:bg-green-700 transition-colors"
                              >
                                ✅ Onayla
                              </button>
                              <button
                                onClick={() => rejectInfluencerApplication(application.id)}
                                className="bg-red-600 text-white px-4 py-2 text-sm rounded-md hover:bg-red-700 transition-colors"
                              >
                                ❌ Reddet
                              </button>
                              <button
                                onClick={() => convertToPortalUser(application)}
                                className="bg-blue-600 text-white px-4 py-2 text-sm rounded-md hover:bg-blue-700 transition-colors"
                              >
                                👤 Portal Kullanıcısı Yap
                              </button>
                            </>
                          )}
                          
                          <button
                            onClick={() => deleteInfluencerApplication(application.id)}
                            className="bg-gray-600 text-white px-4 py-2 text-sm rounded-md hover:bg-gray-700 transition-colors"
                          >
                            🗑️ Sil
                          </button>
                        </div>
                      </div>
                    </div>
                  )) : (
                    <div className="p-8 text-center text-gray-500">
                      <div className="text-4xl mb-4">⭐</div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz başvuru yok</h3>
                      <p>Ana siteden influencer başvurusu bekleniyor.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Collaborations */}
          {activeSection === 'collaborations' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">İşbirlikleri</h1>
              
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni İşbirliği Oluştur</h2>
                
                <form onSubmit={createCollaboration} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Başlık *
                      </label>
                      <input
                        type="text"
                        value={newCollaboration.title}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, title: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="İşbirliği başlığı"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Kategori *
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
                        <option value="genel">Genel</option>
                      </select>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Açıklama *
                    </label>
                    <textarea
                      value={newCollaboration.description}
                      onChange={(e) => setNewCollaboration({ ...newCollaboration, description: e.target.value })}
                      required
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="İşbirliği detaylarını açıklayın"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Gereksinimler
                    </label>
                    <textarea
                      value={newCollaboration.requirements}
                      onChange={(e) => setNewCollaboration({ ...newCollaboration, requirements: e.target.value })}
                      rows="2"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="Özel gereksinimler varsa belirtin"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Bütçe (₺)
                      </label>
                      <input
                        type="number"
                        min="0"
                        value={newCollaboration.budget}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, budget: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="0"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Son Tarih
                      </label>
                      <input
                        type="date"
                        value={newCollaboration.deadline}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, deadline: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Öncelik
                      </label>
                      <select
                        value={newCollaboration.priority}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, priority: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="low">Düşük</option>
                        <option value="medium">Orta</option>
                        <option value="high">Yüksek</option>
                        <option value="urgent">Acil</option>
                      </select>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-3">Hedefleme</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Min. Takipçi
                        </label>
                        <input
                          type="number"
                          min="0"
                          value={newCollaboration.minFollowers}
                          onChange={(e) => setNewCollaboration({ ...newCollaboration, minFollowers: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="1000"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Max. Takipçi
                        </label>
                        <input
                          type="number"
                          min="0"
                          value={newCollaboration.maxFollowers}
                          onChange={(e) => setNewCollaboration({ ...newCollaboration, maxFollowers: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="100000"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Görsel URL
                      </label>
                      <input
                        type="url"
                        value={newCollaboration.imageUrl}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, imageUrl: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="https://example.com/image.jpg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Max. Influencer Sayısı
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="10"
                        value={newCollaboration.maxInfluencers}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, maxInfluencers: parseInt(e.target.value) || 1 })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Görsel URL
                      </label>
                      <input
                        type="url"
                        value={newCollaboration.imageUrl}
                        onChange={(e) => setNewCollaboration({ ...newCollaboration, imageUrl: e.target.value })}
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
              
              <div className="space-y-8">
                {/* Quick Actions */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Hızlı İşlemler</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <button
                      onClick={() => setActiveContentSection('hero')}
                      className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
                    >
                      <div className="text-2xl mb-2">🏠</div>
                      <div className="text-sm font-medium">Ana Sayfa Hero</div>
                    </button>
                    <button
                      onClick={() => setActiveContentSection('services')}
                      className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
                    >
                      <div className="text-2xl mb-2">🎯</div>
                      <div className="text-sm font-medium">Hizmetler</div>
                    </button>
                    <button
                      onClick={() => setActiveContentSection('team')}
                      className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
                    >
                      <div className="text-2xl mb-2">👥</div>
                      <div className="text-sm font-medium">Takım</div>
                    </button>
                    <button
                      onClick={() => setActiveContentSection('all')}
                      className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
                    >
                      <div className="text-2xl mb-2">📄</div>
                      <div className="text-sm font-medium">Tümü</div>
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Content Creation Form */}
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
                            <option value="hero_section">🏠 Hero Section</option>
                            <option value="services">🎯 Hizmetler</option>
                            <option value="about">ℹ️ Hakkımızda</option>
                            <option value="team">👥 Takım</option>
                            <option value="testimonials">💬 Referanslar</option>
                            <option value="faq">❓ S.S.S.</option>
                            <option value="contact">📞 İletişim</option>
                            <option value="header_nav">🧭 Header Nav</option>
                            <option value="footer">🦶 Footer</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Anahtar *</label>
                          <input
                            type="text"
                            value={newSiteContent.key}
                            onChange={(e) => setNewSiteContent({ ...newSiteContent, key: e.target.value })}
                            required
                            placeholder="main_title, service_1 vb."
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Başlık</label>
                          <input
                            type="text"
                            value={newSiteContent.title}
                            onChange={(e) => setNewSiteContent({ ...newSiteContent, title: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="Ana başlık"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Alt Başlık</label>
                          <input
                            type="text"
                            value={newSiteContent.subtitle || ''}
                            onChange={(e) => setNewSiteContent({ ...newSiteContent, subtitle: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="Alt başlık"
                          />
                        </div>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">İçerik</label>
                        <textarea
                          value={newSiteContent.content}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, content: e.target.value })}
                          rows="3"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="İçerik metni"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Görsel</label>
                        <FileUploader 
                          accept="image/*"
                          category="site_content"
                          onFileUploaded={(file) => setNewSiteContent({ ...newSiteContent, imageUrl: `${API_BASE}${file.url}` })}
                          className="mb-2"
                        />
                        {newSiteContent.imageUrl && (
                          <div className="mt-2">
                            <img src={newSiteContent.imageUrl} alt="Preview" className="h-20 w-auto rounded" />
                          </div>
                        )}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Link URL</label>
                          <input
                            type="url"
                            value={newSiteContent.linkUrl || ''}
                            onChange={(e) => setNewSiteContent({ ...newSiteContent, linkUrl: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://example.com"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Link Metni</label>
                          <input
                            type="text"
                            value={newSiteContent.linkText || ''}
                            onChange={(e) => setNewSiteContent({ ...newSiteContent, linkText: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="Daha Fazla Bilgi"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Sıra</label>
                        <input
                          type="number"
                          value={newSiteContent.order}
                          onChange={(e) => setNewSiteContent({ ...newSiteContent, order: parseInt(e.target.value) || 0 })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          min="0"
                        />
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

                  {/* Existing Content List */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut İçerikler</h2>
                    
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {siteContent && siteContent.length > 0 ? siteContent
                        .filter(content => 
                          !activeContentSection || 
                          activeContentSection === 'all' || 
                          content.section === activeContentSection
                        )
                        .map((content) => (
                          <div key={content.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                                  {content.section}
                                </span>
                                <span className="font-medium text-gray-900">{content.key}</span>
                              </div>
                              <p className="font-medium text-gray-800">{content.title}</p>
                              {content.subtitle && (
                                <p className="text-sm text-gray-600">{content.subtitle}</p>
                              )}
                              {content.content && (
                                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{content.content}</p>
                              )}
                              <div className="flex items-center space-x-2 mt-2 text-xs text-gray-500">
                                <span>Sıra: {content.order}</span>
                                {content.imageUrl && <span>🖼️ Görsel var</span>}
                                {content.linkUrl && <span>🔗 Link var</span>}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <button
                                onClick={() => editSiteContent(content)}
                                className="text-blue-600 hover:text-blue-800 text-sm"
                              >
                                ✏️ Düzenle
                              </button>
                              <button
                                onClick={() => deleteSiteContent(content.id)}
                                className="text-red-600 hover:text-red-800 text-sm"
                              >
                                🗑️ Sil
                              </button>
                            </div>
                          </div>
                        )) : (
                          <div className="p-6 text-center text-gray-500">
                            <div className="text-4xl mb-4">📄</div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz içerik yok</h3>
                            <p>İlk içeriği eklemek için yanındaki formu kullanın.</p>
                          </div>
                        )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Site Settings */}
          {activeSection === 'site-settings' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Site Ayarları</h1>
              
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Genel Site Ayarları</h2>
                
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Site Adı</label>
                      <input
                        type="text"
                        value={siteSettings.siteName || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, siteName: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Skywalker.tc"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Site Sloganı</label>
                      <input
                        type="text"
                        value={siteSettings.siteTagline || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, siteTagline: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Trendyol Galaksisinde Liderlik"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Site Açıklaması</label>
                    <textarea
                      value={siteSettings.siteDescription || ''}
                      onChange={(e) => setSiteSettings({ ...siteSettings, siteDescription: e.target.value })}
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="E-ticaret dünyasında rehberiniz"
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Ana Renk</label>
                      <input
                        type="color"
                        value={siteSettings.primaryColor || '#8B5CF6'}
                        onChange={(e) => setSiteSettings({ ...siteSettings, primaryColor: e.target.value })}
                        className="w-full h-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">İkinci Renk</label>
                      <input
                        type="color"
                        value={siteSettings.secondaryColor || '#3B82F6'}
                        onChange={(e) => setSiteSettings({ ...siteSettings, secondaryColor: e.target.value })}
                        className="w-full h-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">İletişim Email</label>
                      <input
                        type="email"
                        value={siteSettings.contactEmail || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, contactEmail: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="info@skywalker.tc"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">İletişim Telefon</label>
                      <input
                        type="tel"
                        value={siteSettings.contactPhone || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, contactPhone: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="+90 555 000 0000"
                      />
                    </div>
                  </div>

                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Logo ve Görseller</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Site Logo</label>
                        <FileUploader 
                          accept="image/*"
                          category="logo"
                          onFileUploaded={(file) => setSiteSettings({ ...siteSettings, logoUrl: `${API_BASE}${file.url}` })}
                          className="mb-2"
                        />
                        {siteSettings.logoUrl && (
                          <div className="mt-2">
                            <img src={siteSettings.logoUrl} alt="Logo" className="h-16 w-auto" />
                          </div>
                        )}
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Favicon</label>
                        <FileUploader 
                          accept="image/*"
                          category="favicon"
                          onFileUploaded={(file) => setSiteSettings({ ...siteSettings, faviconUrl: `${API_BASE}${file.url}` })}
                          className="mb-2"
                        />
                        {siteSettings.faviconUrl && (
                          <div className="mt-2">
                            <img src={siteSettings.faviconUrl} alt="Favicon" className="h-8 w-8" />
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={saveSiteSettings}
                      disabled={loading}
                      className="bg-purple-600 text-white py-2 px-6 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Kaydediliyor...' : 'Ayarları Kaydet'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* File Manager */}
          {activeSection === 'file-manager' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Dosya Yönetimi</h1>
              
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Dosya Yükle</h2>
                  <FileUploader 
                    accept="image/*,video/*,.pdf,.doc,.docx"
                    multiple={true}
                    onFileUploaded={(file) => {
                      setUploadedFiles(prev => [file, ...prev]);
                    }}
                  />
                </div>

                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <div className="p-6 border-b">
                    <h2 className="text-xl font-bold text-gray-900">Yüklenen Dosyalar</h2>
                  </div>
                  
                  <div className="divide-y divide-gray-200">
                    {uploadedFiles && uploadedFiles.length > 0 ? uploadedFiles.map((file) => (
                      <div key={file.id} className="p-6">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            {file.category === 'image' ? (
                              <img 
                                src={`${API_BASE}${file.url}`} 
                                alt={file.filename}
                                className="h-16 w-16 object-cover rounded-lg"
                              />
                            ) : (
                              <div className="h-16 w-16 bg-gray-100 rounded-lg flex items-center justify-center">
                                <span className="text-2xl">
                                  {file.category === 'video' ? '🎥' : 
                                   file.category === 'document' ? '📄' : '📁'}
                                </span>
                              </div>
                            )}
                            <div>
                              <h3 className="text-sm font-medium text-gray-900">{file.filename}</h3>
                              <div className="text-sm text-gray-500 space-x-4">
                                <span>Kategori: {file.category}</span>
                                <span>Boyut: {(file.file_size / 1024 / 1024).toFixed(2)} MB</span>
                              </div>
                              <div className="text-xs text-gray-400 mt-1">
                                URL: {`${API_BASE}${file.url}`}
                              </div>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => navigator.clipboard.writeText(`${API_BASE}${file.url}`)}
                              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                            >
                              📋 URL Kopyala
                            </button>
                            <button
                              onClick={() => deleteFile(file.id)}
                              className="text-red-600 hover:text-red-800 text-sm font-medium"
                            >
                              🗑️ Sil
                            </button>
                          </div>
                        </div>
                      </div>
                    )) : (
                      <div className="p-8 text-center text-gray-500">
                        <div className="text-4xl mb-4">📁</div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz dosya yok</h3>
                        <p>Yukarıdaki yükleme alanını kullanarak dosya yükleyin.</p>
                      </div>
                    )}
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
                  )) : (
                    <div className="p-6 text-center text-gray-500">
                      <div className="text-4xl mb-4">📰</div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz haber yok</h3>
                      <p>İlk haberi eklemek için yukarıdaki formu kullanın.</p>
                    </div>
                  )}
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
                  {projects && projects.length > 0 ? projects.map((project) => (
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
                  )) : (
                    <div className="p-6 text-center text-gray-500">
                      <div className="text-4xl mb-4">🚀</div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz proje yok</h3>
                      <p>İlk projeyi eklemek için yukarıdaki formu kullanın.</p>
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