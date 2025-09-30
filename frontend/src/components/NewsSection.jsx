import React, { useState, useEffect } from 'react';

const NewsSection = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadNews = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/news?limit=6`);
      const data = await response.json();
      setNews(data || []);
    } catch (error) {
      console.error('Error loading news:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNews();
  }, []);

  const getCategoryLabel = (category) => {
    const labels = {
      'company_news': 'Şirket Haberleri',
      'success_stories': 'Başarı Hikayeleri', 
      'industry_news': 'Sektör Haberleri',
      'announcements': 'Duyurular'
    };
    return labels[category] || category;
  };

  const getCategoryColor = (category) => {
    const colors = {
      'company_news': 'bg-blue-100 text-blue-800',
      'success_stories': 'bg-green-100 text-green-800',
      'industry_news': 'bg-yellow-100 text-yellow-800', 
      'announcements': 'bg-purple-100 text-purple-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mb-4"></div>
            <p className="text-gray-600">Haberler yükleniyor...</p>
          </div>
        </div>
      </section>
    );
  }

  if (!news.length) {
    return null; // Don't show section if no news
  }

  return (
    <section id="news" className="py-20 bg-gradient-to-br from-gray-50 to-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Haberler & Güncellemeler
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            E-ticaret dünyasından en son haberler, başarı hikayeleri ve sektörel gelişmeler
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-purple-600 to-blue-600 mx-auto mt-6 rounded-full"></div>
        </div>

        {/* News Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {news.map((article, index) => (
            <div 
              key={article.id}
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-2"
            >
              {/* Article Image */}
              {article.imageUrl && (
                <div className="relative overflow-hidden h-48">
                  <img 
                    src={article.imageUrl} 
                    alt={article.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  {/* Category Badge */}
                  <div className="absolute top-4 left-4">
                    <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${getCategoryColor(article.category)}`}>
                      {getCategoryLabel(article.category)}
                    </span>
                  </div>
                </div>
              )}

              {/* Article Content */}
              <div className="p-6">
                {!article.imageUrl && (
                  <div className="mb-4">
                    <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${getCategoryColor(article.category)}`}>
                      {getCategoryLabel(article.category)}
                    </span>
                  </div>
                )}
                
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-purple-600 transition-colors line-clamp-2">
                  {article.title}
                </h3>
                
                {article.excerpt && (
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {article.excerpt}
                  </p>
                )}
                
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                    </svg>
                    {new Date(article.publishedAt).toLocaleDateString('tr-TR', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </span>
                </div>

                {/* Read More Button */}
                <button 
                  className="group/btn inline-flex items-center text-purple-600 hover:text-purple-800 font-medium transition-colors"
                  onClick={() => {
                    // Open article in modal or new page
                    window.alert(`Haber detayı: ${article.title}\n\n${article.content}`);
                  }}
                >
                  Devamını Oku
                  <svg className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* View All News Button */}
        {news.length >= 6 && (
          <div className="text-center mt-12">
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
              Tüm Haberleri Görüntüle
              <svg className="w-5 h-5 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default NewsSection;