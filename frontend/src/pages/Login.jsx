import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Layers, ArrowRight, Lock, Mail, ShieldCheck, Sparkles } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Login = () => {
  const [email, setEmail] = useState('executive@stratify.ai');
  const [password, setPassword] = useState('••••••••••••');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col justify-center items-center p-4 relative overflow-hidden">
      {/* Background ambient lighting effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600/15 rounded-full blur-[140px] pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-10 right-1/4 w-[400px] h-[400px] bg-purple-600/15 rounded-full blur-[140px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md bg-slate-900/80 backdrop-blur-2xl border border-slate-800 rounded-3xl p-8 shadow-2xl relative z-10"
      >
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 p-0.5 shadow-xl shadow-blue-500/20 mb-4">
            <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
              <Layers className="w-7 h-7 text-blue-400" />
            </div>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight gradient-text-blue-purple font-sans">
            Stratify AI Enterprise
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Sign in to access your Executive Business Intelligence Workspaces
          </p>
        </div>

        {/* Demo Fast Track Pill */}
        <div className="mb-6 p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-center">
          <p className="text-xs text-blue-300 font-medium flex items-center justify-center gap-1.5 mb-2">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" /> Instant Executive Demo Access
          </p>
          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('/')}
            className="w-full shadow-md"
          >
            Launch Executive Workspace <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>

        <div className="relative my-6 text-center">
          <hr className="border-slate-800" />
          <span className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-slate-900 px-3 text-[10px] uppercase tracking-wider text-slate-500 font-mono">
            or sign in with credentials
          </span>
        </div>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Enterprise Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-slate-950/60 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-slate-950/60 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono"
              />
            </div>
          </div>

          <div className="flex items-center justify-between text-xs text-slate-400">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" defaultChecked className="rounded border-slate-700 bg-slate-800 text-blue-500 focus:ring-0" />
              Remember device
            </label>
            <a href="#forgot" className="text-blue-400 hover:text-blue-300">Single Sign-On SSO</a>
          </div>

          <Button type="submit" variant="secondary" className="w-full py-2.5 mt-2">
            Sign In with SSO / SAML
          </Button>
        </form>

        <div className="mt-8 text-center border-t border-slate-800/80 pt-4 flex items-center justify-center gap-2 text-xs text-slate-500">
          <ShieldCheck className="w-4 h-4 text-emerald-400" /> SOC2 Type II Certified & ISO 27001 Secured
        </div>
      </motion.div>
    </div>
  );
};
