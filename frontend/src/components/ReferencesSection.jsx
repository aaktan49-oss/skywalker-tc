import React, { useState, useEffect } from 'react';

const ReferencesSection = () => {
  const [references, setReferences] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadReferences = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/company-logos`);
      const data = await response.json();
      
      if (Array.isArray(data)) {
        setReferences(data);
        // Extract unique categories
        const uniqueCategories = [...new Set(data.map(ref => ref.category).filter(Boolean))];
        setCategories(['all', ...uniqueCategories]);
      } else if (data && Array.isArray(data.items)) {
        setReferences(data.items);
        const uniqueCategories = [...new Set(data.items.map(ref => ref.category).filter(Boolean))];
        setCategories(['all', ...uniqueCategories]);
      } else {
        setReferences([]);
        setCategories(['all']);
      }
    } catch (error) {
      console.error('Error loading references:', error);
      setReferences([]);
      setCategories(['all']);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReferences();
  }, []);

  // Filter references based on selected category
  const filteredReferences = selectedCategory === 'all' 
    ? references 
    : references.filter(ref => ref.category === selectedCategory);

  if (loading) {
    return (
      <section className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400 mb-4"></div>
            <p className="text-gray-300">Referanslar yükleniyor...</p>
          </div>
        </div>
      </section>
    );
  }

  if (!Array.isArray(references) || references.length === 0) {
    return (
      <section className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h2 className="text-4xl font-bold text-white mb-4">
              <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                Referanslarımız
              </span>
            </h2>
            <p className="text-gray-300">Yakında referanslarımız burada görüntülenecek.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="references" className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              Güvenilen Referanslarımız
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Birlikte çalıştığımız değerli iş ortaklarımız ve başarı hikayelerimiz
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-purple-400 to-blue-400 mx-auto rounded-full"></div>
        </div>

        {/* Category Filter */}
        {categories.length > 1 && (
          <div className="flex flex-wrap justify-center mb-12 gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-3 rounded-full text-sm font-semibold transition-all duration-300 transform hover:scale-105 ${
                  selectedCategory === category
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/25'
                    : 'bg-slate-700 text-gray-300 hover:bg-slate-600 hover:text-white'
                }`}
              >
                {category === 'all' ? 'Tüm Referanslar' : category}
              </button>
            ))}
          </div>
        )}

        {/* References Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 mb-12">
          {Array.isArray(filteredReferences) && filteredReferences.map((reference, index) => (
            <div
              key={reference.id || index}
              className="group relative bg-white rounded-2xl p-6 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 cursor-pointer border border-gray-100"
              onClick={() => {
                if (reference.website) {
                  window.open(reference.website, '_blank', 'noopener,noreferrer');
                }
              }}
            >
              {/* Logo Container */}
              <div className="aspect-square flex items-center justify-center mb-4">
                {reference.logoUrl ? (
                  <img
                    src={reference.logoUrl}
                    alt={reference.companyName || 'Referans'}
                    className="max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-300"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                {/* Fallback when image fails to load */}
                <div 
                  className="w-full h-full bg-gradient-to-br from-purple-100 to-blue-100 rounded-lg flex items-center justify-center"
                  style={{ display: reference.logoUrl ? 'none' : 'flex' }}
                >
                  <span className="text-purple-600 font-bold text-lg">
                    {reference.companyName ? reference.companyName.charAt(0).toUpperCase() : '?'}
                  </span>
                </div>
              </div>

              {/* Company Info */}
              <div className="text-center">
                <h3 className="font-semibold text-gray-900 text-sm mb-1 group-hover:text-purple-600 transition-colors">
                  {reference.companyName || 'Şirket Adı'}
                </h3>
                {reference.category && (
                  <p className="text-xs text-gray-500">
                    {reference.category}
                  </p>
                )}
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600/90 to-blue-600/90 rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center">
                <div className="text-center text-white">
                  <div className="w-8 h-8 mx-auto mb-2">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </div>
                  <p className="text-sm font-medium">
                    {reference.website ? 'Ziyaret Et' : 'Referansımız'}
                  </p>
                </div>
              </div>

              {/* Success Badge */}
              {reference.isSuccess && (
                <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                  ✓ Başarılı
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Statistics */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl p-8 text-white">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-4xl font-bold">{references.length}+</div>
              <p className="text-purple-100 font-medium">Mutlu Müşteri</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold">%98</div>
              <p className="text-purple-100 font-medium">Müşteri Memnuniyeti</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold">{categories.length - 1}+</div>
              <p className="text-purple-100 font-medium">Farklı Sektör</p>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16">
          <h3 className="text-2xl font-bold text-white mb-4">
            Bir Sonraki Başarı Hikayesi Sizin Olsun!
          </h3>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
            İş ortaklarımızla birlikte elde ettiğimiz başarıları keşfedin ve siz de bu başarı hikayesinin parçası olun.
          </p>
          <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:shadow-2xl hover:shadow-purple-500/25 transform hover:scale-105 transition-all duration-300">
            Hemen Başlayalım
            <svg className="w-5 h-5 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </button>
        </div>
      </div>
    </section>
  );
};

export default ReferencesSection;