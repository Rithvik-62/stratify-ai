import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, CheckCircle2, AlertTriangle, Info, X } from 'lucide-react';
import { RECENT_ALERTS } from '../../data/mockData';

export const NotificationsModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const getIcon = (severity) => {
    switch (severity) {
      case 'success':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-amber-400" />;
      default:
        return <Info className="w-4 h-4 text-blue-400" />;
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex justify-end p-4 pointer-events-none">
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs pointer-events-auto" onClick={onClose} />
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          className="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden pointer-events-auto mt-14 h-fit max-h-[85vh] flex flex-col"
        >
          <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800 bg-slate-900/90">
            <div className="flex items-center gap-2">
              <Bell className="w-4 h-4 text-blue-400" />
              <h3 className="font-semibold text-white text-sm">System Notifications</h3>
              <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-400">4 New</span>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800">
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="p-4 overflow-y-auto space-y-3">
            {RECENT_ALERTS.map((alert) => (
              <div
                key={alert.id}
                className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/50 hover:border-slate-600 transition-colors flex gap-3"
              >
                <div className="mt-0.5 shrink-0">{getIcon(alert.severity)}</div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-white">{alert.title}</span>
                    <span className="text-[10px] text-slate-500 font-mono">{alert.time}</span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1">{alert.description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="p-3 bg-slate-950/80 border-t border-slate-800 text-center">
            <button onClick={onClose} className="text-xs text-blue-400 hover:text-blue-300 font-medium">
              Mark all as read
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
