import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  EXECUTIVE_KPIS,
  REVENUE_TREND_DATA,
  MONTHLY_SALES_DATA,
  REGIONAL_SALES_DATA,
  INVENTORY_STATUS_DATA,
  CUSTOMER_GROWTH_DATA,
  TOP_PRODUCTS_DATA,
  RECENT_ALERTS,
  BUSINESS_HEALTH_SCORE,
  AI_RECOMMENDATIONS,
} from '../data/mockData';
import { KpiCard } from '../components/common/KpiCard';
import { GlassCard } from '../components/common/GlassCard';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import {
  Sparkles,
  ArrowUpRight,
  ShieldAlert,
  Globe,
  Package,
  TrendingUp,
  Search,
  CheckCircle,
  Activity,
  Zap,
  Download,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
  const [productSearch, setProductSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const navigate = useNavigate();

  const filteredProducts = TOP_PRODUCTS_DATA.filter((p) => {
    const matchesSearch = p.name.toLowerCase().includes(productSearch.toLowerCase());
    const matchesCat = selectedCategory === 'All' || p.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="space-y-8 pb-12">
      {/* 1. Welcome Banner */}
      <GlassCard glowColor="purple" className="relative overflow-hidden border-purple-500/20">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-purple-600/10 via-blue-600/10 to-transparent pointer-events-none" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="purple" className="animate-pulse">Live Executive Telemetry</Badge>
              <span className="text-xs text-slate-400 font-mono">Synced 2 minutes ago</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Welcome back, <span className="gradient-text-blue-purple">Alex Morgan</span>
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Stratify AI Engine has synthesized Q3 enterprise performance. Overall Business Health score is <strong className="text-emerald-400">92/100 (Exceptional)</strong> with zero critical system bottlenecks.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <Button variant="outline" size="sm" icon={Download}>
              Export Executive Deck
            </Button>
            <Button variant="primary" size="sm" icon={Sparkles} onClick={() => navigate('/ai-insights')}>
              Launch AI Synthesis
            </Button>
          </div>
        </div>
      </GlassCard>

      {/* 2. Executive KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {EXECUTIVE_KPIS.map((kpi) => (
          <KpiCard key={kpi.id} kpi={kpi} />
        ))}
      </div>

      {/* 3. Main Financial Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Trend Chart (2 cols) */}
        <GlassCard glowColor="blue" className="lg:col-span-2 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                Revenue Trajectory & Target Forecast
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Monthly revenue run-rate vs baseline enterprise target ($ USD)
              </p>
            </div>
            <Badge variant="blue">FY 2026 Target: $9.5M</Badge>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={REVENUE_TREND_DATA} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="targetGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickFormatter={(val) => `$${val / 1000}k`} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  formatter={(value) => [`$${value.toLocaleString()}`, 'Amount']}
                />
                <Area type="monotone" dataKey="revenue" name="Actual Revenue" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#revenueGrad)" />
                <Area type="monotone" dataKey="target" name="Target Target" stroke="#8b5cf6" strokeWidth={2} strokeDasharray="4 4" fillOpacity={1} fill="url(#targetGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        {/* Monthly Sales Breakdown Chart (1 col) */}
        <GlassCard glowColor="purple">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-base font-bold text-white">Sales Segment Mix</h2>
              <p className="text-xs text-slate-400 mt-0.5">Enterprise vs Mid-Market vs SMB deal volume</p>
            </div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={MONTHLY_SALES_DATA} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Bar dataKey="enterprise" name="Enterprise" fill="#3b82f6" radius={[4, 4, 0, 0]} stackId="a" />
                <Bar dataKey="midMarket" name="Mid-Market" fill="#8b5cf6" radius={[4, 4, 0, 0]} stackId="a" />
                <Bar dataKey="smb" name="SMB" fill="#06b6d4" radius={[4, 4, 0, 0]} stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      {/* 4. AI Recommendation Card & Business Health Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* AI Recommendation Engine Card (2 cols) */}
        <GlassCard glowColor="cyan" className="lg:col-span-2 border-cyan-500/30 relative">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Zap className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  Stratify AI Prescriptive Engine
                </h2>
                <p className="text-xs text-slate-400">Automated machine learning insight feed</p>
              </div>
            </div>
            <Badge variant="cyan">{AI_RECOMMENDATIONS[0].confidence}</Badge>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-white">{AI_RECOMMENDATIONS[0].title}</span>
              <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                {AI_RECOMMENDATIONS[0].impact}
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {AI_RECOMMENDATIONS[0].summary}
            </p>

            <div className="pt-2 flex items-center justify-between border-t border-slate-800/80">
              <span className="text-[11px] text-slate-500 font-mono">
                Category: {AI_RECOMMENDATIONS[0].category}
              </span>
              <Button variant="purple" size="sm" icon={ArrowUpRight} onClick={() => navigate('/ai-insights')}>
                {AI_RECOMMENDATIONS[0].actionLabel}
              </Button>
            </div>
          </div>
        </GlassCard>

        {/* Business Health Score Radial / Meter (1 col) */}
        <GlassCard glowColor="emerald">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-white">Business Health Score</h2>
            <Badge variant="emerald">{BUSINESS_HEALTH_SCORE.rating}</Badge>
          </div>

          <div className="flex items-center justify-center my-4">
            <div className="relative w-32 h-32 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90">
                <circle cx="64" cy="64" r="54" stroke="#1e293b" strokeWidth="10" fill="transparent" />
                <circle
                  cx="64"
                  cy="64"
                  r="54"
                  stroke="#10b981"
                  strokeWidth="10"
                  strokeDasharray={339.29}
                  strokeDashoffset={339.29 * (1 - BUSINESS_HEALTH_SCORE.overallScore / 100)}
                  strokeLinecap="round"
                  fill="transparent"
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-3xl font-extrabold text-white font-mono">{BUSINESS_HEALTH_SCORE.overallScore}</span>
                <span className="text-[10px] text-slate-400 uppercase tracking-widest">Out of 100</span>
              </div>
            </div>
          </div>

          <div className="space-y-2 mt-2">
            {BUSINESS_HEALTH_SCORE.categories.map((cat, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <span className="text-slate-400">{cat.name}</span>
                <span className="font-semibold text-slate-200 font-mono">{cat.score}%</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* 5. Regional Sales Heatmap & Inventory Operations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Regional Sales Heatmap Card */}
        <GlassCard glowColor="blue">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Globe className="w-5 h-5 text-blue-400" />
              <div>
                <h2 className="text-base font-bold text-white">Regional Geographic Breakdown</h2>
                <p className="text-xs text-slate-400">Global market share & cluster status</p>
              </div>
            </div>
            <Badge variant="blue">4 Active Continents</Badge>
          </div>

          <div className="space-y-3">
            {REGIONAL_SALES_DATA.map((reg, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{reg.region}</span>
                    <span className="text-xs text-emerald-400 font-medium">{reg.growth}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{reg.activeClients} Active Accounts • {reg.latency} latency</p>
                </div>
                <div className="text-right">
                  <span className="text-sm font-bold text-white font-mono">{reg.revenue}</span>
                  <div className="w-24 bg-slate-800 h-1.5 rounded-full mt-1.5 overflow-hidden">
                    <div className="bg-blue-500 h-full rounded-full" style={{ width: `${reg.percentage}%` }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Inventory & Infrastructure Status Card */}
        <GlassCard glowColor="purple">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Package className="w-5 h-5 text-purple-400" />
              <div>
                <h2 className="text-base font-bold text-white">Inventory & Infrastructure Status</h2>
                <p className="text-xs text-slate-400">Node capacities and service availability</p>
              </div>
            </div>
            <Badge variant="emerald">100% Operational</Badge>
          </div>

          <div className="space-y-3">
            {INVENTORY_STATUS_DATA.map((item, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
                <div>
                  <span className="text-sm font-semibold text-white">{item.sku}</span>
                  <p className="text-xs text-slate-400">{item.category} • {item.reorderPoint}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${
                    item.status === 'In Stock'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                      : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                  }`}>
                    {item.status}
                  </span>
                  <span className="text-xs font-mono text-slate-300 font-bold">{item.stockLevel}%</span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* 6. Customer Growth & Recent Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Customer Growth Trajectory Line Chart (2 cols) */}
        <GlassCard glowColor="blue" className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-400" /> Customer Active User Trajectory
              </h2>
              <p className="text-xs text-slate-400">Monthly active enterprise seat growth</p>
            </div>
            <Badge variant="blue">+70% YoY Growth</Badge>
          </div>

          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={CUSTOMER_GROWTH_DATA} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Line type="monotone" dataKey="activeUsers" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        {/* Real-time Alerts Ticker (1 col) */}
        <GlassCard glowColor="purple">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-400" /> Recent Alerts
            </h2>
            <span className="text-xs text-slate-500 font-mono">Live Audit</span>
          </div>

          <div className="space-y-3">
            {RECENT_ALERTS.map((alert) => (
              <div key={alert.id} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white">{alert.title}</span>
                  <span className="text-[10px] text-slate-500">{alert.time}</span>
                </div>
                <p className="text-slate-400">{alert.description}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* 7. Top Products Enterprise Data Table */}
      <GlassCard glowColor="blue">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-base font-bold text-white">Top Enterprise Product Revenue Contribution</h2>
            <p className="text-xs text-slate-400">Quarterly product breakdown by margin, growth, and sales volume</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Filter products..."
                value={productSearch}
                onChange={(e) => setProductSearch(e.target.value)}
                className="bg-slate-950/60 border border-slate-800 rounded-xl py-1.5 pl-9 pr-3 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
              />
            </div>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-slate-950/60 border border-slate-800 rounded-xl py-1.5 px-3 text-xs text-slate-200 focus:outline-none"
            >
              <option value="All">All Categories</option>
              <option value="AI Analytics">AI Analytics</option>
              <option value="Integration">Integration</option>
              <option value="Security & Ops">Security & Ops</option>
              <option value="ML Models">ML Models</option>
            </select>
          </div>
        </div>

        {/* Responsive Table Grid */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Product Name</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Units Sold</th>
                <th className="py-3 px-4">Net Revenue</th>
                <th className="py-3 px-4">Margin</th>
                <th className="py-3 px-4">Growth</th>
                <th className="py-3 px-4 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredProducts.map((prod) => (
                <tr key={prod.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-semibold text-white">{prod.name}</td>
                  <td className="py-3.5 px-4 text-slate-400">{prod.category}</td>
                  <td className="py-3.5 px-4 font-mono">{prod.salesCount}</td>
                  <td className="py-3.5 px-4 font-mono font-bold text-white">{prod.revenue}</td>
                  <td className="py-3.5 px-4 font-mono text-emerald-400">{prod.margin}</td>
                  <td className="py-3.5 px-4 font-mono text-blue-400">{prod.growth}</td>
                  <td className="py-3.5 px-4 text-right">
                    <Badge variant={prod.status === 'Best Seller' ? 'purple' : 'blue'}>
                      {prod.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  );
};
