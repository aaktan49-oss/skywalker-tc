import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { toast } from 'sonner';
import { 
  Star, 
  Instagram, 
  Play, 
  Mail, 
  Phone, 
  User,
  Send,
  CheckCircle
} from 'lucide-react';

const InfluencerApplicationSection = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    instagram: '',
    tiktok: '',
    followersCount: '',
    category: '',
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
        "Başvurun başarıyla gönderildi! Ekibimiz en kısa sürede sizinle iletişime geçecek.",
        {
          duration: 5000,
          icon: <CheckCircle className="h-5 w-5" />
        }
      );
      
      // Reset form
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        instagram: '',
        tiktok: '',
        followersCount: '',
        category: '',
        message: ''
      });
    } catch (error) {
      toast.error("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="influencer-apply" className="py-20 bg-gradient-to-br from-slate-900 to-purple-900/30">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-purple-500/20 border border-purple-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-purple-400 fill-current" />
            <span className="text-purple-400 text-sm font-medium">Influencer Başvuru</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Güçlere</span>
            <span className="bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
              Katılmaya Hazır mısın?
            </span>
          </h2>
          
          <p className="text-xl text-gray-200 max-w-2xl mx-auto">
            Formu doldur, sosyal medya hesaplarını paylaş ve Skywalker ailesinin bir üyesi ol!
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-2xl text-white text-center flex items-center justify-center space-x-2">
                <User className="h-6 w-6 text-purple-400" />
                <span className=\"text-lg font-bold text-white\">Influencer Başvuru Formu</span>
              </CardTitle>
            </CardHeader>
            
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Personal Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="firstName" className="text-gray-300">Ad *</Label>
                    <Input
                      id="firstName"
                      name="firstName"
                      type="text"
                      required
                      value={formData.firstName}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="Adınız"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="lastName" className="text-gray-300">Soyad *</Label>
                    <Input
                      id="lastName"
                      name="lastName"
                      type="text"
                      required
                      value={formData.lastName}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="Soyadınız"
                    />
                  </div>
                </div>

                {/* Contact Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-gray-300 flex items-center space-x-1">
                      <Mail className="h-4 w-4" />
                      <span>E-posta *</span>
                    </Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      required
                      value={formData.email}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="ornek@email.com"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="phone" className="text-gray-300 flex items-center space-x-1">
                      <Phone className="h-4 w-4" />
                      <span>Telefon *</span>
                    </Label>
                    <Input
                      id="phone"
                      name="phone"
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="+90 5XX XXX XX XX"
                    />
                  </div>
                </div>

                {/* Social Media Accounts */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="instagram" className="text-gray-300 flex items-center space-x-1">
                      <Instagram className="h-4 w-4" />
                      <span>Instagram Hesabı *</span>
                    </Label>
                    <Input
                      id="instagram"
                      name="instagram"
                      type="text"
                      required
                      value={formData.instagram}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="@kullanici_adi"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="tiktok" className="text-gray-300 flex items-center space-x-1">
                      <Play className="h-4 w-4" />
                      <span>TikTok Hesabı</span>
                    </Label>
                    <Input
                      id="tiktok"
                      name="tiktok"
                      type="text"
                      value={formData.tiktok}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="@kullanici_adi (opsiyonel)"
                    />
                  </div>
                </div>

                {/* Additional Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="followersCount" className="text-gray-300">Toplam Takipçi Sayısı *</Label>
                    <Input
                      id="followersCount"
                      name="followersCount"
                      type="text"
                      required
                      value={formData.followersCount}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="Örn: 10K, 50K, 100K"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="category" className="text-gray-300">İçerik Kategorisi *</Label>
                    <Input
                      id="category"
                      name="category"
                      type="text"
                      required
                      value={formData.category}
                      onChange={handleInputChange}
                      className="bg-slate-700 border-slate-600 text-white focus:border-purple-500"
                      placeholder="Moda, Teknoloji, Yaşam Tarzı..."
                    />
                  </div>
                </div>

                {/* Message */}
                <div className="space-y-2">
                  <Label htmlFor="message" className="text-gray-300">Ek Mesaj</Label>
                  <Textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    className="bg-slate-700 border-slate-600 text-white focus:border-purple-500 min-h-24"
                    placeholder="Kendinden bahset, neden Skywalker ailesine katılmak istiyorsun?"
                  />
                </div>

                {/* Submit Button */}
                <div className="text-center pt-6">
                  <Button 
                    type="submit"
                    disabled={isSubmitting}
                    size="lg"
                    className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white font-semibold rounded-full px-12 py-4 disabled:opacity-50"
                  >
                    {isSubmitting ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        <span>Gönderiliyor...</span>
                      </>
                    ) : (
                      <>
                        <Send className="mr-2 h-5 w-5" />
                        <span>Başvuru Gönder</span>
                      </>
                    )}
                  </Button>
                  
                  <p className="text-sm text-gray-400 mt-4">
                    * işaretli alanlar zorunludur. Başvurunuz 24-48 saat içinde değerlendirilecektir.
                  </p>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default InfluencerApplicationSection;