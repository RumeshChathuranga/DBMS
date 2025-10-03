import { useEffect, useState } from 'react';
import { MainLayout } from '../components/layout';
import { Card } from '../components/common';
import { Hotel, Calendar, DollarSign, FileText, TrendingUp, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface Stats {
  totalRooms: number;
  occupiedRooms: number;
  todayCheckIns: number;
  todayCheckOuts: number;
  pendingInvoices: number;
  monthlyRevenue: number;
}

const DashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<Stats>({
    totalRooms: 21,
    occupiedRooms: 0,
    todayCheckIns: 0,
    todayCheckOuts: 0,
    pendingInvoices: 0,
    monthlyRevenue: 0,
  });

  const occupancyRate = stats.totalRooms > 0 
    ? ((stats.occupiedRooms / stats.totalRooms) * 100).toFixed(1)
    : '0';

  const statCards = [
    {
      title: 'Total Rooms',
      value: stats.totalRooms,
      icon: <Hotel className="text-primary-600" size={24} />,
      bgColor: 'bg-primary-50',
      change: null,
    },
    {
      title: 'Occupied Rooms',
      value: stats.occupiedRooms,
      icon: <Calendar className="text-green-600" size={24} />,
      bgColor: 'bg-green-50',
      subtitle: `${occupancyRate}% occupancy`,
    },
    {
      title: "Today's Check-ins",
      value: stats.todayCheckIns,
      icon: <Users className="text-blue-600" size={24} />,
      bgColor: 'bg-blue-50',
    },
    {
      title: "Today's Check-outs",
      value: stats.todayCheckOuts,
      icon: <Users className="text-purple-600" size={24} />,
      bgColor: 'bg-purple-50',
    },
    {
      title: 'Monthly Revenue',
      value: `LKR ${stats.monthlyRevenue.toLocaleString()}`,
      icon: <DollarSign className="text-yellow-600" size={24} />,
      bgColor: 'bg-yellow-50',
      subtitle: 'This month',
    },
    {
      title: 'Pending Invoices',
      value: stats.pendingInvoices,
      icon: <FileText className="text-red-600" size={24} />,
      bgColor: 'bg-red-50',
    },
  ];

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening in your hotel today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {statCards.map((stat, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-600 mb-1">
                    {stat.title}
                  </p>
                  <p className="text-3xl font-bold text-gray-900 mb-1">
                    {stat.value}
                  </p>
                  {stat.subtitle && (
                    <p className="text-sm text-gray-500">{stat.subtitle}</p>
                  )}
                </div>
                <div className={`p-4 rounded-xl ${stat.bgColor}`}>
                  {stat.icon}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Quick Actions */}
        <Card title="Quick Actions">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn-primary btn-lg flex items-center justify-center gap-2">
              <Calendar size={20} />
              New Booking
            </button>
            <button className="btn-primary btn-lg flex items-center justify-center gap-2">
              <Users size={20} />
              Check-In Guest
            </button>
            <button className="btn-primary btn-lg flex items-center justify-center gap-2">
              <DollarSign size={20} />
              Process Payment
            </button>
          </div>
        </Card>

        {/* Recent Activity */}
        <Card title="Recent Activity">
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
                <TrendingUp className="text-primary-600" size={20} />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  System is ready for operations
                </p>
                <p className="text-xs text-gray-600">
                  All systems operational
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;