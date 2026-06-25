
import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Shield, Cloud, Server, AlertTriangle, BarChart3, Bell, Search, Menu } from 'lucide-react';
import { useAuthStore } from '@/stores/useAuthStore';
import { useTheme } from '@/themes/ThemeProvider';

const navigation = [
  { name: 'SOC Dashboard', href: '/soc', icon: Shield, permission: 'soc.read' },
  { name: 'ASM Core', href: '/asm', icon: LayoutDashboard, permission: 'asset.read' },
  { name: 'Threat Intel', href: '/threat', icon: AlertTriangle, permission: 'threat.read' },
  { name: 'Cloud Intel', href: '/cloud', icon: Cloud, permission: 'cloud.read' },
  { name: 'Infrastructure', href: '/infra', icon: Server, permission: 'infra.read' },
  { name: 'Executive', href: '/executive', icon: BarChart3, permission: 'executive.read' },
];

export function EnterpriseLayout() {
  const { hasPermission } = useAuthStore();
  const { theme, setTheme } = useTheme();

  const filteredNav = navigation.filter(item => hasPermission(item.permission));

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 border-r border-border bg-card hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-border">
          <Shield className="w-8 h-8 text-primary" />
          <span className="ml-3 text-xl font-bold tracking-tight">ReconX</span>
        </div>
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {filteredNav.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
                }`
              }
            >
              <item.icon className="mr-3 flex-shrink-0 h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-16 flex-shrink-0 border-b border-border bg-card flex items-center justify-between px-6">
          <div className="flex items-center flex-1">
            <button className="md:hidden p-2 text-muted-foreground hover:text-foreground">
              <Menu className="w-6 h-6" />
            </button>
            <div className="max-w-md w-full ml-4 hidden md:flex items-center relative">
              <Search className="w-4 h-4 absolute left-3 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Search assets, incidents, IOCs..." 
                className="w-full pl-10 pr-4 py-2 bg-secondary border-none rounded-md text-sm focus:ring-1 focus:ring-primary outline-none"
              />
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2 rounded-full hover:bg-secondary text-muted-foreground"
            >
              {theme === 'dark' ? '🌞' : '🌙'}
            </button>
            <button className="p-2 rounded-full hover:bg-secondary text-muted-foreground relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full"></span>
            </button>
            <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center text-primary font-bold text-sm">
              AD
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-6 bg-background">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
