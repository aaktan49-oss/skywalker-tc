import React from 'react';
import { Card, CardContent } from './ui/card';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Star } from 'lucide-react';
import { testimonials } from '../mock';

const TestimonialsSection = () => {
  return (
    <section id="testimonials" className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Güçlü Müttefik Sesleri</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Galaksinin</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Başarı Hikayeleri
            </span>
          </h2>
          
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Trendyol evreninde liderlik yapmış müşterilerimizin deneyimleri. 
            Her biri, güçlü strateji ve Jedi ustalığının kanıtı.
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <Card key={testimonial.id} className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-all duration-300 group hover:transform hover:-translate-y-2">
              <CardContent className="p-6">
                {/* Rating Stars */}
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-amber-400 fill-current" />
                  ))}
                </div>
                
                {/* Comment */}
                <p className="text-gray-200 mb-6 leading-relaxed italic">
                  "{testimonial.comment}"
                </p>
                
                {/* Author Info */}
                <div className="flex items-center">
                  <Avatar className="h-12 w-12 mr-4">
                    <AvatarImage src={testimonial.avatar} alt={testimonial.name} />
                    <AvatarFallback className="bg-amber-500/20 text-amber-400">
                      {testimonial.name.charAt(0)}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <h4 className="font-semibold text-white">{testimonial.name}</h4>
                    <p className="text-sm text-gray-400">{testimonial.company}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Stats Section */}
        <div className="mt-20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-amber-400 mb-2">50+</div>
              <p className="text-gray-200">Güçlü Müttefik</p>
              <p className="text-sm text-gray-400">Başarılı Firma</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-blue-400 mb-2">%99+</div>
              <p className="text-gray-300">Optimizasyon</p>
              <p className="text-sm text-gray-500">Başarı Oranı</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-green-400 mb-2">15+</div>
              <p className="text-gray-300">Uzman Takım</p>
              <p className="text-sm text-gray-500">Jedi Konseyi</p>
            </div>
            <div className="p-6">
              <div className="text-3xl md:text-4xl font-bold text-purple-400 mb-2">10+</div>
              <p className="text-gray-300">Yıl Deneyim</p>
              <p className="text-sm text-gray-500">Galakside</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;