import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { LogOut, User } from "lucide-react";
import { Button } from "../common";
import SkyNestLogo from "../../assets/skynestandlogo.png";

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <img
              src={SkyNestLogo}
              alt="SkyNest Hotels Logo"
              className="h-12 sm:h-14 md:h-16 w-auto" // increase heights
            />
          </div>

          {/* User Info & Logout */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              {/* <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
                <User className="text-primary-600" size={20} />
              </div> */}
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-900">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-xs text-gray-600">{user?.userRole}</p>
              </div>
            </div>

            <Button
              variant="secondary"
              size="sm"
              onClick={handleLogout}
              icon={<LogOut size={16} />}
              className="!flex !items-center !gap-2 !rounded-lg !px-4 !py-2 !bg-primary-600 !text-white !shadow-sm hover:!bg-blue-700 hover:!shadow-md active:!scale-[.98] focus:!outline-none focus:!ring-2 focus:!ring-blue-400 focus:!ring-offset-2 transition-colors"
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
