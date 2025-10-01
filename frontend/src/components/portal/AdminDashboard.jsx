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
  const [activeContentSection, setActiveContentSection] = useState('all');
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
    subtitle: '',
    content: '',
    imageUrl: '',
    linkUrl: '',
    linkText: '',
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
  const [teamMembers, setTeamMembers] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [newTeamMember, setNewTeamMember] = useState({
    name: '',
    position: '',
    department: '',
    bio: '',
    imageUrl: '',
    email: '',
    linkedin: '',
    twitter: '',
    expertise: [],
    order: 0
  });
  const [newTestimonial, setNewTestimonial] = useState({
    clientName: '',
    clientPosition: '',
    clientCompany: '',
    content: '',
    rating: 5,
    imageUrl: '',
    projectType: '',
    order: 0,
    isFeatured: false
  });
  const [newFaq, setNewFaq] = useState({
    question: '',
    answer: '',
    category: '',
    order: 0
  });
  const [notifications, setNotifications] = useState([]);
  const [newNotification, setNewNotification] = useState({
    title: '',
    content: '',
    type: 'announcement',
    isGlobal: true,
    targetUsers: [],
    startDate: '',
    endDate: ''
  });
  const [newsletterSubscribers, setNewsletterSubscribers] = useState([]);
  const [leads, setLeads] = useState([]);
  const [analytics, setAnalytics] = useState({});
  
  // Services (Galaktik Hizmetler) state
  const [services, setServices] = useState([]);
  const [newService, setNewService] = useState({
    title: '',
    description: '',
    shortDescription: '',
    serviceType: 'e-ticaret',
    price: null,
    duration: '',
    icon: '🛸',
    imageUrl: '',
    color: '#8B5CF6',
    features: [],
    deliverables: [],
    requirements: [],
    processSteps: [],
    timeline: '',
    isActive: true,
    isFeatured: false,
    showPrice: true,
    order: 0,
    tags: [],
    metaTitle: '',
    metaDescription: ''
  });
  
  // Payment Management state
  const [paymentTransactions, setPaymentTransactions] = useState([]);
  const [paymentStats, setPaymentStats] = useState({});
  
  // SMS Management state
  const [smsTransactions, setSmsTransactions] = useState([]);
  const [smsStats, setSmsStats] = useState({});
  const [smsTemplates, setSmsTemplates] = useState([]);
  const [newSmsTemplate, setNewSmsTemplate] = useState({
    name: '',
    triggerType: '',
    template: '',
    variables: []
  });

  const API_BASE = process.env.REACT_APP_BACKEND_URL;
  const token = localStorage.getItem('portal_token');

  const apiCall = async (endpoint, method = 'GET', data = null) => {
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    if (method !== 'GET' && data) {
      config.body = JSON.stringify(data);
    }

    const url = `${API_BASE}${endpoint}`;
    
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

  const loadTeamMembers = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/team`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setTeamMembers(data || []);
    } catch (error) {
      console.error('Error loading team members:', error);
    }
  };

  const loadTestimonials = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/testimonials`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setTestimonials(data || []);
    } catch (error) {
      console.error('Error loading testimonials:', error);
    }
  };

  const loadFaqs = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/faqs`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setFaqs(data || []);
    } catch (error) {
      console.error('Error loading FAQs:', error);
    }
  };

  const loadNotifications = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/notifications`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setNotifications(data || []);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  };

  const loadNewsletterSubscribers = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/marketing/admin/newsletter/subscribers`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setNewsletterSubscribers(data || []);
    } catch (error) {
      console.error('Error loading newsletter subscribers:', error);
    }
  };

  const loadLeads = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/marketing/admin/leads`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setLeads(data || []);
    } catch (error) {
      console.error('Error loading leads:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/marketing/admin/analytics/dashboard?days=30`, {
        method: 'GET',
        headers
      });
      const data = await response.json();
      setAnalytics(data || {});
    } catch (error) {
      console.error('Error loading analytics:', error);
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
      
      const contentData = {
        section: newSiteContent.section,
        key: newSiteContent.key,
        title: newSiteContent.title || null,
        subtitle: newSiteContent.subtitle || null,
        content: newSiteContent.content || null,
        imageUrl: newSiteContent.imageUrl || null,
        linkUrl: newSiteContent.linkUrl || null,
        linkText: newSiteContent.linkText || null,
        order: newSiteContent.order || 0
      };
      
      const url = newSiteContent.editingId 
        ? `${API_BASE}/api/content/admin/site-content/${newSiteContent.editingId}`
        : `${API_BASE}/api/content/admin/site-content`;
      
      const method = newSiteContent.editingId ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(contentData)
      });
      const result = await response.json();
      
      if (result.success) {
        alert(newSiteContent.editingId ? 'İçerik başarıyla güncellendi!' : 'Site içeriği başarıyla eklendi!');
        setNewSiteContent({
          section: 'hero_section',
          key: '',
          title: '',
          subtitle: '',
          content: '',
          imageUrl: '',
          linkUrl: '',
          linkText: '',
          order: 0
        });
        loadSiteContent();
      } else {
        alert(result.detail || 'İçerik kaydedilirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error saving site content:', error);
      alert('İçerik kaydedilirken hata oluştu.');
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

  // ===== SERVICES (GALAKTIK HIZMETLER) FUNCTIONS =====
  
  const loadServices = async () => {
    try {
      const data = await apiCall('/api/services/admin/all');
      setServices(data.data?.services || []);
    } catch (error) {
      console.error('Error loading services:', error);
    }
  };

  const createService = async () => {
    if (!newService.title || !newService.description || !newService.shortDescription) {
      alert('Lütfen zorunlu alanları doldurun.');
      return;
    }

    try {
      const result = await apiCall('/api/services/admin/create', 'POST', newService);
      if (result.success) {
        alert('Hizmet başarıyla oluşturuldu!');
        setNewService({
          title: '',
          description: '',
          shortDescription: '',
          serviceType: 'e-ticaret',
          price: null,
          duration: '',
          icon: '🛸',
          imageUrl: '',
          color: '#8B5CF6',
          features: [],
          deliverables: [],
          requirements: [],
          processSteps: [],
          timeline: '',
          isActive: true,
          isFeatured: false,
          showPrice: true,
          order: 0,
          tags: [],
          metaTitle: '',
          metaDescription: ''
        });
        loadServices();
      } else {
        alert(result.detail || 'Hizmet oluşturulurken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating service:', error);
      alert('Hizmet oluşturulurken hata oluştu.');
    }
  };

  const deleteService = async (serviceId) => {
    if (!window.confirm('Bu hizmeti silmek istediğinize emin misiniz?')) return;

    try {
      const result = await apiCall(`/api/services/admin/${serviceId}`, 'DELETE');
      if (result.success) {
        alert('Hizmet başarıyla silindi!');
        loadServices();
      } else {
        alert(result.detail || 'Hizmet silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting service:', error);
      alert('Hizmet silinirken hata oluştu.');
    }
  };

  const toggleServiceActive = async (serviceId) => {
    try {
      const result = await apiCall(`/api/services/admin/${serviceId}/toggle-active`, 'POST');
      if (result.success) {
        alert(result.message);
        loadServices();
      } else {
        alert(result.detail || 'Hizmet durumu güncellenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error toggling service:', error);
      alert('Hizmet durumu güncellenirken hata oluştu.');
    }
  };

  const toggleServiceFeatured = async (serviceId) => {
    try {
      const result = await apiCall(`/api/services/admin/${serviceId}/toggle-featured`, 'POST');
      if (result.success) {
        alert(result.message);
        loadServices();
      } else {
        alert(result.detail || 'Hizmet öne çıkarma durumu güncellenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error toggling service featured:', error);
      alert('Hizmet öne çıkarma durumu güncellenirken hata oluştu.');
    }
  };

  // ===== PAYMENT MANAGEMENT FUNCTIONS =====
  
  const loadPaymentTransactions = async () => {
    try {
      const data = await apiCall('/api/payments/admin/transactions');
      setPaymentTransactions(data.data?.transactions || []);
    } catch (error) {
      console.error('Error loading payment transactions:', error);
    }
  };

  const loadPaymentStats = async () => {
    try {
      const data = await apiCall('/api/payments/admin/stats');
      setPaymentStats(data.data || {});
    } catch (error) {
      console.error('Error loading payment stats:', error);
    }
  };

  // ===== SMS MANAGEMENT FUNCTIONS =====
  
  const loadSmsTransactions = async () => {
    try {
      const data = await apiCall('/api/sms/admin/transactions');
      setSmsTransactions(data.data?.transactions || []);
    } catch (error) {
      console.error('Error loading SMS transactions:', error);
    }
  };

  const loadSmsStats = async () => {
    try {
      const data = await apiCall('/api/sms/admin/stats');
      setSmsStats(data.data || {});
    } catch (error) {
      console.error('Error loading SMS stats:', error);
    }
  };

  const loadSmsTemplates = async () => {
    try {
      const data = await apiCall('/api/sms/templates');
      setSmsTemplates(data.data || []);
    } catch (error) {
      console.error('Error loading SMS templates:', error);
    }
  };

  const createSmsTemplate = async () => {
    if (!newSmsTemplate.name || !newSmsTemplate.template) {
      alert('Lütfen zorunlu alanları doldurun.');
      return;
    }

    try {
      const result = await apiCall('/api/sms/templates', 'POST', newSmsTemplate);
      if (result.success) {
        alert('SMS şablonu başarıyla oluşturuldu!');
        setNewSmsTemplate({
          name: '',
          triggerType: '',
          template: '',
          variables: []
        });
        loadSmsTemplates();
      } else {
        alert(result.detail || 'SMS şablonu oluşturulurken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating SMS template:', error);
      alert('SMS şablonu oluşturulurken hata oluştu.');
    }
  };

  const sendTestSms = async () => {
    const phoneNumber = prompt('SMS göndermek için telefon numarası girin (örn: +905551234567):');
    const message = prompt('Gönderilecek mesajı girin:');
    
    if (!phoneNumber || !message) {
      alert('Telefon numarası ve mesaj gereklidir.');
      return;
    }

    try {
      const result = await apiCall('/api/sms/send', 'POST', {
        phoneNumber,
        message,
        priority: 'high'
      });
      if (result.success) {
        alert('Test SMS başarıyla gönderildi!');
        loadSmsTransactions();
      } else {
        alert(result.message || 'SMS gönderilirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error sending test SMS:', error);
      alert('SMS gönderilirken hata oluştu.');
    }
  };

  // ===== useEffect - Data Loading Based on Active Section =====
  
  useEffect(() => {
    // Load data based on active section
    switch(activeSection) {
      case 'users':
        loadUsers();
        break;
      case 'influencer-applications':
        loadInfluencerApplications();
        break;
      case 'collaborations':
        // loadCollaborations(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'logos':
        // loadLogos(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'site-content':
        // loadSiteContent(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'news':
        // loadNews(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'projects':
        // loadProjects(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'team':
        // loadTeamMembers(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'testimonials':
        // loadTestimonials(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'faqs':
        // loadFaqs(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'notifications':
        // loadNotifications(); // Bu fonksiyonu da implement edebiliriz
        break;
      case 'services':
        loadServices();
        break;
      case 'payments':
        loadPaymentTransactions();
        loadPaymentStats();
        break;
      case 'sms':
        loadSmsTransactions();
        loadSmsStats();
        loadSmsTemplates();
        break;
      case 'analytics':
        // loadAnalytics(); // Bu fonksiyonu da implement edebiliriz
        break;
      default:
        // Overview veya diğer bölümler için genel yükleme
        break;
    }
  }, [activeSection]); // activeSection değiştiğinde çalışır

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

  const createTeamMember = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const memberData = {
        ...newTeamMember,
        expertise: newTeamMember.expertise.filter(skill => skill.trim() !== '')
      };
      
      const response = await fetch(`${API_BASE}/api/content/admin/team`, {
        method: 'POST',
        headers,
        body: JSON.stringify(memberData)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Takım üyesi başarıyla eklendi!');
        setNewTeamMember({
          name: '', position: '', department: '', bio: '', imageUrl: '',
          email: '', linkedin: '', twitter: '', expertise: [], order: 0
        });
        loadTeamMembers();
      } else {
        alert(result.detail || 'Takım üyesi eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating team member:', error);
      alert('Takım üyesi eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createTestimonial = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const response = await fetch(`${API_BASE}/api/content/admin/testimonials`, {
        method: 'POST',
        headers,
        body: JSON.stringify(newTestimonial)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Referans başarıyla eklendi!');
        setNewTestimonial({
          clientName: '', clientPosition: '', clientCompany: '', content: '',
          rating: 5, imageUrl: '', projectType: '', order: 0, isFeatured: false
        });
        loadTestimonials();
      } else {
        alert(result.detail || 'Referans eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating testimonial:', error);
      alert('Referans eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const createFaq = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const response = await fetch(`${API_BASE}/api/content/admin/faqs`, {
        method: 'POST',
        headers,
        body: JSON.stringify(newFaq)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('S.S.S. başarıyla eklendi!');
        setNewFaq({ question: '', answer: '', category: '', order: 0 });
        loadFaqs();
      } else {
        alert(result.detail || 'S.S.S. eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating FAQ:', error);
      alert('S.S.S. eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const deleteTeamMember = async (memberId) => {
    if (!window.confirm('Bu takım üyesini silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/team/${memberId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Takım üyesi başarıyla silindi!');
        loadTeamMembers();
      } else {
        alert(result.detail || 'Takım üyesi silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting team member:', error);
      alert('Takım üyesi silinirken hata oluştu.');
    }
  };

  const deleteTestimonial = async (testimonialId) => {
    if (!window.confirm('Bu referansı silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/testimonials/${testimonialId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Referans başarıyla silindi!');
        loadTestimonials();
      } else {
        alert(result.detail || 'Referans silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting testimonial:', error);
      alert('Referans silinirken hata oluştu.');
    }
  };

  const deleteFaq = async (faqId) => {
    if (!window.confirm('Bu S.S.S. öğesini silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/faqs/${faqId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('S.S.S. başarıyla silindi!');
        loadFaqs();
      } else {
        alert(result.detail || 'S.S.S. silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting FAQ:', error);
      alert('S.S.S. silinirken hata oluştu.');
    }
  };

  const createNotification = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const headers = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
      const notificationData = {
        ...newNotification,
        startDate: newNotification.startDate ? new Date(newNotification.startDate).toISOString() : null,
        endDate: newNotification.endDate ? new Date(newNotification.endDate).toISOString() : null
      };
      
      const response = await fetch(`${API_BASE}/api/content/admin/notifications`, {
        method: 'POST',
        headers,
        body: JSON.stringify(notificationData)
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Bildirim başarıyla eklendi!');
        setNewNotification({
          title: '', content: '', type: 'announcement', isGlobal: true,
          targetUsers: [], startDate: '', endDate: ''
        });
        loadNotifications();
      } else {
        alert(result.detail || 'Bildirim eklenirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error creating notification:', error);
      alert('Bildirim eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const deleteNotification = async (notificationId) => {
    if (!window.confirm('Bu bildirimi silmek istediğinize emin misiniz?')) return;

    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE}/api/content/admin/notifications/${notificationId}`, {
        method: 'DELETE',
        headers
      });
      const result = await response.json();
      
      if (result.success) {
        alert('Bildirim başarıyla silindi!');
        loadNotifications();
      } else {
        alert(result.detail || 'Bildirim silinirken hata oluştu.');
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
      alert('Bildirim silinirken hata oluştu.');
    }
  };

  const editSiteContent = (content) => {
    setNewSiteContent({
      section: content.section,
      key: content.key,
      title: content.title || '',
      subtitle: content.subtitle || '',
      content: content.content || '',
      imageUrl: content.imageUrl || '',
      linkUrl: content.linkUrl || '',
      linkText: content.linkText || '',
      order: content.order || 0,
      editingId: content.id
    });
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
    } else if (activeSection === 'team') {
      loadTeamMembers();
    } else if (activeSection === 'testimonials') {
      loadTestimonials();
    } else if (activeSection === 'faqs') {
      loadFaqs();
    } else if (activeSection === 'notifications') {
      loadNotifications();
    } else if (activeSection === 'newsletter') {
      loadNewsletterSubscribers();
    } else if (activeSection === 'leads') {
      loadLeads();
    } else if (activeSection === 'analytics') {
      loadAnalytics();
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
    { id: 'projects', label: 'Projelerimiz', icon: '🚀' },
    { id: 'team', label: 'Takım Yönetimi', icon: '👨‍💼' },
    { id: 'testimonials', label: 'Referanslar', icon: '🏢' },
    { id: 'faqs', label: 'S.S.S. Yönetimi', icon: '❓' },
    { id: 'notifications', label: 'Bildirim Sistemi', icon: '🔔' },
    { id: 'newsletter', label: 'Newsletter', icon: '📧' },
    { id: 'leads', label: 'Potansiyel Müşteriler', icon: '👤' },
    { id: 'analytics', label: 'Analytics', icon: '📊' },
    { id: 'services', label: 'Galaktik Hizmetler', icon: '🛸' },
    { id: 'payments', label: 'Ödeme Yönetimi', icon: '💳' },
    { id: 'sms', label: 'SMS Yönetimi', icon: '📱' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg flex flex-col h-screen">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold text-gray-800">Admin Panel</h2>
          <p className="text-sm text-gray-600">Hoşgeldin, {user.firstName}</p>
        </div>
        
        <nav className="mt-6 flex-1 overflow-y-auto">
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

        <div className="mt-auto pt-6 border-t border-gray-200">
          <button
            onClick={onLogout}
            className="flex items-center w-full px-4 py-2 text-gray-600 hover:text-red-600 hover:bg-red-50 transition-colors rounded-lg"
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
                        {loading ? 
                          (newSiteContent.editingId ? 'Güncelleniyor...' : 'Ekleniyor...') : 
                          (newSiteContent.editingId ? 'İçeriği Güncelle' : 'İçerik Ekle')
                        }
                      </button>
                      
                      {newSiteContent.editingId && (
                        <button
                          type="button"
                          onClick={() => setNewSiteContent({
                            section: 'hero_section', key: '', title: '', subtitle: '', content: '', 
                            imageUrl: '', linkUrl: '', linkText: '', order: 0
                          })}
                          className="w-full mt-2 bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600 transition-colors"
                        >
                          İptal Et
                        </button>
                      )}
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
              
              <div className="space-y-6">
                {/* Genel Site Ayarları */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Genel Site Ayarları</h2>
                  
                  <div className="space-y-4">
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
                        <label className="block text-sm font-medium text-gray-700 mb-1">İletişim Email</label>
                        <input
                          type="email"
                          value={siteSettings.contactEmail || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, contactEmail: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="info@skywalker.tc"
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
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Adres</label>
                        <input
                          type="text"
                          value={siteSettings.address || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, address: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="İstanbul, Türkiye"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">WhatsApp Numarası</label>
                        <input
                          type="tel"
                          value={siteSettings.whatsappNumber || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, whatsappNumber: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="+90 555 123 45 67"
                        />
                      </div>
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
                  </div>
                </div>

                {/* SEO & Analytics */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">SEO & Analytics Ayarları</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Meta Başlık</label>
                      <input
                        type="text"
                        value={siteSettings.metaTitle || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, metaTitle: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Skywalker.tc - E-ticaret Danışmanlığı"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Meta Açıklama</label>
                      <textarea
                        value={siteSettings.metaDescription || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, metaDescription: e.target.value })}
                        rows="3"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Trendyol ve e-ticaret platformlarında uzman danışmanlık hizmetleri..."
                      />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Google Analytics ID</label>
                        <input
                          type="text"
                          value={siteSettings.googleAnalyticsId || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, googleAnalyticsId: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="G-XXXXXXXXXX"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Google Ads ID</label>
                        <input
                          type="text"
                          value={siteSettings.googleAdsId || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, googleAdsId: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="AW-XXXXXXXXX"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Google Tag Manager ID</label>
                        <input
                          type="text"
                          value={siteSettings.googleTagManagerId || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, googleTagManagerId: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="GTM-XXXXXXX"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Facebook Pixel ID</label>
                        <input
                          type="text"
                          value={siteSettings.facebookPixelId || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, facebookPixelId: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="123456789012345"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Doğrulama Kodları */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Site Doğrulama Kodları</h2>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Google Search Console</label>
                        <input
                          type="text"
                          value={siteSettings.googleVerificationCode || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, googleVerificationCode: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="google-site-verification=XXXXXX"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Meta (Facebook) Doğrulama</label>
                        <input
                          type="text"
                          value={siteSettings.metaVerificationCode || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, metaVerificationCode: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="facebook-domain-verification=XXXXXX"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Bing Doğrulama</label>
                        <input
                          type="text"
                          value={siteSettings.bingVerificationCode || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, bingVerificationCode: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="msvalidate.01=XXXXXX"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Yandex Doğrulama</label>
                        <input
                          type="text"
                          value={siteSettings.yandexVerificationCode || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, yandexVerificationCode: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="yandex-verification=XXXXXX"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Sosyal Medya Ayarları */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Sosyal Medya Ayarları</h2>
                  
                  <div className="space-y-6">
                    {/* Sosyal Medya Hesapları */}
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Sosyal Medya Hesapları</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">🐦 Twitter</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.twitter || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, twitter: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://twitter.com/skywalker_tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">📘 Facebook</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.facebook || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, facebook: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://facebook.com/skywalker.tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">📷 Instagram</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.instagram || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, instagram: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://instagram.com/skywalker.tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">💼 LinkedIn</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.linkedin || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, linkedin: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://linkedin.com/company/skywalker-tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">📺 YouTube</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.youtube || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, youtube: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://youtube.com/@skywalker-tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">🎵 TikTok</label>
                          <input
                            type="url"
                            value={siteSettings.socialMedia?.tiktok || ''}
                            onChange={(e) => setSiteSettings({ 
                              ...siteSettings, 
                              socialMedia: { ...siteSettings.socialMedia, tiktok: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="https://tiktok.com/@skywalker.tc"
                          />
                        </div>
                      </div>
                    </div>

                    {/* SEO / Open Graph Ayarları */}
                    <div className="border-t pt-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">SEO / Open Graph Ayarları</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Open Graph Başlık</label>
                          <input
                            type="text"
                            value={siteSettings.ogTitle || ''}
                            onChange={(e) => setSiteSettings({ ...siteSettings, ogTitle: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="Skywalker.tc"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Twitter Kullanıcı Adı</label>
                          <input
                            type="text"
                            value={siteSettings.twitterSite || ''}
                            onChange={(e) => setSiteSettings({ ...siteSettings, twitterSite: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="@skywalker_tc"
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Open Graph Açıklama</label>
                      <textarea
                        value={siteSettings.ogDescription || ''}
                        onChange={(e) => setSiteSettings({ ...siteSettings, ogDescription: e.target.value })}
                        rows="2"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="E-ticaret danışmanlığında uzman ekip..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Open Graph Görseli</label>
                      <FileUploader 
                        accept="image/*"
                        category="og_image"
                        onFileUploaded={(file) => setSiteSettings({ ...siteSettings, ogImage: `${API_BASE}${file.url}` })}
                        className="mb-2"
                      />
                      {siteSettings.ogImage && (
                        <div className="mt-2">
                          <img src={siteSettings.ogImage} alt="OG Image" className="h-20 w-auto rounded" />
                        </div>
                      )}
                      <p className="text-xs text-gray-500 mt-1">Önerilen boyut: 1200x630px</p>
                    </div>
                  </div>
                </div>

                {/* Logo ve Görseller */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Logo ve Görseller</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Site Logo</label>
                      <FileUploader 
                        accept="image/*"
                        category="logo"
                        onFileUploaded={(file) => setSiteSettings({ ...siteSettings, logo: `${API_BASE}${file.url}` })}
                        className="mb-2"
                      />
                      {siteSettings.logo && (
                        <div className="mt-2">
                          <img src={siteSettings.logo} alt="Logo" className="h-16 w-auto" />
                        </div>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Favicon</label>
                      <FileUploader 
                        accept="image/*"
                        category="favicon"
                        onFileUploaded={(file) => setSiteSettings({ ...siteSettings, favicon: `${API_BASE}${file.url}` })}
                        className="mb-2"
                      />
                      {siteSettings.favicon && (
                        <div className="mt-2">
                          <img src={siteSettings.favicon} alt="Favicon" className="h-8 w-8" />
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Özellik Ayarları */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Özellik Ayarları</h2>
                  
                  <div className="space-y-4">
                    <div className="flex items-center space-x-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={siteSettings.newsletterEnabled || false}
                          onChange={(e) => setSiteSettings({ ...siteSettings, newsletterEnabled: e.target.checked })}
                          className="mr-2"
                        />
                        <span className="text-sm font-medium text-gray-700">Newsletter Sistemi Aktif</span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={siteSettings.liveChatEnabled || false}
                          onChange={(e) => setSiteSettings({ ...siteSettings, liveChatEnabled: e.target.checked })}
                          className="mr-2"
                        />
                        <span className="text-sm font-medium text-gray-700">Canlı Destek Aktif</span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={siteSettings.cookieConsentEnabled || false}
                          onChange={(e) => setSiteSettings({ ...siteSettings, cookieConsentEnabled: e.target.checked })}
                          className="mr-2"
                        />
                        <span className="text-sm font-medium text-gray-700">Çerez Onayı</span>
                      </label>
                    </div>

                    {siteSettings.liveChatEnabled && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Canlı Destek Widget Kodu</label>
                        <textarea
                          value={siteSettings.liveChatWidget || ''}
                          onChange={(e) => setSiteSettings({ ...siteSettings, liveChatWidget: e.target.value })}
                          rows="4"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="<!-- Tawk.to, Intercom vb. widget kodu buraya -->"
                        />
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex justify-end">
                  <button
                    onClick={saveSiteSettings}
                    disabled={loading}
                    className="bg-purple-600 text-white py-3 px-8 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors text-lg font-semibold"
                  >
                    {loading ? 'Kaydediliyor...' : 'Tüm Ayarları Kaydet'}
                  </button>
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

          {/* Team Management */}
          {activeSection === 'team' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Takım Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Team Member Creation Form */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Takım Üyesi Ekle</h2>
                  
                  <form onSubmit={createTeamMember} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Ad Soyad *</label>
                        <input
                          type="text"
                          value={newTeamMember.name}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, name: e.target.value })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="Ahmet Yılmaz"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Pozisyon *</label>
                        <input
                          type="text"
                          value={newTeamMember.position}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, position: e.target.value })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="E-ticaret Uzmanı"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Departman *</label>
                        <select
                          value={newTeamMember.department}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, department: e.target.value })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="">Seçiniz</option>
                          <option value="E-ticaret">E-ticaret</option>
                          <option value="Pazarlama">Pazarlama</option>
                          <option value="Teknoloji">Teknoloji</option>
                          <option value="Tasarım">Tasarım</option>
                          <option value="Satış">Satış</option>
                          <option value="Yönetim">Yönetim</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <input
                          type="email"
                          value={newTeamMember.email}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, email: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="ahmet@skywalker.tc"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Biyografi</label>
                      <textarea
                        value={newTeamMember.bio}
                        onChange={(e) => setNewTeamMember({ ...newTeamMember, bio: e.target.value })}
                        rows="3"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Takım üyesi hakkında kısa bilgi..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Profil Fotoğrafı</label>
                      <FileUploader 
                        accept="image/*"
                        category="team_photos"
                        onFileUploaded={(file) => setNewTeamMember({ ...newTeamMember, imageUrl: `${API_BASE}${file.url}` })}
                        className="mb-2"
                      />
                      {newTeamMember.imageUrl && (
                        <div className="mt-2">
                          <img src={newTeamMember.imageUrl} alt="Preview" className="h-20 w-20 rounded-full object-cover" />
                        </div>
                      )}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn</label>
                        <input
                          type="url"
                          value={newTeamMember.linkedin}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, linkedin: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="https://linkedin.com/in/..."
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Sıra</label>
                        <input
                          type="number"
                          value={newTeamMember.order}
                          onChange={(e) => setNewTeamMember({ ...newTeamMember, order: parseInt(e.target.value) || 0 })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                    
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Ekleniyor...' : 'Takım Üyesi Ekle'}
                    </button>
                  </form>
                </div>

                {/* Team Members List */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut Takım Üyeleri</h2>
                  
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {teamMembers.map((member) => (
                      <div key={member.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center">
                          {member.imageUrl && (
                            <img 
                              src={member.imageUrl} 
                              alt={member.name}
                              className="w-12 h-12 rounded-full object-cover mr-4"
                            />
                          )}
                          <div>
                            <h3 className="font-semibold text-gray-900">{member.name}</h3>
                            <p className="text-sm text-gray-600">{member.position} - {member.department}</p>
                            <p className="text-xs text-gray-500">Sıra: {member.order}</p>
                          </div>
                        </div>
                        <button
                          onClick={() => deleteTeamMember(member.id)}
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

          {/* Testimonials Management */}
          {activeSection === 'testimonials' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Referans Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Testimonial Creation Form */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Referans Ekle</h2>
                  
                  <form onSubmit={createTestimonial} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Müşteri Adı *</label>
                        <input
                          type="text"
                          value={newTestimonial.clientName}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, clientName: e.target.value })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="Ayşe Demir"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Pozisyon</label>
                        <input
                          type="text"
                          value={newTestimonial.clientPosition}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, clientPosition: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="CEO"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Şirket *</label>
                        <input
                          type="text"
                          value={newTestimonial.clientCompany}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, clientCompany: e.target.value })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="ABC E-ticaret"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Puan *</label>
                        <select
                          value={newTestimonial.rating}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, rating: parseInt(e.target.value) })}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        >
                          <option value={5}>⭐⭐⭐⭐⭐ (5)</option>
                          <option value={4}>⭐⭐⭐⭐ (4)</option>
                          <option value={3}>⭐⭐⭐ (3)</option>
                          <option value={2}>⭐⭐ (2)</option>
                          <option value={1}>⭐ (1)</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Referans Metni *</label>
                      <textarea
                        value={newTestimonial.content}
                        onChange={(e) => setNewTestimonial({ ...newTestimonial, content: e.target.value })}
                        required
                        rows="4"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Skywalker.tc ile çalışmaktan çok memnunuz..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Müşteri Fotoğrafı</label>
                      <FileUploader 
                        accept="image/*"
                        category="testimonial_photos"
                        onFileUploaded={(file) => setNewTestimonial({ ...newTestimonial, imageUrl: `${API_BASE}${file.url}` })}
                        className="mb-2"
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Proje Türü</label>
                        <input
                          type="text"
                          value={newTestimonial.projectType}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, projectType: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="E-ticaret Optimizasyon"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Sıra</label>
                        <input
                          type="number"
                          value={newTestimonial.order}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, order: parseInt(e.target.value) || 0 })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="featured"
                          checked={newTestimonial.isFeatured}
                          onChange={(e) => setNewTestimonial({ ...newTestimonial, isFeatured: e.target.checked })}
                          className="mr-2"
                        />
                        <label htmlFor="featured" className="text-sm font-medium text-gray-700">Öne Çıkan</label>
                      </div>
                    </div>
                    
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Ekleniyor...' : 'Referans Ekle'}
                    </button>
                  </form>
                </div>

                {/* Testimonials List */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut Referanslar</h2>
                  
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {testimonials.map((testimonial) => (
                      <div key={testimonial.id} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center mb-2">
                              <h3 className="font-semibold text-gray-900">{testimonial.clientName}</h3>
                              <div className="ml-2">
                                {'⭐'.repeat(testimonial.rating)}
                              </div>
                              {testimonial.isFeatured && (
                                <span className="ml-2 bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                                  Öne Çıkan
                                </span>
                              )}
                            </div>
                            <p className="text-sm text-gray-600 mb-2">{testimonial.clientCompany}</p>
                            <p className="text-sm text-gray-800">{testimonial.content.substring(0, 100)}...</p>
                            <p className="text-xs text-gray-500 mt-2">Sıra: {testimonial.order}</p>
                          </div>
                          <button
                            onClick={() => deleteTestimonial(testimonial.id)}
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
            </div>
          )}

          {/* FAQ Management */}
          {activeSection === 'faqs' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">S.S.S. Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* FAQ Creation Form */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni S.S.S. Ekle</h2>
                  
                  <form onSubmit={createFaq} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Kategori *</label>
                      <select
                        value={newFaq.category}
                        onChange={(e) => setNewFaq({ ...newFaq, category: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="">Seçiniz</option>
                        <option value="Genel">Genel</option>
                        <option value="Hizmetler">Hizmetler</option>
                        <option value="Fiyatlandırma">Fiyatlandırma</option>
                        <option value="Teknik">Teknik</option>
                        <option value="İş Ortaklığı">İş Ortaklığı</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Soru *</label>
                      <input
                        type="text"
                        value={newFaq.question}
                        onChange={(e) => setNewFaq({ ...newFaq, question: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Hizmetleriniz nelerdir?"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Cevap *</label>
                      <textarea
                        value={newFaq.answer}
                        onChange={(e) => setNewFaq({ ...newFaq, answer: e.target.value })}
                        required
                        rows="4"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="E-ticaret optimizasyon, pazarlama ve satış artırma hizmetleri sunuyoruz..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Sıra</label>
                      <input
                        type="number"
                        value={newFaq.order}
                        onChange={(e) => setNewFaq({ ...newFaq, order: parseInt(e.target.value) || 0 })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Ekleniyor...' : 'S.S.S. Ekle'}
                    </button>
                  </form>
                </div>

                {/* FAQ List */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut S.S.S.</h2>
                  
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {faqs.map((faq) => (
                      <div key={faq.id} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center mb-2">
                              <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full mr-2">
                                {faq.category}
                              </span>
                              <span className="text-xs text-gray-500">Sıra: {faq.order}</span>
                            </div>
                            <h3 className="font-semibold text-gray-900 mb-2">{faq.question}</h3>
                            <p className="text-sm text-gray-800">{faq.answer.substring(0, 150)}...</p>
                          </div>
                          <button
                            onClick={() => deleteFaq(faq.id)}
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
            </div>
          )}

          {/* Notification System Management */}
          {activeSection === 'notifications' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Bildirim Sistemi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Notification Creation Form */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Bildirim Oluştur</h2>
                  
                  <form onSubmit={createNotification} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Bildirim Türü *</label>
                      <select
                        value={newNotification.type}
                        onChange={(e) => setNewNotification({ ...newNotification, type: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="announcement">📢 Duyuru</option>
                        <option value="news">📰 Haber</option>
                        <option value="update">🔄 Güncelleme</option>
                        <option value="maintenance">🔧 Bakım</option>
                        <option value="promotion">🎉 Promosyon</option>
                        <option value="alert">⚠️ Uyarı</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Başlık *</label>
                      <input
                        type="text"
                        value={newNotification.title}
                        onChange={(e) => setNewNotification({ ...newNotification, title: e.target.value })}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Bildirim başlığı..."
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">İçerik *</label>
                      <textarea
                        value={newNotification.content}
                        onChange={(e) => setNewNotification({ ...newNotification, content: e.target.value })}
                        required
                        rows="4"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder="Bildirim detayları..."
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Başlama Tarihi</label>
                        <input
                          type="datetime-local"
                          value={newNotification.startDate}
                          onChange={(e) => setNewNotification({ ...newNotification, startDate: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Bitiş Tarihi</label>
                        <input
                          type="datetime-local"
                          value={newNotification.endDate}
                          onChange={(e) => setNewNotification({ ...newNotification, endDate: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>

                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="isGlobal"
                        checked={newNotification.isGlobal}
                        onChange={(e) => setNewNotification({ ...newNotification, isGlobal: e.target.checked })}
                        className="mr-2"
                      />
                      <label htmlFor="isGlobal" className="text-sm font-medium text-gray-700">
                        Tüm Kullanıcılara Gönder (Global)
                      </label>
                    </div>

                    <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
                      <p className="text-blue-700 text-sm">
                        <strong>Bilgi:</strong> Bildirimler belirlenen tarih aralığında aktif kullanıcılara görünecektir. 
                        Tarih belirtmezseniz hemen aktif olur.
                      </p>
                    </div>
                    
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Oluşturuluyor...' : 'Bildirim Oluştur'}
                    </button>
                  </form>
                </div>

                {/* Notifications List */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Mevcut Bildirimler</h2>
                  
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {notifications.length > 0 ? notifications.map((notification) => {
                      const isActive = notification.isActive && 
                        (!notification.startDate || new Date(notification.startDate) <= new Date()) &&
                        (!notification.endDate || new Date(notification.endDate) >= new Date());
                      
                      const getTypeIcon = (type) => {
                        const icons = {
                          'announcement': '📢',
                          'news': '📰',
                          'update': '🔄',
                          'maintenance': '🔧',
                          'promotion': '🎉',
                          'alert': '⚠️'
                        };
                        return icons[type] || '📌';
                      };

                      return (
                        <div key={notification.id} className={`p-4 rounded-lg border ${
                          isActive ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                        }`}>
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center mb-2">
                                <span className="text-lg mr-2">{getTypeIcon(notification.type)}</span>
                                <h3 className="font-semibold text-gray-900">{notification.title}</h3>
                                <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                                  isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                                }`}>
                                  {isActive ? 'Aktif' : 'Pasif'}
                                </span>
                                {notification.isGlobal && (
                                  <span className="ml-2 bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                                    Global
                                  </span>
                                )}
                              </div>
                              <p className="text-sm text-gray-600 mb-2">{notification.content.substring(0, 100)}...</p>
                              <div className="text-xs text-gray-500">
                                <div>Oluşturulma: {new Date(notification.createdAt).toLocaleDateString('tr-TR')}</div>
                                {notification.startDate && (
                                  <div>Başlama: {new Date(notification.startDate).toLocaleDateString('tr-TR')}</div>
                                )}
                                {notification.endDate && (
                                  <div>Bitiş: {new Date(notification.endDate).toLocaleDateString('tr-TR')}</div>
                                )}
                              </div>
                            </div>
                            <button
                              onClick={() => deleteNotification(notification.id)}
                              className="ml-4 text-red-600 hover:text-red-800 transition-colors"
                            >
                              🗑️
                            </button>
                          </div>
                        </div>
                      );
                    }) : (
                      <div className="text-center text-gray-500 py-8">
                        <div className="text-4xl mb-4">🔔</div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Henüz bildirim yok</h3>
                        <p>İlk bildirimi oluşturmak için yukarıdaki formu kullanın.</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Usage Statistics */}
              <div className="mt-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-6 text-white">
                <h3 className="text-xl font-bold mb-4">Bildirim İstatistikleri</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold">{notifications.length}</div>
                    <p className="text-purple-100">Toplam Bildirim</p>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">
                      {notifications.filter(n => n.isActive && (!n.endDate || new Date(n.endDate) >= new Date())).length}
                    </div>
                    <p className="text-purple-100">Aktif Bildirim</p>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">
                      {notifications.filter(n => n.isGlobal).length}
                    </div>
                    <p className="text-purple-100">Global Bildirim</p>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">
                      {new Set(notifications.map(n => n.type)).size}
                    </div>
                    <p className="text-purple-100">Farklı Tür</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Newsletter Management */}
          {activeSection === 'newsletter' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Newsletter Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Aktif Aboneler</h3>
                  <div className="text-3xl font-bold">{newsletterSubscribers.filter(s => s.isActive).length}</div>
                </div>
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Toplam Abone</h3>
                  <div className="text-3xl font-bold">{newsletterSubscribers.length}</div>
                </div>
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Bu Ay Yeni</h3>
                  <div className="text-3xl font-bold">
                    {newsletterSubscribers.filter(s => {
                      const subDate = new Date(s.subscribedAt);
                      const now = new Date();
                      return subDate.getMonth() === now.getMonth() && subDate.getFullYear() === now.getFullYear();
                    }).length}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Newsletter Aboneleri</h2>
                
                <div className="overflow-x-auto">
                  <table className="w-full table-auto">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">E-posta</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Ad</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Abone Tarihi</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Kaynak</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Durum</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {newsletterSubscribers.map((subscriber) => (
                        <tr key={subscriber.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm text-gray-900">{subscriber.email}</td>
                          <td className="px-4 py-2 text-sm text-gray-900">{subscriber.name || '-'}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">
                            {new Date(subscriber.subscribedAt).toLocaleDateString('tr-TR')}
                          </td>
                          <td className="px-4 py-2 text-sm text-gray-500">{subscriber.source}</td>
                          <td className="px-4 py-2">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              subscriber.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {subscriber.isActive ? 'Aktif' : 'Pasif'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Leads Management */}
          {activeSection === 'leads' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Potansiyel Müşteriler</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
                <div className="bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Toplam Lead</h3>
                  <div className="text-3xl font-bold">{leads.length}</div>
                </div>
                <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">İşlenmemiş</h3>
                  <div className="text-3xl font-bold">{leads.filter(l => !l.isProcessed).length}</div>
                </div>
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">İşlenmiş</h3>
                  <div className="text-3xl font-bold">{leads.filter(l => l.isProcessed).length}</div>
                </div>
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Bu Hafta</h3>
                  <div className="text-3xl font-bold">
                    {leads.filter(l => {
                      const leadDate = new Date(l.createdAt);
                      const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                      return leadDate >= weekAgo;
                    }).length}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Potansiyel Müşteri Listesi</h2>
                
                <div className="overflow-x-auto">
                  <table className="w-full table-auto">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Ad</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">E-posta</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Telefon</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Şirket</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Kaynak</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Tarih</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Durum</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {leads.map((lead) => (
                        <tr key={lead.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm text-gray-900">{lead.name || '-'}</td>
                          <td className="px-4 py-2 text-sm text-gray-900">{lead.email}</td>
                          <td className="px-4 py-2 text-sm text-gray-900">{lead.phone || '-'}</td>
                          <td className="px-4 py-2 text-sm text-gray-900">{lead.company || '-'}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">{lead.source}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">
                            {new Date(lead.createdAt).toLocaleDateString('tr-TR')}
                          </td>
                          <td className="px-4 py-2">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              lead.isProcessed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {lead.isProcessed ? 'İşlenmiş' : 'Beklemede'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Services Management (Galaktik Hizmetler) */}
          {activeSection === 'services' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Galaktik Hizmetler Yönetimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="lg:col-span-2">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h2 className="text-lg font-semibold text-gray-900">Mevcut Hizmetler</h2>
                      <button 
                        onClick={loadServices}
                        className="mt-2 text-sm text-purple-600 hover:text-purple-700"
                      >
                        🔄 Yenile
                      </button>
                    </div>
                    <div className="p-6">
                      <div className="space-y-4">
                        {services.map((service) => (
                          <div key={service.id} className="border border-gray-200 rounded-lg p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="flex items-center mb-2">
                                  <span className="text-2xl mr-2">{service.icon}</span>
                                  <h3 className="text-lg font-semibold text-gray-900">{service.title}</h3>
                                  <span className={`ml-2 px-2 py-1 text-xs font-semibold rounded-full ${
                                    service.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                  }`}>
                                    {service.isActive ? 'Aktif' : 'Pasif'}
                                  </span>
                                  {service.isFeatured && (
                                    <span className="ml-2 px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                      Öne Çıkan
                                    </span>
                                  )}
                                </div>
                                <p className="text-sm text-gray-600 mb-2">{service.shortDescription}</p>
                                <div className="flex items-center space-x-4 text-xs text-gray-500">
                                  <span>📁 {service.serviceType}</span>
                                  <span>💰 {service.price ? `${service.price} ${service.currency}` : 'İletişime Geç'}</span>
                                  <span>⏱️ {service.duration}</span>
                                </div>
                              </div>
                              <div className="flex space-x-2 ml-4">
                                <button
                                  onClick={() => toggleServiceActive(service.id)}
                                  className={`px-3 py-1 text-xs rounded ${
                                    service.isActive 
                                      ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                                      : 'bg-green-100 text-green-700 hover:bg-green-200'
                                  }`}
                                >
                                  {service.isActive ? 'Pasifleştir' : 'Aktifleştir'}
                                </button>
                                <button
                                  onClick={() => toggleServiceFeatured(service.id)}
                                  className={`px-3 py-1 text-xs rounded ${
                                    service.isFeatured 
                                      ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' 
                                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                  }`}
                                >
                                  {service.isFeatured ? 'Öne Çıkarmayı Kaldır' : 'Öne Çıkar'}
                                </button>
                                <button
                                  onClick={() => deleteService(service.id)}
                                  className="px-3 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                                >
                                  Sil
                                </button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Add New Service Form */}
                <div>
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Yeni Hizmet Ekle</h2>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Hizmet Adı *
                        </label>
                        <input
                          type="text"
                          value={newService.title}
                          onChange={(e) => setNewService({...newService, title: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="E-ticaret Danışmanlığı"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Kısa Açıklama *
                        </label>
                        <input
                          type="text"
                          value={newService.shortDescription}
                          onChange={(e) => setNewService({...newService, shortDescription: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="E-ticaret sitenizi optimize edin"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Hizmet Türü
                        </label>
                        <select
                          value={newService.serviceType}
                          onChange={(e) => setNewService({...newService, serviceType: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="e-ticaret">E-ticaret</option>
                          <option value="sosyal_medya">Sosyal Medya</option>
                          <option value="seo">SEO</option>
                          <option value="icerik_pazarlama">İçerik Pazarlama</option>
                          <option value="influencer_pazarlama">Influencer Pazarlama</option>
                          <option value="marka_yonetimi">Marka Yönetimi</option>
                          <option value="strateji_danismanligi">Strateji Danışmanlığı</option>
                          <option value="diger">Diğer</option>
                        </select>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Fiyat (TL)
                          </label>
                          <input
                            type="number"
                            value={newService.price || ''}
                            onChange={(e) => setNewService({...newService, price: e.target.value ? parseFloat(e.target.value) : null})}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="5000"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Süre *
                          </label>
                          <input
                            type="text"
                            value={newService.duration}
                            onChange={(e) => setNewService({...newService, duration: e.target.value})}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="2-4 hafta"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          İkon
                        </label>
                        <input
                          type="text"
                          value={newService.icon}
                          onChange={(e) => setNewService({...newService, icon: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="🛸"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Detaylı Açıklama *
                        </label>
                        <textarea
                          value={newService.description}
                          onChange={(e) => setNewService({...newService, description: e.target.value})}
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="Bu hizmette neler yapıyoruz..."
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Süreç Açıklaması *
                        </label>
                        <textarea
                          value={newService.timeline}
                          onChange={(e) => setNewService({...newService, timeline: e.target.value})}
                          rows={2}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="1. hafta analiz, 2. hafta uygulama..."
                        />
                      </div>

                      <div className="flex items-center space-x-4">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={newService.isFeatured}
                            onChange={(e) => setNewService({...newService, isFeatured: e.target.checked})}
                            className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Öne Çıkan</span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={newService.showPrice}
                            onChange={(e) => setNewService({...newService, showPrice: e.target.checked})}
                            className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Fiyat Göster</span>
                        </label>
                      </div>

                      <button
                        onClick={createService}
                        disabled={loading}
                        className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
                      >
                        {loading ? 'Ekleniyor...' : '🛸 Hizmet Ekle'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Payment Management */}
          {activeSection === 'payments' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Ödeme Yönetimi & Faturalama</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Toplam İşlem</h3>
                  <div className="text-3xl font-bold">{paymentStats.total_transactions || 0}</div>
                </div>
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Başarılı Ödeme</h3>
                  <div className="text-3xl font-bold">{paymentStats.successful_amount || 0} ₺</div>
                </div>
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Başarı Oranı</h3>
                  <div className="text-3xl font-bold">{paymentStats.success_rate || 0}%</div>
                </div>
                <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Bu Ay</h3>
                  <div className="text-3xl font-bold">
                    {paymentStats.stats_by_status?.success?.totalAmount || 0} ₺
                  </div>
                </div>
              </div>

              {/* Müşteriye Ödeme Linki Gönderme Paneli */}
              <div className="bg-white rounded-lg shadow mb-6">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-900">💳 Müşteriye Ödeme Linki Oluştur</h2>
                  <p className="text-sm text-gray-600">Müşterinize Iyzico üzerinden güvenli ödeme linki gönderin</p>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Müşteri Adı Soyadı *
                        </label>
                        <input
                          type="text"
                          placeholder="Ahmet Yılmaz"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Email Adresi *
                        </label>
                        <input
                          type="email"
                          placeholder="ahmet@example.com"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Telefon Numarası *
                        </label>
                        <input
                          type="tel"
                          placeholder="+90 555 123 45 67"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          TC Kimlik No *
                        </label>
                        <input
                          type="text"
                          placeholder="12345678901"
                          maxLength="11"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Hizmet Türü *
                        </label>
                        <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500">
                          <option value="">Hizmet Seçin</option>
                          <option value="e-ticaret">🛒 E-ticaret Danışmanlığı</option>
                          <option value="sosyal-medya">📱 Sosyal Medya Yönetimi</option>
                          <option value="influencer">⭐ Influencer Pazarlama</option>
                          <option value="seo">🔍 SEO & Google Ads</option>
                          <option value="marka">🎯 Marka Kimliği</option>
                          <option value="ozel">✨ Özel Proje</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tutar (TL) *
                        </label>
                        <input
                          type="number"
                          placeholder="5000"
                          min="1"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Açıklama
                        </label>
                        <textarea
                          placeholder="E-ticaret mağaza kurulumu - 1. Taksit"
                          rows="3"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Son Ödeme Tarihi
                        </label>
                        <input
                          type="date"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="flex items-center space-x-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">SMS ile de gönder</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">Hatırlatma SMS'i kur</span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="mt-6">
                    <button className="w-full lg:w-auto px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold transition-colors">
                      🔗 Ödeme Linki Oluştur ve Gönder
                    </button>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                  <h2 className="text-lg font-semibold text-gray-900">Ödeme İşlemleri</h2>
                  <div className="flex space-x-2">
                    <button 
                      onClick={loadPaymentTransactions}
                      className="px-4 py-2 text-sm bg-purple-600 text-white rounded hover:bg-purple-700"
                    >
                      🔄 Yenile
                    </button>
                    <button 
                      onClick={loadPaymentStats}
                      className="px-4 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                    >
                      📊 İstatistikler
                    </button>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">İşlem ID</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Müşteri</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tutar</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Durum</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tarih</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hizmet</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {paymentTransactions.map((transaction) => (
                        <tr key={transaction.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {transaction.id.slice(0, 8)}...
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm text-gray-900">{transaction.buyerInfo?.name}</div>
                            <div className="text-xs text-gray-500">{transaction.buyerInfo?.email}</div>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {transaction.amount} {transaction.currency}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              transaction.status === 'success' ? 'bg-green-100 text-green-800' :
                              transaction.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {transaction.status === 'success' ? 'Başarılı' :
                               transaction.status === 'pending' ? 'Beklemede' : 'Başarısız'}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500">
                            {new Date(transaction.createdAt).toLocaleDateString('tr-TR')}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500">
                            {transaction.serviceType || 'Genel'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* SMS Management */}
          {activeSection === 'sms' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">SMS Yönetimi & Müşteri İletişimi</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Toplam SMS</h3>
                  <div className="text-3xl font-bold">{smsStats.total_sms || 0}</div>
                </div>
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Başarılı</h3>
                  <div className="text-3xl font-bold">{smsStats.successful_sms || 0}</div>
                </div>
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Başarı Oranı</h3>
                  <div className="text-3xl font-bold">{smsStats.success_rate || 0}%</div>
                </div>
                <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Şablonlar</h3>
                  <div className="text-3xl font-bold">{smsTemplates.length}</div>
                </div>
              </div>

              {/* Müşteri SMS Gönderme Paneli */}
              <div className="bg-white rounded-lg shadow mb-6">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-900">🎯 Müşteriye SMS Gönder</h2>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Müşteri Telefonu *
                      </label>
                      <input
                        type="tel"
                        placeholder="+90 555 123 45 67"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        SMS Türü *
                      </label>
                      <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">SMS Türü Seçin</option>
                        <option value="customer_request_response">📋 Talep Yanıtı</option>
                        <option value="payment_reminder">💳 Ödeme Hatırlatması</option>
                        <option value="meeting_reminder">📅 Toplantı Hatırlatması</option>
                        <option value="project_update">🚀 Proje Güncellemesi</option>
                        <option value="general_info">ℹ️ Genel Bilgilendirme</option>
                      </select>
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Müşteri Adı (Kayıt için)
                      </label>
                      <input
                        type="text"
                        placeholder="Ahmet Yılmaz"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        SMS Mesajı *
                      </label>
                      <textarea
                        rows="3"
                        placeholder="Merhaba, talebiniz ile ilgili size dönüş yapmak istiyoruz..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <button className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">
                        📱 SMS Gönder ve Kaydet
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* SMS Transaction History with Better Details */}
                <div className="bg-white rounded-lg shadow">
                  <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                    <h2 className="text-lg font-semibold text-gray-900">SMS Geçmişi</h2>
                    <div className="flex space-x-2">
                      <button 
                        onClick={loadSmsTransactions}
                        className="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700"
                      >
                        🔄
                      </button>
                      <button 
                        onClick={sendTestSms}
                        className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                      >
                        📱 Test SMS
                      </button>
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="space-y-4">
                      {smsTransactions.slice(0, 10).map((sms) => (
                        <div key={sms.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="text-sm font-semibold text-gray-900">{sms.phoneNumber}</span>
                                <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                                  sms.triggerType === 'customer_request_response' ? 'bg-blue-100 text-blue-800' :
                                  sms.triggerType === 'payment_reminder' ? 'bg-orange-100 text-orange-800' :
                                  sms.triggerType === 'meeting_reminder' ? 'bg-purple-100 text-purple-800' :
                                  'bg-gray-100 text-gray-800'
                                }`}>
                                  {sms.triggerType === 'customer_request_response' ? '📋 Talep Yanıtı' :
                                   sms.triggerType === 'payment_reminder' ? '💳 Ödeme Hatırlatması' :
                                   sms.triggerType === 'meeting_reminder' ? '📅 Toplantı' :
                                   sms.triggerType}
                                </span>
                              </div>
                              <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                                "{sms.message}"
                              </div>
                              <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                                <span>📅 {new Date(sms.createdAt).toLocaleString('tr-TR')}</span>
                                {sms.relatedEntityId && (
                                  <span>🔗 ID: {sms.relatedEntityId.slice(0, 8)}...</span>
                                )}
                              </div>
                            </div>
                            <span className={`px-3 py-1 text-xs rounded-full font-medium ${
                              sms.status === 'sent' ? 'bg-green-100 text-green-800' :
                              sms.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {sms.status === 'sent' ? '✅ Gönderildi' :
                               sms.status === 'pending' ? '⏳ Beklemede' : '❌ Başarısız'}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* SMS Templates */}
                <div className="bg-white rounded-lg shadow">
                  <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                    <h2 className="text-lg font-semibold text-gray-900">SMS Şablonları</h2>
                    <button 
                      onClick={loadSmsTemplates}
                      className="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700"
                    >
                      🔄
                    </button>
                  </div>
                  <div className="p-6">
                    {/* Add New Template Form */}
                    <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                      <h3 className="text-sm font-semibold text-gray-900 mb-3">Yeni Şablon</h3>
                      <div className="space-y-3">
                        <input
                          type="text"
                          placeholder="Şablon Adı"
                          value={newSmsTemplate.name}
                          onChange={(e) => setNewSmsTemplate({...newSmsTemplate, name: e.target.value})}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <input
                          type="text"
                          placeholder="Tetikleyici Türü (örn: customer_response)"
                          value={newSmsTemplate.triggerType}
                          onChange={(e) => setNewSmsTemplate({...newSmsTemplate, triggerType: e.target.value})}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <textarea
                          placeholder="Mesaj şablonu (değişkenler için {variable_name} kullanın)"
                          value={newSmsTemplate.template}
                          onChange={(e) => setNewSmsTemplate({...newSmsTemplate, template: e.target.value})}
                          rows={3}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <button
                          onClick={createSmsTemplate}
                          className="w-full px-4 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                        >
                          📱 Şablon Ekle
                        </button>
                      </div>
                    </div>

                    {/* Existing Templates */}
                    <div className="space-y-3">
                      {smsTemplates.map((template) => (
                        <div key={template.id} className="border border-gray-200 rounded p-3">
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <div className="text-sm font-medium text-gray-900">{template.name}</div>
                              <div className="text-xs text-gray-600">{template.triggerType}</div>
                              <div className="text-xs text-gray-500 mt-1 truncate">{template.template}</div>
                            </div>
                            <span className={`px-2 py-1 text-xs rounded ${
                              template.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {template.isActive ? 'Aktif' : 'Pasif'}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Load Stats Button */}
              <div className="mt-6 flex justify-center">
                <button 
                  onClick={loadSmsStats}
                  className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                >
                  📊 SMS İstatistiklerini Yükle
                </button>
              </div>
            </div>
          )}

          {/* Referanslar (Company Logos) Management */}
          {activeSection === 'testimonials' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">🏢 Referans Firmaları</h1>
              
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Yeni Firma Logosu Ekle</h2>
                <p className="text-gray-600 mb-4">İş birliği yaptığınız firma logolarını yükleyerek referans galerinizi oluşturun.</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Firma Adı *
                    </label>
                    <input
                      type="text"
                      placeholder="ABC Şirketi"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Website (Opsiyonel)
                    </label>
                    <input
                      type="url"
                      placeholder="https://abcsirketi.com"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Logo Yükle *
                    </label>
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-400 transition-colors">
                      <input
                        type="file"
                        accept="image/*"
                        className="hidden"
                        id="logoUpload"
                      />
                      <label htmlFor="logoUpload" className="cursor-pointer">
                        <div className="text-6xl mb-2">🏢</div>
                        <div className="text-lg font-semibold text-gray-700 mb-2">Logo yüklemek için tıklayın</div>
                        <p className="text-sm text-gray-500">PNG, JPG, SVG formatlarını destekler (Maks. 2MB)</p>
                      </label>
                    </div>
                  </div>
                  <div className="md:col-span-2">
                    <button className="w-full px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold">
                      🏢 Firma Ekle
                    </button>
                  </div>
                </div>
              </div>

              {/* Current Logos */}
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-900">Mevcut Referans Firmaları</h2>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {/* Sample logos */}
                    <div className="border border-gray-200 rounded-lg p-4 text-center hover:shadow-md transition-shadow">
                      <div className="text-4xl mb-2">🏢</div>
                      <div className="text-sm font-medium text-gray-700">Trendyol</div>
                      <div className="text-xs text-gray-500 mt-1">trendyol.com</div>
                      <div className="flex justify-center space-x-2 mt-2">
                        <button className="text-xs text-blue-600 hover:text-blue-800">✏️</button>
                        <button className="text-xs text-red-600 hover:text-red-800">🗑️</button>
                      </div>
                    </div>
                    <div className="border border-gray-200 rounded-lg p-4 text-center hover:shadow-md transition-shadow">
                      <div className="text-4xl mb-2">🛒</div>
                      <div className="text-sm font-medium text-gray-700">Hepsiburada</div>
                      <div className="text-xs text-gray-500 mt-1">hepsiburada.com</div>
                      <div className="flex justify-center space-x-2 mt-2">
                        <button className="text-xs text-blue-600 hover:text-blue-800">✏️</button>
                        <button className="text-xs text-red-600 hover:text-red-800">🗑️</button>
                      </div>
                    </div>
                    <div className="border border-gray-200 rounded-lg p-4 text-center hover:shadow-md transition-shadow">
                      <div className="text-4xl mb-2">🏪</div>
                      <div className="text-sm font-medium text-gray-700">N11</div>
                      <div className="text-xs text-gray-500 mt-1">n11.com</div>
                      <div className="flex justify-center space-x-2 mt-2">
                        <button className="text-xs text-blue-600 hover:text-blue-800">✏️</button>
                        <button className="text-xs text-red-600 hover:text-red-800">🗑️</button>
                      </div>
                    </div>
                    <div className="border border-gray-200 rounded-lg p-4 text-center hover:shadow-md transition-shadow">
                      <div className="text-4xl mb-2">📱</div>
                      <div className="text-sm font-medium text-gray-700">GittiGidiyor</div>
                      <div className="text-xs text-gray-500 mt-1">gittigidiyor.com</div>
                      <div className="flex justify-center space-x-2 mt-2">
                        <button className="text-xs text-blue-600 hover:text-blue-800">✏️</button>
                        <button className="text-xs text-red-600 hover:text-red-800">🗑️</button>
                      </div>
                    </div>
                    {/* Add new placeholder */}
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-purple-400 transition-colors cursor-pointer">
                      <div className="text-4xl mb-2 text-gray-400">➕</div>
                      <div className="text-sm text-gray-500">Yeni Ekle</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Analytics Dashboard */}
          {activeSection === 'analytics' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Analytics Dashboard</h1>
              
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Sayfa Görüntüleme</h3>
                  <div className="text-3xl font-bold">{analytics.total_page_views || 0}</div>
                  <p className="text-blue-100 text-sm">Son 30 gün</p>
                </div>
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Newsletter Aboneleri</h3>
                  <div className="text-3xl font-bold">{analytics.newsletter_subscribers || 0}</div>
                  <p className="text-green-100 text-sm">Aktif aboneler</p>
                </div>
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Yeni Potansiyel</h3>
                  <div className="text-3xl font-bold">{analytics.new_leads || 0}</div>
                  <p className="text-purple-100 text-sm">Son 30 gün</p>
                </div>
                <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">Dönüşüm Oranı</h3>
                  <div className="text-3xl font-bold">
                    {analytics.total_page_views && analytics.new_leads 
                      ? ((analytics.new_leads / analytics.total_page_views) * 100).toFixed(1)
                      : 0}%
                  </div>
                  <p className="text-orange-100 text-sm">Ziyaret → Lead</p>
                </div>
              </div>

              {analytics.top_pages && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">En Popüler Sayfalar</h2>
                  
                  <div className="space-y-3">
                    {analytics.top_pages.map((page, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center">
                          <span className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">
                            {index + 1}
                          </span>
                          <span className="font-medium text-gray-900">{page.path}</span>
                        </div>
                        <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                          {page.views} görüntüleme
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;