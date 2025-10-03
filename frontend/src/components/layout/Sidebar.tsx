import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Calendar, 
  Users, 
  Hotel, 
  Utensils, 
  DollarSign, 
  FileText 
} from 'lucide-react';

interface NavItem {
  name: string;
  path: string;
  icon: React.ReactNode;
  roles?: string[];
}

const navigation: NavItem[] = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: <LayoutDashboard size={20} />,
  },
  {
    name: 'Reservations',
    path: '/reservations',
    icon: <Calendar size={20} />,
  },
  {
    name: 'Guests',
    path: '/guests',
    icon: <Users size={20} />,
  },
  {
    name: 'Rooms',
    path: '/rooms',
    icon: <Hotel size={20} />,
  },
  {
    name: 'Services',
    path: '/services',
    icon: <Utensils size={20} />,
  },
  {
    name: 'Billing',
    path: '/billing',
    icon: <DollarSign size={20} />,
  },
  {
    name: 'Reports',
    path: '/reports',
    icon: <FileText size={20} />,
    roles: ['Admin', 'Manager'],
  },
];

const Sidebar = () => {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-4rem)] sticky top-16">
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-50'
              }`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;