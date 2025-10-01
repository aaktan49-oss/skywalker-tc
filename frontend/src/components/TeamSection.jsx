import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Star, Zap, Shield } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TeamSection = () => {
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTeamMembers();
  }, []);

  const fetchTeamMembers = async () => {
    try {
      const response = await fetch(`${API}/content/team`);
      const data = await response.json();
      setTeamMembers(data || []);
    } catch (error) {
      console.error('Team loading error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRoleIcon = (role) => {
    if (role.includes('Lideri') || role.includes('Uzmanı')) {
      return Shield;
    } else if (role.includes('Strateji') || role.includes('Danışmanlık')) {
      return Star;
    } else {
      return Zap;
    }
  };

  const getRoleColor = (character) => {
    if (character.includes('Master') || character.includes('Grand Master')) {
      return 'from-amber-400 to-orange-500';
    } else if (character.includes('Knight') || character.includes('Jedi')) {
      return 'from-blue-400 to-indigo-500';
    } else if (character.includes('Leader') || character.includes('Rebel')) {
      return 'from-green-400 to-emerald-500';
    } else {
      return 'from-purple-400 to-pink-500';
    }
  };

  if (loading) {
    return (
      <section id="team" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="container mx-auto px-4 lg:px-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-400 mx-auto"></div>
            <p className="text-gray-400 mt-4">Jedi Konseyi yükleniyor...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="team" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto px-4 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Galaktik Jedi Konseyi</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Uzman</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Takımımız
            </span>
          </h2>
          
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Her biri kendi alanında usta olan 9 uzmanımız, Trendyol evreninde size rehberlik etmek için hazır. 
            Güç onlarla birlikte!
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {teamMembers.map((member) => {
            const IconComponent = getRoleIcon(member.role);
            const gradientColor = getRoleColor(member.character);
            
            return (
              <Card key={member.id} className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300 group hover:transform hover:-translate-y-2">
                <CardHeader className="pb-4">
                  <div className="flex flex-col items-center text-center">
                    <div className="relative mb-4">
                      <img 
                        src={member.avatar || 'https://images.unsplash.com/photo-1566753323558-f4e0952af115?w=150&h=150&fit=crop&crop=face'} 
                        alt={member.name} 
                        className="h-20 w-20 rounded-full object-cover border-3 border-amber-400/50 group-hover:border-amber-400 transition-colors duration-300"
                      />
                      <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                        <div className={`bg-gradient-to-r ${gradientColor} rounded-full p-2`}>
                          <IconComponent className="h-4 w-4 text-white" />
                        </div>
                      </div>
                    </div>
                    
                    <CardTitle className="text-xl font-bold text-white group-hover:text-amber-400 transition-colors duration-300 mb-2">
                      {member.name}
                    </CardTitle>
                    
                    <Badge 
                      variant="secondary" 
                      className={`bg-gradient-to-r ${gradientColor} text-white border-0 mb-3 px-3 py-1`}
                    >
                      {member.character}
                    </Badge>
                  </div>
                </CardHeader>
                
                <CardContent className="text-center">
                  <div className="mb-4">
                    <h4 className="font-semibold text-amber-400 text-lg mb-2">
                      {member.role}
                    </h4>
                    
                    <p className="text-gray-200 text-sm leading-relaxed">
                      {member.specialization}
                    </p>
                  </div>
                  
                  <div className="flex justify-center">
                    <div className="flex space-x-1">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className="h-4 w-4 text-amber-400 fill-current" />
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="mt-20 text-center">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-amber-400 mb-2">9+</div>
              <p className="text-gray-200">Uzman Jedi</p>
              <p className="text-sm text-gray-400">Farklı Alanlarda</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-blue-400 mb-2">15+</div>
              <p className="text-gray-200">Yıl Deneyim</p>
              <p className="text-sm text-gray-400">Toplamda</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-green-400 mb-2">50+</div>
              <p className="text-gray-200">Proje Başarısı</p>
              <p className="text-sm text-gray-400">Birlikte</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-purple-400 mb-2">7/24</div>
              <p className="text-gray-200">Destek</p>
              <p className="text-sm text-gray-400">Her Zaman</p>
            </div>
          </div>
        </div>
        
        <div className="mt-16 text-center">
          <Card className="bg-gradient-to-r from-amber-500/10 to-orange-500/10 border-amber-500/30 max-w-2xl mx-auto">
            <CardContent className="p-8">
              <Star className="h-12 w-12 text-amber-400 mx-auto mb-4 fill-current" />
              <h3 className="text-xl font-bold text-white mb-3">
                Uzman Takımımızla Çalışmaya Hazır mısınız?
              </h3>
              <p className="text-gray-200 mb-4">
                Her biri alanının ustası olan Jedi konseyi üyelerimizle tanışın ve 
                Trendyol evrenindeki yolculuğunuza başlayın.
              </p>
              <button 
                onClick={() => {
                  const element = document.querySelector('#contact');
                  if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white px-6 py-3 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-amber-500/25"
              >
                Hemen İletişime Geç
              </button>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default TeamSection;