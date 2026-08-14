import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  LineChart,
  Sparkles,
  FileSpreadsheet,
  Settings,
  LogIn,
  ChevronLeft,
  ChevronRight,
  Layers,
  Database,
  Building2,
  CheckCircle,
} from 'lucide-react';
import { motion } from 'framer-motion';

export const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Upload Data', path: '/upload', icon: UploadCloud },
    { label: 'Analytics', path: '/analytics', icon: LineChart },
    { label: 'AI Insights', path: '/ai-insights', icon: Sparkles, badge: 'AI Live' },
    { label: 'Reports', path: '/reports', icon: FileSpreadsheet },
    { label: 'Settings', path: '/settings', icon: Settings },
    { label: 'Login', path: '/login', icon: LogIn, secondary: true },
  ];

  return (
    <aside
      className={`
        sticky top-0 h-screen bg-slate-900/90 backdrop-blur-2xl border-r border-slate-800/80
        transition-all duration-300 z-40 flex flex-col justify-between select-none shrink-0
        ${collapsed ? 'w-20' : 'w-64'}
      `}
    >
      <div>
        {/* Logo & Brand Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-800/80">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 p-0.5 shadow-lg shadow-blue-500/20 shrink-0">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Layers className="w-5 h-5 text-blue-400" />
              </div>
            </div>
            {!collapsed && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col">
                <span className="font-extrabold text-lg tracking-tight gradient-text-blue-purple font-sans">
                  Stratify<span className="text-white ml-0.5">AI</span>
                </span>
                <span className="text-[10px] text-slate-400 font-semibold tracking-wider uppercase">
                  Enterprise BI v4.2
                </span>
              </motion.div>
            )}
          </div>

          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Workspace Switcher */}
        {!collapsed && (
          <div className="mx-3 my-3 p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <Building2 className="w-4 h-4 text-purple-400 shrink-0" />
              <div className="truncate">
                <p className="text-xs font-semibold text-white truncate">Acme Global Enterprise</p>
                <p className="text-[10px] text-slate-400 flex items-center gap-1">
                  <Database className="w-3 h-3 text-emerald-400 inline" /> Snowflake Prod
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Items */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={`
                  relative flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group
                  ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600/20 to-purple-600/20 text-white border border-blue-500/30 shadow-md shadow-blue-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }
                `}
              >
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-blue-400' : 'group-hover:text-slate-200'}`} />

                {!collapsed && (
                  <span className="truncate flex-1">{item.label}</span>
                )}

                {!collapsed && item.badge && (
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 animate-pulse">
                    {item.badge}
                  </span>
                )}

                {isActive && (
                  <motion.div
                    layoutId="sidebarActiveIndicator"
                    className="absolute left-0 top-2 bottom-2 w-1 bg-gradient-to-b from-blue-400 to-purple-500 rounded-r-full"
                  />
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* User Profile Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/40">
        <div className="flex items-center gap-3">
          <div className="relative shrink-0">
            <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 p-0.5">
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
                alt="Executive Avatar"
                className="w-full h-full rounded-full object-cover"
              />
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-500 border-2 border-slate-900 rounded-full" />
          </div>

          {!collapsed && (
            <div className="flex-1 truncate">
              <p className="text-xs font-semibold text-white truncate flex items-center gap-1">
                Alex Morgan <CheckCircle className="w-3 h-3 text-blue-400 inline" />
              </p>
              <p className="text-[10px] text-slate-400 truncate">Chief Data Officer</p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};
