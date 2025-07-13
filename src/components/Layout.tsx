import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Upload,
  Shield,
  UserX,
  Link as ChainIcon,
  FileText,
  QrCode,
  Activity
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload Data', href: '/upload', icon: Upload },
    { name: 'Fraud Detection', href: '/fraud-detection', icon: Shield },
    { name: 'Blocklist', href: '/blocklist', icon: UserX },
    { name: 'Blockchain Log', href: '/blockchain-log', icon: ChainIcon },
    { name: 'Reports', href: '/report', icon: FileText },
    { name: 'Receipt Verify', href: '/receipt-verification', icon: QrCode },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-walmart-blue shadow-sm border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Activity className="h-8 w-8 text-walmart-gold" />
              <h1 className="text-xl font-bold text-white">
                Walmart AI Fraud Prevention Platform
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-blue-100">Analyst Dashboard</span>
              <div className="h-8 w-8 bg-walmart-gold rounded-full flex items-center justify-center">
                <span className="text-sm font-semibold text-walmart-blue">WM</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm min-h-screen">
          <div className="p-6">
            <ul className="space-y-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-walmart-blue text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <item.icon className="h-5 w-5" />
                      <span>{item.name}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;