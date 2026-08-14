import React, { useState } from 'react';
import { GlassCard } from '../components/common/GlassCard';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { MOCK_REPORTS } from '../data/mockData';
import { FileSpreadsheet, Download, Calendar, Plus, Clock, FileText, CheckCircle2 } from 'lucide-react';

export const Reports = () => {
  const [reports, setReports] = useState(MOCK_REPORTS);
  const [downloadMsg, setDownloadMsg] = useState('');

  const triggerExport = (title) => {
    setDownloadMsg(`Generating & downloading ${title}...`);
    setTimeout(() => setDownloadMsg(''), 2500);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Executive Report Hub & Automation</h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated PDF briefings, Excel workbench exports, and board presentation decks.
          </p>
        </div>

        <Button variant="primary" size="sm" icon={Plus}>
          Schedule New Report
        </Button>
      </div>

      {downloadMsg && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-2 animate-pulse">
          <CheckCircle2 className="w-4 h-4" /> {downloadMsg}
        </div>
      )}

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reports.map((report) => (
          <GlassCard key={report.id} glowColor="blue" className="flex flex-col justify-between p-6">
            <div>
              <div className="flex items-center justify-between mb-3">
                <Badge variant="purple">{report.category}</Badge>
                <span className="text-[11px] text-slate-500 font-mono flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {report.schedule}
                </span>
              </div>

              <h3 className="text-base font-bold text-white mb-1 flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-400" /> {report.title}
              </h3>
              <p className="text-xs text-slate-400">
                Format: <span className="text-slate-200 font-medium">{report.format}</span> • Owner: {report.owner}
              </p>
            </div>

            <div className="pt-4 mt-6 border-t border-slate-800 flex items-center justify-between">
              <span className="text-[11px] text-slate-500">Last Generated: {report.lastGenerated}</span>
              <Button
                variant="secondary"
                size="sm"
                icon={Download}
                onClick={() => triggerExport(report.title)}
              >
                Download Export
              </Button>
            </div>
          </GlassCard>
        ))}
      </div>

      {/* Scheduled Automation Hub */}
      <GlassCard glowColor="purple">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Calendar className="w-4 h-4 text-purple-400" /> Automated Distribution Schedule
            </h2>
            <p className="text-xs text-slate-400">Configured Slack, Email, and S3 bucket export triggers</p>
          </div>
          <Badge variant="emerald">3 Active Automation Triggers</Badge>
        </div>

        <div className="space-y-3">
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs">
            <div>
              <span className="font-bold text-white">Monday 08:00 AM Executive Briefing</span>
              <p className="text-slate-400">Delivers PDF to executive-team@stratify.ai</p>
            </div>
            <Badge variant="emerald">Active</Badge>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs">
            <div>
              <span className="font-bold text-white">Daily 06:00 UTC Infrastructure Audit</span>
              <p className="text-slate-400">Pushes CSV to AWS S3 s3://stratify-reports-prod/</p>
            </div>
            <Badge variant="emerald">Active</Badge>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};
