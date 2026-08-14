import React from 'react';
import { motion } from 'framer-motion';

export const GlassCard = ({ children, className = '', hover = true, glowColor = 'blue', ...props }) => {
  const glowMap = {
    blue: 'hover:border-blue-500/40 hover:shadow-[0_0_25px_-5px_rgba(59,130,246,0.2)]',
    purple: 'hover:border-purple-500/40 hover:shadow-[0_0_25px_-5px_rgba(139,92,246,0.2)]',
    cyan: 'hover:border-cyan-500/40 hover:shadow-[0_0_25px_-5px_rgba(6,182,212,0.2)]',
    emerald: 'hover:border-emerald-500/40 hover:shadow-[0_0_25px_-5px_rgba(16,185,129,0.2)]',
    none: '',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut' }}
      className={`
        bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-5 text-slate-100
        transition-all duration-300
        ${hover ? `${glowMap[glowColor] || glowMap.blue}` : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </motion.div>
  );
};
