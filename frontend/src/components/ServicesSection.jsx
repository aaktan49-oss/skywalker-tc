import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Package, 
  Search, 
  Palette, 
  Target, 
  Users, 
  Globe, 
  BarChart3, 
  UserCheck, 
  MessageSquare,
  ArrowRight,
  Star
} from 'lucide-react';
import { services } from '../mock';

const iconMap = {
  Package,
  Search,
  Palette,
  Target,
  Users,
  Globe,
  BarChart3,
  UserCheck,
  MessageSquare
};

const ServicesSection = () => {
  const handleContactUs = () => {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="services" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Galaktik Hizmetler</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Trendyol Evreninde</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Ustaca Hizmetler
            </span>
          </h2>
          
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Her hizmetimiz, e-ticaret galaksisinde dominasyonunuz için özel olarak tasarlandı. 
            Jedi konseyi deneyimimizle işletmenizi zirveye taşıyoruz.
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service) => {
            const IconComponent = iconMap[service.icon] || Package;
            
            return (
              <Card key={service.id} className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300 group hover:transform hover:-translate-y-2">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-xl group-hover:from-amber-500/30 group-hover:to-orange-500/30 transition-all duration-300">
                      <IconComponent className="h-6 w-6 text-amber-400" />
                    </div>
                  </div>
                  
                  <CardTitle className="text-xl font-bold text-white group-hover:text-amber-400 transition-colors duration-300">
                    {service.title}
                  </CardTitle>
                </CardHeader>
                
                <CardContent>
                  <p className="text-gray-300 mb-6 leading-relaxed">
                    {service.description}
                  </p>
                  
                  <ul className="space-y-2 mb-6">
                    {service.features.map((feature, index) => (
                      <li key={index} className="flex items-center text-sm text-gray-400">
                        <div className="w-1.5 h-1.5 bg-amber-400 rounded-full mr-3 flex-shrink-0"></div>
                        {feature}
                      </li>
                    ))}
                  </ul>
                  
                  <Button 
                    onClick={handleContactUs}
                    className="w-full bg-gradient-to-r from-slate-700 to-slate-600 hover:from-amber-500 hover:to-orange-600 text-white border-0 transition-all duration-300 group/btn"
                  >
                    <span>Hemen Başla</span>
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover/btn:translate-x-1" />
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Additional Services Note */}
        <div className="text-center mt-16">
          <Card className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border-blue-500/30 max-w-2xl mx-auto">
            <CardContent className="p-8">
              <MessageSquare className="h-12 w-12 text-blue-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-3">Skywalker WhatsApp Destek Grupları</h3>
              <p className="text-gray-300 mb-4">
                Tüm ekip liderlerimizle doğrudan iletişim kurun. 7/24 destek, anlık çözümler ve süreç takibi için özel WhatsApp gruplarımıza katılın.
              </p>
              <Button 
                onClick={handleContactUs}
                className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white"
              >
                WhatsApp Grubuna Katıl
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;