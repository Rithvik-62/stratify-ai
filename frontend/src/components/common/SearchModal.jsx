import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, BarChart2, Layers, Cpu, FileText, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const SearchModal = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        isOpen ? onClose() : null;
      }
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const searchItems = [
    { title: 'Executive Overview Dashboard', path: '/', category: 'Dashboards', icon: BarChart2 },
    { title: 'Q3 Enterprise Revenue Trends', path: '/analytics', category: 'Analytics', icon: BarChart2 },
    { title: 'Stratify Copilot AI Chat', path: '/ai-insights', category: 'AI Assistant', icon: Cpu },
    { title: 'Data Pipeline Staging (Snowflake)', path: '/upload', category: 'Data Operations', icon: Layers },
    { title: 'Weekly Financial Briefing PDF', path: '/reports', category: 'Reports', icon: FileText },
  ];

  const filtered = searchItems.filter(item =>
    item.title.toLowerCase().includes(query.toLowerCase()) ||
    item.category.toLowerCase().includes(query.toLowerCase())
  );

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-slate-950/80 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden"
        >
          {/* Input Header */}
          <div className="flex items-center px-4 py-3.5 border-b border-slate-800 gap-3">
            <Search className="w-5 h-5 text-blue-400 shrink-0" />
            <input
              type="text"
              autoFocus
              placeholder="Search reports, metrics, datasets, AI queries..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-transparent text-slate-100 placeholder-slate-500 focus:outline-none text-sm font-sans"
            />
            <button
              onClick={onClose}
              className="p-1 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Results List */}
          <div className="p-2 max-h-80 overflow-y-auto space-y-1">
            {filtered.length > 0 ? (
              filtered.map((item, idx) => {
                const ItemIcon = item.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      navigate(item.path);
                      onClose();
                    }}
                    className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-800/80 text-left transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-slate-800 text-blue-400 group-hover:bg-blue-600/20">
                        <ItemIcon className="w-4 h-4" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-slate-200 group-hover:text-white">{item.title}</div>
                        <div className="text-xs text-slate-500">{item.category}</div>
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-blue-400 group-hover:translate-x-1 transition-all" />
                  </button>
                );
              })
            ) : (
              <div className="p-8 text-center text-slate-500 text-sm">
                No matching reports or datasets found for "{query}".
              </div>
            )}
          </div>

          <div className="px-4 py-2.5 bg-slate-950/60 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-500">
            <span>Press <kbd className="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300 font-mono">ESC</kbd> to close</span>
            <span>Stratify Search Index v4.2</span>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
