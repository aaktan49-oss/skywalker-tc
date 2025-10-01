import React, { useState } from 'react';

const PortalAuth = ({ onLoginSuccess }) => {
  const [activeTab, setActiveTab] = useState('login');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    company: '',
    phone: '',
    role: 'influencer',
    instagram: '',
    followersCount: '',
    category: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/api/portal/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('portal_token', data.access_token);
        localStorage.setItem('portal_user', JSON.stringify(data.user));
        onLoginSuccess(data.user);
      } else {
        setError(data.detail || 'Giriş başarısız');
      }
    } catch (error) {
      setError('Bağlantı hatası. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const registerData = {
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
        role: formData.role
      };

      if (formData.role === 'partner') {
        registerData.company = formData.company;
        registerData.phone = formData.phone;
      } else if (formData.role === 'influencer') {
        registerData.instagram = formData.instagram;
        registerData.followersCount = formData.followersCount;
        registerData.category = formData.category;
      }

      const response = await fetch(`${API_BASE}/api/portal/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registerData)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        alert(data.message);
        setActiveTab('login');
        setFormData({
          email: formData.email,
          password: '',
          firstName: '',
          lastName: '',
          company: '',
          phone: '',
          role: 'influencer',
          instagram: '',
          followersCount: '',
          category: ''
        });
      } else {
        setError(data.detail || data.message || 'Kayıt başarısız');
      }
    } catch (error) {
      setError('Bağlantı hatası. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-md">
        {/* Tab Header */}
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('login')}
            className={`flex-1 py-4 text-center font-medium ${
              activeTab === 'login'
                ? 'text-purple-600 border-b-2 border-purple-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Giriş Yap
          </button>
          <button
            onClick={() => setActiveTab('register')}
            className={`flex-1 py-4 text-center font-medium ${
              activeTab === 'register'
                ? 'text-purple-600 border-b-2 border-purple-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Kayıt Ol
          </button>
        </div>

        {/* Form Content */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          {activeTab === 'login' ? (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-posta
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Şifre
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="space-y-4">
              {/* Role Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hesap Türü
                </label>
                <select
                  name="role"
                  value={formData.role}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="influencer">Influencer</option>
                  <option value="partner">Firma</option>
                </select>
              </div>

              {/* Common Fields */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Ad
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Soyad
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-posta
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Şifre
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  minLength="6"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              {/* Role-specific fields */}
              {formData.role === 'partner' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Şirket Adı
                    </label>
                    <input
                      type="text"
                      name="company"
                      value={formData.company}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Telefon
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </>
              )}

              {formData.role === 'influencer' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Instagram Hesabı
                    </label>
                    <input
                      type="text"
                      name="instagram"
                      value={formData.instagram}
                      onChange={handleInputChange}
                      placeholder="@kullaniciadi"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Takipçi Sayısı
                    </label>
                    <select
                      name="followersCount"
                      value={formData.followersCount}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="">Seçiniz</option>
                      <option value="1K-10K">1K - 10K</option>
                      <option value="10K-50K">10K - 50K</option>
                      <option value="50K-100K">50K - 100K</option>
                      <option value="100K-500K">100K - 500K</option>
                      <option value="500K+">500K+</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      İçerik Kategoriniz
                    </label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="">Seçiniz</option>
                      <option value="moda">Moda</option>
                      <option value="kozmetik">Kozmetik</option>
                      <option value="teknoloji">Teknoloji</option>
                      <option value="spor">Spor</option>
                      <option value="yasam">Yaşam Tarzı</option>
                      <option value="yiyecek">Yiyecek & İçecek</option>
                      <option value="diger">Diğer</option>
                    </select>
                  </div>
                </>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Kayıt yapılıyor...' : 'Kayıt Ol'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortalAuth;