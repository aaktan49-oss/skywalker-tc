import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  Users, 
  MessageSquare, 
  UserCheck, 
  TicketIcon,
  TrendingUp,
  Star,
  Activity
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = ({ token }) => {
  const [stats, setStats] = useState({
    influencers: { total: 0, pending: 0, approved: 0 },
    contacts: { total: 0, new: 0, replied: 0 },
    tickets: { total: 0, open: 0, in_progress: 0, resolved: 0, recent: 0 },
    customers: { total: 0, active: 0 }
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        setStats(response.data.data);
      }
    } catch (error) {
      console.error('Dashboard stats yüklenirken hata:', error);
      // Keep default stats structure on error
      setStats({
        influencers: { total: 0, pending: 0, approved: 0 },
        contacts: { total: 0, new: 0, replied: 0 },
        tickets: { total: 0, open: 0, in_progress: 0, resolved: 0, recent: 0 },
        customers: { total: 0, active: 0 }
      });
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
    <Card className="bg-slate-800/50 border-slate-700 hover:border-amber-500/50 transition-colors duration-300">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium">{title}</p>
            <p className={`text-3xl font-bold ${color} mt-2`}>{value}</p>
            {subtitle && (
              <p className="text-gray-500 text-sm mt-1">{subtitle}</p>
            )}
          </div>
          <div className={`bg-gradient-to-r ${color.replace('text-', 'from-').replace('-400', '-400/20')} to-transparent rounded-full p-3`}>
            <Icon className={`h-6 w-6 ${color}`} />
          </div>
        </div>
        {trend && (
          <div className="mt-4 flex items-center">
            <TrendingUp className="h-4 w-4 text-green-400 mr-1" />
            <span className="text-green-400 text-sm font-medium">{trend}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-400"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 mt-1">Skywalker.tc Yönetim Paneli</p>
        </div>
        <div className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-green-400" />
          <span className="text-green-400 text-sm font-medium">Sistem Aktif</span>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Toplam Müşteri"
          value={stats?.customers?.total || 0}
          subtitle={`${stats?.customers?.active || 0} aktif`}
          icon={Users}
          color="text-blue-400"
        />
        
        <StatCard
          title="Influencer Başvuru"
          value={stats?.influencers?.total || 0}
          subtitle={`${stats?.influencers?.pending || 0} beklemede`}
          icon={UserCheck}
          color="text-purple-400"
        />

        <StatCard
          title="İletişim Mesajı"
          value={stats?.contacts?.total || 0}
          subtitle={`${stats?.contacts?.new || 0} yeni`}
          icon={MessageSquare}
          color="text-green-400"
        />

        <StatCard
          title="Destek Talepleri"
          value={stats?.tickets?.total || 0}
          subtitle={`${stats?.tickets?.recent || 0} bu hafta`}
          icon={TicketIcon}
          color="text-amber-400"
        />
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Influencer Stats */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <UserCheck className="h-5 w-5 text-purple-400 mr-2" />
              Influencer Başvuruları
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Toplam Başvuru</span>
              <Badge variant="secondary" className="bg-purple-500/20 text-purple-400">
                {stats.influencers.total}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Onay Bekleyen</span>
              <Badge variant="secondary" className="bg-yellow-500/20 text-yellow-400">
                {stats.influencers.pending}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Onaylanan</span>
              <Badge variant="secondary" className="bg-green-500/20 text-green-400">
                {stats.influencers.approved}
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Ticket Stats */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <TicketIcon className="h-5 w-5 text-amber-400 mr-2" />
              Destek Talepleri
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Açık Talepler</span>
              <Badge variant="secondary" className="bg-red-500/20 text-red-400">
                {stats.tickets.open}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">İşlemde</span>
              <Badge variant="secondary" className="bg-blue-500/20 text-blue-400">
                {stats.tickets.in_progress}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Çözülenler</span>
              <Badge variant="secondary" className="bg-green-500/20 text-green-400">
                {stats.tickets.resolved}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="bg-gradient-to-r from-amber-500/10 to-orange-500/10 border-amber-500/30">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Star className="h-5 w-5 text-amber-400 mr-2 fill-current" />
            Hızlı İşlemler
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors duration-300 text-left">
              <UserCheck className="h-6 w-6 text-purple-400 mb-2" />
              <p className="text-white font-medium">Başvuruları</p>
              <p className="text-gray-400 text-sm">Gör</p>
            </button>
            
            <button className="p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors duration-300 text-left">
              <MessageSquare className="h-6 w-6 text-green-400 mb-2" />
              <p className="text-white font-medium">Mesajları</p>
              <p className="text-gray-400 text-sm">Yönet</p>
            </button>
            
            <button className="p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors duration-300 text-left">
              <TicketIcon className="h-6 w-6 text-amber-400 mb-2" />
              <p className="text-white font-medium">Talepleri</p>
              <p className="text-gray-400 text-sm">Çöz</p>
            </button>
            
            <button className="p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors duration-300 text-left">
              <Users className="h-6 w-6 text-blue-400 mb-2" />
              <p className="text-white font-medium">Müşterileri</p>
              <p className="text-gray-400 text-sm">Listele</p>
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;