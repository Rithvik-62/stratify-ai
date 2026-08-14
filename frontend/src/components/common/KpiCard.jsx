import React from 'react';
import { GlassCard } from './GlassCard';
import { TrendingUp, TrendingDown, DollarSign, Users, Activity, HelpCircle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line } from 'recharts';

const ICON_MAP = {
  DollarSign,
  TrendingUp,
  Users,
  Activity,
};

export const KpiCard = ({ kpi }) => {
  const IconComponent = ICON_MAP[kpi.iconName] || Activity;
  const isPositive = kpi.isPositive;

  const sparklineData = (kpi.sparkline || [10, 20, 15, 30, 25, 40]).map((val, idx) => ({ i: idx, val }));

  const colorStyles = {
    blue: { iconBg: 'bg-blue-500/10 text-blue-400 border-blue-500/20', glow: 'blue', sparklineColor: '#3b82f6' },
    purple: { iconBg: 'bg-purple-500/10 text-purple-400 border-purple-500/20', glow: 'purple', sparklineColor: '#8b5cf6' },
    cyan: { iconBg: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20', glow: 'cyan', sparklineColor: '#06b6d4' },
    emerald: { iconBg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', glow: 'emerald', sparklineColor: '#10b981' },
  }[kpi.accentColor || 'blue'];

  return (
    <GlassCard glowColor={colorStyles.glow} className="relative overflow-hidden group">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          {kpi.label}
          <HelpCircle className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors cursor-help" />
        </span>
        <div className={`p-2.5 rounded-xl border ${colorStyles.iconBg}`}>
          <IconComponent className="w-5 h-5" />
        </div>
      </div>

      <div className="flex items-baseline justify-between mb-3">
        <div>
          <h3 className="text-2xl font-extrabold text-white tracking-tight font-mono">{kpi.value}</h3>
          <p className="text-xs text-slate-400 mt-0.5">{kpi.timeframe}</p>
        </div>

        <div className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold border ${
          isPositive
            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
            : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
        }`}>
          {isPositive ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
          <span>{kpi.change}</span>
        </div>
      </div>

      {/* Mini Sparkline Chart */}
      <div className="h-10 w-full mt-2 opacity-70 group-hover:opacity-100 transition-opacity">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={sparklineData}>
            <Line
              type="monotone"
              dataKey="val"
              stroke={colorStyles.sparklineColor}
              strokeWidth={2}
              dot={false}
              isAnimationActive={true}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </GlassCard>
  );
};
