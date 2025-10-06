import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { MainLayout } from "../components/layout";
import { Card } from "../components/common";
import {
  Hotel,
  Calendar,
  DollarSign,
  FileText,
  TrendingUp,
  Users,
  CheckCircle,
  LogIn,
  LogOut,
  Plus,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { roomService, bookingService, billingService } from "../services";
import { toast } from "react-toastify";

interface Stats {
  totalRooms: number;
  occupiedRooms: number;
  todayCheckIns: number;
  todayCheckOuts: number;
  pendingInvoices: number;
  monthlyRevenue: number;
}

interface RecentActivity {
  id: string;
  type: "booking" | "checkin" | "checkout" | "payment";
  title: string;
  description: string;
  timestamp: string;
  icon: React.ReactNode;
  color: string;
}

const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState<Stats>({
    totalRooms: 0,
    occupiedRooms: 0,
    todayCheckIns: 0,
    todayCheckOuts: 0,
    pendingInvoices: 0,
    monthlyRevenue: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>(
    []
  );

  useEffect(() => {
    console.log("Dashboard useEffect triggered, user:", user);
    fetchDashboardStats();
    fetchRecentActivities();
  }, [user]);

  const fetchDashboardStats = async () => {
    if (!user) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const branchID = user.branchID || 1; // Default to branch 1 if not set
      console.log(
        "Fetching dashboard stats for branch:",
        branchID,
        "User:",
        user
      );

      // Fetch all data in parallel with individual error handling
      const [rooms, checkIns, checkOuts, pendingInvoices] = await Promise.all([
        roomService.getRoomsByBranch(branchID).catch((err) => {
          console.error("Failed to fetch rooms:", err);
          return [];
        }),
        bookingService.getTodaysCheckIns(branchID).catch((err) => {
          console.error("Failed to fetch check-ins:", err);
          return [];
        }),
        bookingService.getTodaysCheckOuts(branchID).catch((err) => {
          console.error("Failed to fetch check-outs:", err);
          return [];
        }),
        billingService.getPendingInvoices(branchID).catch((err) => {
          console.error("Failed to fetch invoices:", err);
          return [];
        }),
      ]);

      console.log("Dashboard data:", {
        rooms,
        checkIns,
        checkOuts,
        pendingInvoices,
      });

      // Calculate stats
      const totalRooms = rooms.length;
      const occupiedRooms = rooms.filter(
        (r) => r.roomStatus === "Occupied"
      ).length;

      setStats({
        totalRooms,
        occupiedRooms,
        todayCheckIns: checkIns.length,
        todayCheckOuts: checkOuts.length,
        pendingInvoices: pendingInvoices.length,
        monthlyRevenue: pendingInvoices.reduce(
          (sum, inv) => sum + (inv.totalAmount || 0),
          0
        ),
      });
    } catch (error: any) {
      console.error("Error fetching dashboard stats:", error);
      toast.error("Failed to load dashboard statistics");
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentActivities = async () => {
    if (!user) return;

    try {
      const branchID = user.branchID || 1;

      // First try to get real activity logs
      const activityLogs = await bookingService
        .getRecentActivities(10, branchID)
        .catch(() => []);

      if (activityLogs && activityLogs.length > 0) {
        // Use real activity logs from the system
        const activities: RecentActivity[] = activityLogs.map((log: any) => ({
          id: log.id,
          type: log.type,
          title: log.title,
          description: `${log.description} by ${log.user}`,
          timestamp: new Date(log.timestamp).toLocaleString(),
          icon: getActivityIcon(log.type),
          color: getActivityColor(log.type),
        }));

        setRecentActivities(activities);
        return;
      }

      // Fallback: Construct activities from existing data
      const [recentBookings, todaysCheckIns, todaysCheckOuts] =
        await Promise.all([
          bookingService.getBookings({ page: 1, page_size: 5 }).catch(() => []), // Get 5 recent bookings
          bookingService.getTodaysCheckIns(branchID).catch(() => []),
          bookingService.getTodaysCheckOuts(branchID).catch(() => []),
        ]);

      const activities: RecentActivity[] = [];

      // Add recent bookings
      recentBookings.slice(0, 2).forEach((booking: any) => {
        const bookingDate = new Date(booking.checkInDate);
        const isToday =
          bookingDate.toDateString() === new Date().toDateString();
        const timeAgo = isToday ? "Today" : bookingDate.toLocaleDateString();

        activities.push({
          id: `booking-${booking.bookingID}`,
          type: "booking",
          title: "New Booking Created",
          description: `${booking.firstName} ${booking.lastName} - Room ${booking.roomNo} (${booking.typeName})`,
          timestamp: timeAgo,
          icon: <Plus className="text-blue-600" size={16} />,
          color: "bg-blue-100",
        });
      });

      // Add today's check-ins
      todaysCheckIns.slice(0, 2).forEach((checkin: any) => {
        activities.push({
          id: `checkin-${checkin.bookingID}`,
          type: "checkin",
          title: "Guest Checked In",
          description: `${checkin.firstName} ${checkin.lastName} - Room ${checkin.roomNo}`,
          timestamp: "Today",
          icon: <LogIn className="text-green-600" size={16} />,
          color: "bg-green-100",
        });
      });

      // Add today's check-outs
      todaysCheckOuts.slice(0, 2).forEach((checkout: any) => {
        activities.push({
          id: `checkout-${checkout.bookingID}`,
          type: "checkout",
          title: "Guest Checked Out",
          description: `${checkout.firstName} ${checkout.lastName} - Room ${checkout.roomNo}`,
          timestamp: "Today",
          icon: <LogOut className="text-orange-600" size={16} />,
          color: "bg-orange-100",
        });
      });

      // Sort by type priority and limit to 5 items
      const sortedActivities = activities
        .sort((a, b) => {
          const priority = { checkin: 1, checkout: 2, booking: 3, payment: 4 };
          return priority[a.type] - priority[b.type];
        })
        .slice(0, 5);

      // If no activities, add a default system activity
      if (sortedActivities.length === 0) {
        sortedActivities.push({
          id: "system-status",
          type: "booking",
          title: "System Active",
          description: `Hotel system is running smoothly - ${stats.totalRooms} rooms available`,
          timestamp: "Now",
          icon: <CheckCircle className="text-green-600" size={16} />,
          color: "bg-green-100",
        });
      }

      setRecentActivities(sortedActivities);
    } catch (error) {
      console.error("Error fetching recent activities:", error);
    }
  };

  // Helper functions for activity display
  const getActivityIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case "checkin":
        return <LogIn className="text-green-600" size={16} />;
      case "checkout":
        return <LogOut className="text-orange-600" size={16} />;
      case "booking":
        return <Plus className="text-blue-600" size={16} />;
      case "payment":
        return <DollarSign className="text-purple-600" size={16} />;
      default:
        return <CheckCircle className="text-gray-600" size={16} />;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type.toLowerCase()) {
      case "checkin":
        return "bg-green-100";
      case "checkout":
        return "bg-orange-100";
      case "booking":
        return "bg-blue-100";
      case "payment":
        return "bg-purple-100";
      default:
        return "bg-gray-100";
    }
  };

  // Quick action handlers
  const handleNewBooking = () => {
    toast.info("Redirecting to reservations...");
    navigate("/reservations");
  };

  const handleCheckIn = () => {
    toast.info("Redirecting to reservations for check-in...");
    navigate("/reservations");
  };

  const handleProcessPayment = () => {
    toast.info("Redirecting to billing...");
    navigate("/billing");
  };

  const occupancyRate =
    stats.totalRooms > 0
      ? ((stats.occupiedRooms / stats.totalRooms) * 100).toFixed(1)
      : "0";

  const statCards = [
    {
      title: "Total Rooms",
      value: stats.totalRooms,
      icon: <Hotel className="text-primary-600" size={24} />,
      bgColor: "bg-primary-50",
      change: null,
    },
    {
      title: "Occupied Rooms",
      value: stats.occupiedRooms,
      icon: <Calendar className="text-green-600" size={24} />,
      bgColor: "bg-green-50",
      subtitle: `${occupancyRate}% occupancy`,
    },
    {
      title: "Today's Check-ins",
      value: stats.todayCheckIns,
      icon: <Users className="text-blue-600" size={24} />,
      bgColor: "bg-blue-50",
    },
    {
      title: "Today's Check-outs",
      value: stats.todayCheckOuts,
      icon: <Users className="text-purple-600" size={24} />,
      bgColor: "bg-purple-50",
    },
    {
      title: "Monthly Revenue",
      value: `LKR ${stats.monthlyRevenue.toLocaleString()}`,
      icon: <DollarSign className="text-yellow-600" size={24} />,
      bgColor: "bg-yellow-50",
      subtitle: "This month",
    },
    {
      title: "Pending Invoices",
      value: stats.pendingInvoices,
      icon: <FileText className="text-red-600" size={24} />,
      bgColor: "bg-red-50",
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

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <>
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
                <button
                  className="btn-primary btn-lg flex items-center justify-center gap-2"
                  onClick={handleNewBooking}
                >
                  <Calendar size={20} />
                  New Booking
                </button>
                <button
                  className="btn-primary btn-lg flex items-center justify-center gap-2"
                  onClick={handleCheckIn}
                >
                  <Users size={20} />
                  Check-In Guest
                </button>
                <button
                  className="btn-primary btn-lg flex items-center justify-center gap-2"
                  onClick={handleProcessPayment}
                >
                  <DollarSign size={20} />
                  Process Payment
                </button>
              </div>
            </Card>

            {/* Recent Activity */}
            <Card title="Recent Activity">
              <div className="space-y-4">
                {recentActivities.length > 0 ? (
                  recentActivities.map((activity) => (
                    <div
                      key={activity.id}
                      className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg"
                    >
                      <div
                        className={`w-10 h-10 rounded-full ${activity.color} flex items-center justify-center`}
                      >
                        {activity.icon}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {activity.title}
                        </p>
                        <p className="text-xs text-gray-600">
                          {activity.description}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {activity.timestamp}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                    <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
                      <TrendingUp className="text-primary-600" size={20} />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">
                        No recent activity
                      </p>
                      <p className="text-xs text-gray-600">
                        {stats.todayCheckIns} check-ins and{" "}
                        {stats.todayCheckOuts} check-outs today
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </>
        )}
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
