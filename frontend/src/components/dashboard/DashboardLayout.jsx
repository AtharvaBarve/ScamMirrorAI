import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Shield, 
  LayoutDashboard, 
  Activity, 
  LineChart, 
  FileText, 
  Settings,
  Search,
  Bell,
  User,
  Menu,
  ChevronLeft
} from 'lucide-react';
import Input from '../ui/Input';
import Badge from '../ui/Badge';

const SidebarItem = ({ icon: Icon, label, path, isActive, isCollapsed }) => (
  <Link 
    to={path} 
    className={`flex items-center px-4 py-3 mb-1 rounded-lg transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-gray-400 hover:bg-surface hover:text-white'}`}
  >
    <Icon className={`w-5 h-5 ${isActive ? 'text-primary' : ''} ${!isCollapsed ? 'mr-3' : 'mx-auto'}`} />
    {!isCollapsed && <span className="font-medium text-sm">{label}</span>}
  </Link>
);

const DashboardLayout = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const location = useLocation();

  const navItems = [
    { icon: LayoutDashboard, label: 'Overview', path: '/dashboard' },
    { icon: Activity, label: 'Threat Feed', path: '/dashboard/feed' },
    { icon: LineChart, label: 'Trends', path: '/dashboard/trends' },
    { icon: FileText, label: 'Reports', path: '/dashboard/reports' },
    { icon: Settings, label: 'Settings', path: '/dashboard/settings' },
  ];

  return (
    <div className="flex h-screen bg-background text-white overflow-hidden">
      
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarCollapsed ? '80px' : '260px' }}
        className="flex-shrink-0 bg-surface/50 border-r border-border backdrop-blur-xl flex flex-col z-20"
      >
        <div className="h-16 flex items-center px-4 justify-between border-b border-border/50">
          <Link to="/" className="flex items-center overflow-hidden">
            <Shield className="w-8 h-8 text-primary flex-shrink-0" />
            {!isSidebarCollapsed && (
              <motion.span 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="ml-3 font-display font-bold text-xl tracking-tight whitespace-nowrap"
              >
                ScamMirror
              </motion.span>
            )}
          </Link>
        </div>

        <nav className="flex-grow p-4 overflow-y-auto">
          <div className="space-y-1">
            {navItems.map((item) => (
              <SidebarItem 
                key={item.label}
                icon={item.icon}
                label={item.label}
                path={item.path}
                isActive={location.pathname === item.path || (item.path !== '/dashboard' && location.pathname.startsWith(item.path))}
                isCollapsed={isSidebarCollapsed}
              />
            ))}
          </div>
        </nav>

        <div className="p-4 border-t border-border/50">
          <button 
            onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
            className="flex items-center justify-center w-full p-2 rounded-lg text-gray-400 hover:bg-surface hover:text-white transition-colors"
          >
            <ChevronLeft className={`w-5 h-5 transition-transform duration-300 ${isSidebarCollapsed ? 'rotate-180' : ''}`} />
          </button>
        </div>
      </motion.aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        
        {/* Topbar */}
        <header className="h-16 flex-shrink-0 bg-surface/30 backdrop-blur-md border-b border-border flex items-center justify-between px-6 z-10">
          
          {/* Mobile menu button (hidden on desktop) */}
          <button className="lg:hidden text-gray-400 hover:text-white p-2">
            <Menu className="w-6 h-6" />
          </button>

          {/* Search */}
          <div className="hidden lg:flex items-center flex-1 max-w-md">
            <div className="relative w-full">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-gray-500" />
              </div>
              <Input 
                type="text" 
                placeholder="Search IOCs, URLs, or Threat Families..." 
                className="pl-10 h-10 text-sm bg-background/50 border-border/50"
              />
            </div>
          </div>

          {/* Right Actions */}
          <div className="flex items-center space-x-4 ml-4">
            <div className="hidden md:flex items-center mr-4">
              <span className="text-xs font-mono text-gray-500 mr-2">NETWORK STATUS</span>
              <Badge variant="success" className="animate-pulse">SECURE</Badge>
            </div>
            
            <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-danger"></span>
            </button>
            
            <div className="w-px h-6 bg-border mx-2" />
            
            <button className="flex items-center space-x-2 p-1 rounded-full hover:bg-surface transition-colors">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
                <User className="w-4 h-4 text-primary" />
              </div>
            </button>
          </div>
        </header>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 relative">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
