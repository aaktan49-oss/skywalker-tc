import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { 
  Shield, 
  Target, 
  Zap, 
  Users, 
  TrendingUp, 
  Star,
  ArrowRight
} from 'lucide-react';

const AboutSection = () => {
  const aboutFeatures = [
    {
      icon: Shield,
      title: "10+ Yıl Galaksi Deneyimi",
      description: "E-ticaret evreninde 10+ yılı aşkın deneyimimizle, her türlü zorluğa karşı hazırlıklıyız."
    },
    {
      icon: Users,
      title: "15+ Jedi Konseyi",
      description: "Her biri kendi alanında uzman 15+ kişilik güçlü takımımızla yanınızdayız."
    },
    {
      icon: Target,
      title: "Minimum Bütçe, Maksimum Kazanç",
      description: "Felsefemiz basit: En az harcamayla en yüksek getiriyi sağlamak."
    },
    {
      icon: TrendingUp,
      title: "%99+ Başarı Oranı",
      description: "Optimizasyon çalışmalarımızda %99 üzerinde başarı oranına ulaşıyoruz."
    }
  ];

  const handleScrollToContact = () => {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="about" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Skywalker Hikayesi</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">E-ticaret</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              İmparatorluğu Kurucuları
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          {/* Left Content */}
          <div className="space-y-6">
            <h3 className="text-2xl md:text-3xl font-bold text-white">
              Güç Bizimle <span className="text-amber-400">Başladı</span>
            </h3>
            
            <p className="text-lg text-gray-300 leading-relaxed">
              Skywalker.tc olarak, Trendyol galaksisinde 10+ yıldır işletmelerin dijital dönüşüm 
              yolculuklarına rehberlik ediyoruz. 50+ başarılı firma ile çalışarak, minimum bütçeyle 
              maksimum kazanç felsefesini hayata geçirdik.
            </p>
            
            <p className="text-lg text-gray-300 leading-relaxed">
              Her müşterimizi galaksinin lideri haline getirmek için, Jedi konseyi deneyimimizi 
              ve kanıtlanmış stratejilerimizi kullanıyoruz. Bizimle çalışan her işletme, 
              e-ticaret evreninde güçlü bir varlık haline geliyor.
            </p>
            
            <div className="pt-4">
              <Button 
                onClick={handleScrollToContact}
                size="lg"
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold rounded-full group"
              >
                <Zap className="mr-2 h-5 w-5" />
                <span>Güçlere Katıl</span>
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </div>
          </div>

          {/* Right Content - Mission Statement */}
          <div className="relative">
            <Card className="bg-gradient-to-br from-amber-500/10 to-orange-500/10 border-amber-500/30">
              <CardContent className="p-8">
                <div className="text-center mb-6">
                  <Star className="h-12 w-12 text-amber-400 fill-current mx-auto mb-4" />
                  <h4 className="text-xl font-bold text-white">Misyonumuz</h4>
                </div>
                
                <p className="text-gray-300 text-center leading-relaxed italic text-lg">
                  "Her işletmenin Trendyol galaksisinde kendi imparatorluğunu kurmasını sağlamak. 
                  Güçlü stratejiler, uzman rehberlik ve sürekli destek ile e-ticaret evreninde 
                  dominasyon yaratmak."
                </p>
                
                <div className="text-center mt-6">
                  <span className="text-amber-400 font-semibold">- Skywalker Jedi Konseyi</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {aboutFeatures.map((feature, index) => {
            const IconComponent = feature.icon;
            
            return (
              <Card key={index} className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300 group text-center">
                <CardContent className="p-6">
                  <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 group-hover:from-amber-500/30 group-hover:to-orange-500/30 transition-all duration-300">
                    <IconComponent className="h-8 w-8 text-amber-400" />
                  </div>
                  
                  <h4 className="font-bold text-white mb-3 text-lg">{feature.title}</h4>
                  <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default AboutSection;