import React, { useState } from 'react';
import {
  Search,
  Bell,
  Calendar,
  RefreshCw,
  Sparkles,
  SlidersHorizontal,
  ChevronDown,
} from 'lucide-react';
import { Button } from '../common/Button';
import { SearchModal } from '../common/SearchModal';
import { NotificationsModal } from '../common/NotificationsModal';
import { useNavigate } from 'react-router-dom';

export const Navbar = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isNotifyOpen, setIsNotifyOpen] = useState(false);
  const [dateRange, setDateRange] = useState('This Quarter (Q3)');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const navigate = useNavigate();

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 800);
  };

  return (
    <>
      <header className="sticky top-0 z-30 h-16 bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/80 px-6 flex items-center justify-between">
        {/* Left: Quick Search Bar */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setIsSearchOpen(true)}
            className="flex items-center gap-3 px-3.5 py-2 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-slate-200 transition-all text-xs w-64 md:w-80 group shadow-inner"
          >
            <Search className="w-4 h-4 text-slate-500 group-hover:text-blue-400" />
            <span className="flex-1 text-left">Search metrics, reports, datasets...</span>
            <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-slate-800 border border-slate-700 rounded text-slate-400">
              ⌘K
            </kbd>
          </button>
        </div>

        {/* Right Action Tools */}
        <div className="flex items-center gap-3">
          {/* Quick Date Range Filter */}
          <div className="relative hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-950/50 border border-slate-800 text-xs text-slate-300">
            <Calendar className="w-3.5 h-3.5 text-blue-400" />
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer pr-4"
            >
              <option value="Last 7 Days" className="bg-slate-900">Last 7 Days</option>
              <option value="Last 30 Days" className="bg-slate-900">Last 30 Days</option>
              <option value="This Quarter (Q3)" className="bg-slate-900">This Quarter (Q3)</option>
              <option value="Year to Date (YTD)" className="bg-slate-900">Year to Date (YTD)</option>
            </select>
          </div>

          {/* Refresh Button */}
          <button
            onClick={handleRefresh}
            title="Refresh live metrics"
            className="p-2 rounded-xl bg-slate-950/50 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-blue-400' : ''}`} />
          </button>

          {/* Notifications Button */}
          <button
            onClick={() => setIsNotifyOpen(!isNotifyOpen)}
            className="relative p-2 rounded-xl bg-slate-950/50 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-all"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-blue-500 animate-ping" />
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-blue-500" />
          </button>

          {/* AI Quick Assistant Trigger */}
          <Button
            variant="purple"
            size="sm"
            icon={Sparkles}
            onClick={() => navigate('/ai-insights')}
            className="hidden sm:flex"
          >
            Ask Stratify AI
          </Button>
        </div>
      </header>

      <SearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />
      <NotificationsModal isOpen={isNotifyOpen} onClose={() => setIsNotifyOpen(false)} />
    </>
  );
};
