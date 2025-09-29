import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ArrowRight, Star, Users, TrendingUp, Instagram, Play } from 'lucide-react';

const InfluencerSection = () => {
  const handleInfluencerApply = () => {
    const element = document.querySelector('#influencer-apply');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleContactUs = () => {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const features = [
    {
      icon: TrendingUp,
      title: "Yüksek Komisyon",
      description: "Sektörün en yüksek komisyon oranları ile kazancınızı maksimize edin"
    },
    {
      icon: Users,
      title: "Geniş Müşteri Ağı",
      description: "50+ başarılı firma portföyümüzle sürekli iş imkanları"
    },
    {
      icon: Star,
      title: "Profesyonel Destek",
      description: "Uzman ekibimizden 7/24 içerik ve strateji desteği alın"
    }
  ];

  return (
    <section id="influencer" className="py-20 bg-gradient-to-br from-slate-900 to-indigo-900">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-purple-500/20 border border-purple-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-purple-400 fill-current" />
            <span className="text-purple-400 text-sm font-medium">Influencer Güç Birliği</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Sosyal Medya</span>
            <span className="bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
              Galaksisinin Lideri Ol
            </span>
          </h2>
          
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Skywalker ailesine katıl ve Trendyol evreninde güçlü bir müttefik olarak 
            hem kazanç elde et, hem de markaların büyümesine katkıda bulun.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h3 className="text-2xl md:text-3xl font-bold text-white">
                Neden <span className="text-purple-400">Skywalker</span> Ailesine Katılmalısın?
              </h3>
              
              <p className="text-lg text-gray-200 leading-relaxed">
                10+ yıl deneyimimiz ve 50+ başarılı firma ile çalışma geçmişimizle, 
                influencer'lara en iyi fırsatları sunuyoruz. Bizimle sadece içerik üretmekle kalmayacak, 
                aynı zamanda gerçek bir işbirliğinin parçası olacaksın.
              </p>
            </div>

            {/* Features */}
            <div className="space-y-4">
              {features.map((feature, index) => {
                const IconComponent = feature.icon;
                return (
                  <div key={index} className="flex items-start space-x-4 p-4 rounded-lg bg-slate-800/30 border border-slate-700/50">
                    <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg p-2 flex-shrink-0">
                      <IconComponent className="h-5 w-5 text-purple-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">{feature.title}</h4>
                      <p className="text-gray-400 text-sm">{feature.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
            
            <div className="pt-4 space-y-4">
              <Button 
                onClick={handleInfluencerApply}
                size="lg"
                className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white font-semibold rounded-full group w-full sm:w-auto"
              >
                <Star className="mr-2 h-5 w-5" />
                <span>Hemen Başvur</span>
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
              
              <Button 
                onClick={handleContactUs}
                variant="outline"
                size="lg"
                className="border-2 border-gray-500 text-gray-300 hover:bg-gray-500 hover:text-white rounded-full font-semibold w-full sm:w-auto"
              >
                Daha Fazla Bilgi Al
              </Button>
            </div>
          </div>

          {/* Right Content - Application CTA */}
          <div className="relative">
            <Card className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-purple-500/30">
              <CardHeader>
                <div className="text-center">
                  <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <Users className="h-8 w-8 text-purple-400" />
                  </div>
                  <CardTitle className="text-xl text-white">İnfluencer Başvuru Süreci</CardTitle>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold">1</div>
                    <span className="text-gray-300">Başvuru formunu doldur</span>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold">2</div>
                    <span className="text-gray-300">Sosyal medya hesaplarını paylaş</span>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold">3</div>
                    <span className="text-gray-300">Ekibimiz seni değerlendirsin</span>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full flex items-center justify-center text-white text-sm font-bold">✓</div>
                    <span className="text-amber-400 font-semibold">Güç birliğine hoşgeldin!</span>
                  </div>
                </div>
                
                <div className="pt-4 border-t border-gray-700">
                  <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Instagram className="h-4 w-4" />
                      <span>Instagram</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Play className="h-4 w-4" />
                      <span>TikTok</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InfluencerSection;