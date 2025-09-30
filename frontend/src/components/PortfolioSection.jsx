import React, { useState, useEffect } from 'react';

const PortfolioSection = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadProjects = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/projects?limit=9`);
      const data = await response.json();
      setProjects(data || []);
    } catch (error) {
      console.error('Error loading projects:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  // Get unique categories
  const categories = ['all', ...new Set(projects.map(p => p.category))];
  
  // Filter projects based on selected category
  const filteredProjects = selectedCategory === 'all' 
    ? projects 
    : projects.filter(p => p.category === selectedCategory);

  const getStatusColor = (status) => {
    const colors = {
      'completed': 'bg-green-100 text-green-800',
      'in_progress': 'bg-yellow-100 text-yellow-800',
      'planned': 'bg-blue-100 text-blue-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusLabel = (status) => {
    const labels = {
      'completed': 'Tamamlandı',
      'in_progress': 'Devam Ediyor',
      'planned': 'Planlandı'
    };
    return labels[status] || status;
  };

  if (loading) {
    return (
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mb-4"></div>
            <p className="text-gray-600">Projeler yükleniyor...</p>
          </div>
        </div>
      </section>
    );
  }

  if (!projects.length) {
    return null; // Don't show section if no projects
  }

  return (
    <section id="portfolio" className="py-20 bg-gradient-to-br from-gray-800 to-gray-900">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Başarılı Projelerimiz
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Müşterilerimizle birlikte gerçekleştirdiğimiz başarı hikayeleri ve elde ettiğimiz sonuçlar
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-purple-600 to-blue-600 mx-auto mt-6 rounded-full"></div>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center mb-12 gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                selectedCategory === category
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg transform scale-105'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {category === 'all' ? 'Tümü' : category}
            </button>
          ))}
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredProjects.map((project, index) => (
            <div 
              key={project.id}
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100 transform hover:-translate-y-2"
            >
              {/* Project Image */}
              {project.imageUrl && (
                <div className="relative overflow-hidden h-48">
                  <img 
                    src={project.imageUrl} 
                    alt={project.projectTitle}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  {/* Status Badge */}
                  <div className="absolute top-4 right-4">
                    <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(project.status)}`}>
                      {getStatusLabel(project.status)}
                    </span>
                  </div>
                </div>
              )}

              {/* Project Content */}
              <div className="p-6">
                {!project.imageUrl && (
                  <div className="flex justify-between items-center mb-4">
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 text-xs font-semibold rounded-full">
                      {project.category}
                    </span>
                    <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(project.status)}`}>
                      {getStatusLabel(project.status)}
                    </span>
                  </div>
                )}
                
                <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-purple-600 transition-colors">
                  {project.projectTitle}
                </h3>
                
                <p className="text-gray-600 font-medium mb-3 flex items-center">
                  <svg className="w-4 h-4 mr-2 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clipRule="evenodd" />
                  </svg>
                  {project.clientName}
                </p>
                
                <p className="text-gray-600 mb-4 text-sm line-clamp-3">
                  {project.description}
                </p>
                
                {/* Results */}
                {project.results && (
                  <div className="bg-green-50 border-l-4 border-green-400 p-3 mb-4">
                    <p className="text-green-700 text-sm font-medium">
                      <span className="flex items-center">
                        <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Sonuçlar:
                      </span>
                      {project.results}
                    </p>
                  </div>
                )}

                {/* Project Dates */}
                <div className="flex items-center justify-between text-xs text-gray-500">
                  {project.startDate && (
                    <span>
                      Başlama: {new Date(project.startDate).toLocaleDateString('tr-TR')}
                    </span>
                  )}
                  {project.endDate && (
                    <span>
                      Bitiş: {new Date(project.endDate).toLocaleDateString('tr-TR')}
                    </span>
                  )}
                </div>

                {/* Tags */}
                {project.tags && project.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-3">
                    {project.tags.slice(0, 3).map((tag, tagIndex) => (
                      <span key={tagIndex} className="bg-gray-100 text-gray-600 px-2 py-1 text-xs rounded-full">
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* View All Projects Button */}
        {projects.length >= 9 && (
          <div className="text-center mt-12">
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
              Tüm Projeleri Görüntüle
              <svg className="w-5 h-5 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </div>
        )}

        {/* Statistics */}
        <div className="mt-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl p-8 text-white">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">{projects.length}+</div>
              <p className="text-purple-100">Tamamlanan Proje</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">
                {new Set(projects.map(p => p.clientName)).size}+
              </div>
              <p className="text-purple-100">Mutlu Müşteri</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">%150+</div>
              <p className="text-purple-100">Ortalama Performans Artışı</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PortfolioSection;