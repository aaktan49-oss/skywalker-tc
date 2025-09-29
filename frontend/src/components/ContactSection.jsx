import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { toast } from 'sonner';
import {
  Star,
  Mail,
  Phone,
  MapPin,
  Clock,
  Send,
  MessageSquare,
  CheckCircle
} from 'lucide-react';
import { contactInfo } from '../mock';

const ContactSection = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    service: '',
    message: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Mock submission - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast.success(
        "Mesajınız başarıyla gönderildi! 24 saat içinde size döneceğiz.",
        {
          duration: 5000,
          icon: <CheckCircle className="h-5 w-5" />
        }
      );
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        company: '',
        service: '',
        message: ''
      });
    } catch (error) {
      toast.error("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="contact" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Galaksi İletişim</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Güçlere</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Katılmaya Hazır mısın?
            </span>
          </h2>
          
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Trendyol evreninde dominasyon kurma yolculuğunuz şimdi başlıyor. 
            Bizimle iletişime geçin ve güçlü stratejilerin kapılarını aralıyın.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-bold text-white mb-6">Bize Ulaşın</h3>
              
              <div className="space-y-6">
                {/* Phone */}
                <div className="flex items-start space-x-4 p-4 rounded-lg bg-slate-800/50">
                  <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-lg p-3 flex-shrink-0">
                    <Phone className="h-6 w-6 text-amber-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">Telefon</h4>
                    <p className="text-gray-300">{contactInfo.phone}</p>
                    <p className="text-sm text-gray-400">7/24 WhatsApp Desteği</p>
                  </div>
                </div>
                
                {/* Email */}
                <div className="flex items-start space-x-4 p-4 rounded-lg bg-slate-800/50">
                  <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-lg p-3 flex-shrink-0">
                    <Mail className="h-6 w-6 text-amber-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">E-posta</h4>
                    <p className="text-gray-300">{contactInfo.email}</p>
                    <p className="text-sm text-gray-400">24 saat içinde yanıt</p>
                  </div>
                </div>
                
                {/* Address */}
                <div className="flex items-start space-x-4 p-4 rounded-lg bg-slate-800/50">
                  <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-lg p-3 flex-shrink-0">
                    <MapPin className="h-6 w-6 text-amber-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">Adres</h4>
                    <p className="text-gray-300">{contactInfo.address}</p>
                    <p className="text-sm text-gray-400">Galaksi Merkezi</p>
                  </div>
                </div>
                
                {/* Working Hours */}
                <div className="flex items-start space-x-4 p-4 rounded-lg bg-slate-800/50">
                  <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-lg p-3 flex-shrink-0">
                    <Clock className="h-6 w-6 text-amber-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">Çalışma Saatleri</h4>
                    <p className="text-gray-300">{contactInfo.workingHours}</p>
                    <p className="text-sm text-gray-400">Acil durumlar için WhatsApp</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Quick Contact Actions */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Hızlı İletişim</h4>
              <div className="flex flex-col sm:flex-row gap-3">
                <a 
                  href={`https://wa.me/${contactInfo.phone.replace(/[^0-9]/g, '')}`}
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex-1 inline-flex items-center justify-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-full font-semibold transition-colors duration-300"
                >
                  <MessageSquare className="mr-2 h-5 w-5" />
                  WhatsApp
                </a>
                <a 
                  href={`mailto:${contactInfo.email}`}
                  className="flex-1 inline-flex items-center justify-center px-6 py-3 border border-amber-500 text-amber-400 hover:bg-amber-500 hover:text-white rounded-full font-semibold transition-all duration-300"
                >
                  <Mail className="mr-2 h-5 w-5" />
                  E-posta
                </a>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-xl text-white text-center">İletişim Formu</CardTitle>
              </CardHeader>
              
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  {/* Name and Email */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name" className="text-gray-300">Ad Soyad *</Label>
                      <Input
                        id="name"
                        name="name"
                        type="text"
                        required
                        value={formData.name}
                        onChange={handleInputChange}
                        className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                        placeholder="Adınız Soyadınız"
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-gray-300">E-posta *</Label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        required
                        value={formData.email}
                        onChange={handleInputChange}
                        className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                        placeholder="ornek@email.com"
                      />
                    </div>
                  </div>
                  
                  {/* Phone and Company */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="phone" className="text-gray-300">Telefon</Label>
                      <Input
                        id="phone"
                        name="phone"
                        type="tel"
                        value={formData.phone}
                        onChange={handleInputChange}
                        className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                        placeholder="+90 5XX XXX XX XX"
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="company" className="text-gray-300">Firma Adı</Label>
                      <Input
                        id="company"
                        name="company"
                        type="text"
                        value={formData.company}
                        onChange={handleInputChange}
                        className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                        placeholder="Firma adınız"
                      />
                    </div>
                  </div>
                  
                  {/* Service */}
                  <div className="space-y-2">
                    <Label htmlFor="service" className="text-gray-300">Hangi hizmetle ilgileniyorsunuz?</Label>
                    <Input
                      id="service"
                      name="service"
                      type="text"
                      value={formData.service}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                      placeholder="SEO, Reklam Yönetimi, Tam Paket..."
                    />
                  </div>
                  
                  {/* Message */}
                  <div className="space-y-2">
                    <Label htmlFor="message" className="text-gray-300">Mesajınız *</Label>
                    <Textarea
                      id="message"
                      name="message"
                      required
                      value={formData.message}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-amber-500 min-h-24"
                      placeholder="Projeniz hakkında detaylar, beklentileriniz..."
                    />
                  </div>
                  
                  {/* Submit Button */}
                  <div className="pt-4">
                    <Button 
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold rounded-full py-3 disabled:opacity-50"
                    >
                      {isSubmitting ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                          <span>Gönderiliyor...</span>
                        </>
                      ) : (
                        <>
                          <Send className="mr-2 h-5 w-5" />
                          <span>Mesaj Gönder</span>
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;