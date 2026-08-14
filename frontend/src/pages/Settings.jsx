import React, { useState } from 'react';
import { GlassCard } from '../components/common/GlassCard';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Settings as SettingsIcon, Key, Users, Shield, Bell, CheckCircle2, Copy } from 'lucide-react';

export const Settings = () => {
  const [copiedKey, setCopiedKey] = useState(false);
  const [activeTab, setActiveTab] = useState('team');

  const teamMembers = [
    { name: 'Alex Morgan', email: 'alex.morgan@stratify.ai', role: 'Owner / CDO', status: 'Active' },
    { name: 'Sarah Jenkins', email: 'sarah.j@stratify.ai', role: 'Admin / VP Engineering', status: 'Active' },
    { name: 'David Chen', email: 'david.c@stratify.ai', role: 'Analyst Lead', status: 'Active' },
    { name: 'Emma Watson', email: 'emma.w@stratify.ai', role: 'Viewer (Executive Board)', status: 'Active' },
  ];

  const handleCopyKey = () => {
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Enterprise Organization Settings</h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage team RBAC permissions, API tokens, security standards, and platform preferences.
        </p>
      </div>

      {/* Settings Tab Navigation Bar */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
        <button
          onClick={() => setActiveTab('team')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'team' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Users className="w-4 h-4" /> Team & Permissions
        </button>

        <button
          onClick={() => setActiveTab('api')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'api' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Key className="w-4 h-4" /> API Keys & Webhooks
        </button>

        <button
          onClick={() => setActiveTab('security')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'security' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Shield className="w-4 h-4" /> Security & Compliance
        </button>
      </div>

      {/* Tab Content 1: Team & Permissions */}
      {activeTab === 'team' && (
        <GlassCard glowColor="blue">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-base font-bold text-white">Team Members & Role-Based Access Control (RBAC)</h2>
              <p className="text-xs text-slate-400 mt-0.5">Manage user roles across workspace environments</p>
            </div>
            <Button variant="primary" size="sm">Invite Member</Button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">User Name</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Workspace Role</th>
                  <th className="py-3 px-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {teamMembers.map((member, i) => (
                  <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-white">{member.name}</td>
                    <td className="py-3.5 px-4 text-slate-400 font-mono">{member.email}</td>
                    <td className="py-3.5 px-4"><Badge variant="purple">{member.role}</Badge></td>
                    <td className="py-3.5 px-4 text-right"><Badge variant="emerald">{member.status}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      )}

      {/* Tab Content 2: API Keys & Webhooks */}
      {activeTab === 'api' && (
        <GlassCard glowColor="purple">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-white">Enterprise Live Production API Key</h2>
              <p className="text-xs text-slate-400">Use this token to authenticate programmatic GraphQL/REST queries</p>
            </div>
            <Button variant="outline" size="sm">Roll Key</Button>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between font-mono text-xs text-slate-300">
            <span>st_live_sk_94827018a7b3c2918e9f4a5b</span>
            <button
              onClick={handleCopyKey}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-blue-400 transition-colors text-xs font-sans"
            >
              {copiedKey ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              {copiedKey ? 'Copied!' : 'Copy Key'}
            </button>
          </div>
        </GlassCard>
      )}

      {/* Tab Content 3: Security & Compliance */}
      {activeTab === 'security' && (
        <GlassCard glowColor="cyan" className="space-y-4">
          <h2 className="text-base font-bold text-white">Security & Audit Policies</h2>
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3 text-xs">
            <div className="flex items-center justify-between">
              <div>
                <span className="font-bold text-white">Enforce Mandatory Single Sign-On (SSO / Okta / Azure AD)</span>
                <p className="text-slate-400">Require MFA and SAML authentication for all workspace members</p>
              </div>
              <input type="checkbox" defaultChecked className="toggle cursor-pointer" />
            </div>
            <hr className="border-slate-800" />
            <div className="flex items-center justify-between">
              <div>
                <span className="font-bold text-white">SOC2 Compliance Audit Trail Logs</span>
                <p className="text-slate-400">Automatically stream all query logs to Datadog / CloudWatch</p>
              </div>
              <input type="checkbox" defaultChecked className="toggle cursor-pointer" />
            </div>
          </div>
        </GlassCard>
      )}
    </div>
  );
};
