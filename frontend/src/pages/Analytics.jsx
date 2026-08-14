import React, { useState } from 'react';
import { GlassCard } from '../components/common/GlassCard';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { REVENUE_TREND_DATA } from '../data/mockData';
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
import { Filter, Download, BarChart2, TrendingUp, PieChart, Layers, Sliders } from 'lucide-react';

export const Analytics = () => {
  const [metric, setMetric] = useState('revenue');
  const [chartType, setChartType] = useState('area');
  const [dimension, setDimension] = useState('region');

  return (
    <div className="space-y-8 pb-12">
      {/* Header & Controls Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Advanced BI Analytics Studio</h1>
          <p className="text-xs text-slate-400 mt-1">
            Multidimensional slice-and-dice queries, variance analysis, and custom visualizations.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" icon={Filter}>
            Filter Dimensions
          </Button>
          <Button variant="primary" size="sm" icon={Download}>
            Export Dataset
          </Button>
        </div>
      </div>

      {/* Control Panel Bar */}
      <GlassCard glowColor="blue" className="p-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Select Primary Metric
            </label>
            <select
              value={metric}
              onChange={(e) => setMetric(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-medium"
            >
              <option value="revenue">Net Revenue ($ USD)</option>
              <option value="target">Target Benchmark ($ USD)</option>
              <option value="margin">Gross Profit Margin (%)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Visualization Format
            </label>
            <div className="flex items-center gap-1 bg-slate-950/80 border border-slate-800 p-1 rounded-xl">
              <button
                onClick={() => setChartType('area')}
                className={`flex-1 py-1 text-xs rounded-lg font-medium transition-all ${chartType === 'area' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
              >
                Area Fill
              </button>
              <button
                onClick={() => setChartType('bar')}
                className={`flex-1 py-1 text-xs rounded-lg font-medium transition-all ${chartType === 'bar' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
              >
                Bar Columns
              </button>
              <button
                onClick={() => setChartType('line')}
                className={`flex-1 py-1 text-xs rounded-lg font-medium transition-all ${chartType === 'line' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
              >
                Line Path
              </button>
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Breakdown Dimension
            </label>
            <select
              value={dimension}
              onChange={(e) => setDimension(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-medium"
            >
              <option value="region">By Geographic Region</option>
              <option value="category">By Product Category</option>
              <option value="tier">By Enterprise Customer Tier</option>
            </select>
          </div>
        </div>
      </GlassCard>

      {/* Main Interactive Dynamic Chart */}
      <GlassCard glowColor="purple" className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-base font-bold text-white uppercase tracking-wider text-xs flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-purple-400" /> Dynamic Analytics Canvas
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Displaying 12-month aggregated telemetry</p>
          </div>
          <Badge variant="purple">Real-Time Aggregation</Badge>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            {chartType === 'area' ? (
              <AreaChart data={REVENUE_TREND_DATA}>
                <defs>
                  <linearGradient id="mainGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Area type="monotone" dataKey={metric} stroke="#8b5cf6" strokeWidth={3} fill="url(#mainGrad)" />
              </AreaChart>
            ) : chartType === 'bar' ? (
              <BarChart data={REVENUE_TREND_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Bar dataKey={metric} fill="#3b82f6" radius={[6, 6, 0, 0]} />
              </BarChart>
            ) : (
              <LineChart data={REVENUE_TREND_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Line type="monotone" dataKey={metric} stroke="#06b6d4" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
      </GlassCard>

      {/* Detailed Analytical Breakdown Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard glowColor="blue">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-semibold uppercase">North America Market</span>
            <Badge variant="blue">+16.8% YoY</Badge>
          </div>
          <p className="text-2xl font-extrabold text-white font-mono">$2,425,000</p>
          <p className="text-xs text-slate-400 mt-1">50% total net ARR contribution</p>
        </GlassCard>

        <GlassCard glowColor="purple">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-semibold uppercase">EMEA Enterprise</span>
            <Badge variant="purple">+11.4% YoY</Badge>
          </div>
          <p className="text-2xl font-extrabold text-white font-mono">$1,358,000</p>
          <p className="text-xs text-slate-400 mt-1">28% total net ARR contribution</p>
        </GlassCard>

        <GlassCard glowColor="cyan">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-semibold uppercase">APAC & Emerging</span>
            <Badge variant="cyan">+22.5% YoY</Badge>
          </div>
          <p className="text-2xl font-extrabold text-white font-mono">$776,000</p>
          <p className="text-xs text-slate-400 mt-1">Highest growth acceleration region</p>
        </GlassCard>
      </div>
    </div>
  );
};
