import React, { useState, useEffect } from 'react';
import AdminLogin from './admin/AdminLogin';
import AdminDashboard from './portal/AdminDashboard';
import { toast } from 'sonner';

const AdminPanel = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [adminUser, setAdminUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if already logged in
    const savedToken = localStorage.getItem('adminToken');
    const savedUser = localStorage.getItem('adminUser');

    if (savedToken && savedUser) {
      try {
        const user = JSON.parse(savedUser);
        setToken(savedToken);
        setAdminUser(user);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Saved user data parse error:', error);
        // Clear corrupted data
        localStorage.removeItem('adminToken');
        localStorage.removeItem('adminUser');
      }
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (user, authToken) => {
    setAdminUser(user);
    setToken(authToken);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminUser');
    setAdminUser(null);
    setToken(null);
    setIsAuthenticated(false);
    toast.success('Başarıyla çıkış yaptınız');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-400"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AdminLogin onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Admin Header */}
      <div className="bg-slate-800/50 border-b border-slate-700 px-4 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_trendyol-mentor/artifacts/8o8bzseq_WhatsApp%20Image%202025-07-18%20at%2021.43.19.jpeg" 
              alt="Skywalker Logo" 
              className="h-10 w-10 rounded-full object-cover border border-amber-400"
            />
            <div>
              <h1 className="text-xl font-bold text-white">Skywalker Admin</h1>
              <p className="text-sm text-gray-400">Yönetim Paneli</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-white font-medium">{adminUser?.username}</p>
              <p className="text-gray-400 text-sm">{adminUser?.role}</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors duration-300"
            >
              Çıkış
            </button>
          </div>
        </div>
      </div>

      {/* Admin Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <AdminDashboard token={token} />
      </div>
    </div>
  );
};

export default AdminPanel;