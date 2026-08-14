import React, { useState } from 'react';
import { GlassCard } from '../components/common/GlassCard';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { DATA_SOURCES } from '../data/mockData';
import { UploadCloud, CheckCircle2, FileText, Database, Layers, ArrowRight, RefreshCw } from 'lucide-react';

export const UploadData = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [stagedFile, setStagedFile] = useState(null);

  const handleSimulatedUpload = (file) => {
    setStagedFile(file);
    setIsUploading(true);
    setUploadProgress(0);

    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          return 100;
        }
        return prev + 20;
      });
    }, 200);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Enterprise Data Ingestion & Connectors</h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload unstructured CSV/Parquet files or sync live streaming pipelines into the Stratify Lakehouse.
        </p>
      </div>

      {/* Drag & Drop Staging Card */}
      <GlassCard glowColor="blue">
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            if (e.dataTransfer.files.length > 0) {
              handleSimulatedUpload(e.dataTransfer.files[0]);
            }
          }}
          className={`
            border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-300 flex flex-col items-center justify-center cursor-pointer
            ${isDragging ? 'border-blue-400 bg-blue-500/10 scale-[1.01]' : 'border-slate-800 hover:border-slate-700 bg-slate-950/40'}
          `}
          onClick={() => handleSimulatedUpload({ name: 'Q3_Financial_Ledger_Final.parquet', size: '42.8 MB' })}
        >
          <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4 shadow-lg shadow-blue-500/10">
            <UploadCloud className="w-8 h-8" />
          </div>

          <h3 className="text-base font-bold text-white mb-1">
            Drag and drop your dataset files here
          </h3>
          <p className="text-xs text-slate-400 max-w-md mb-4">
            Supports CSV, JSON, Apache Parquet, Excel (.xlsx), and Delta Lake formats up to 5GB per dataset.
          </p>

          <Button variant="primary" size="sm">
            Browse Local Files
          </Button>

          {/* Staged file progress bar */}
          {stagedFile && (
            <div className="mt-6 w-full max-w-md bg-slate-900 border border-slate-800 p-4 rounded-xl text-left space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-400" /> {stagedFile.name}
                </span>
                <span className="font-mono text-slate-400">{uploadProgress}%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-200" style={{ width: `${uploadProgress}%` }} />
              </div>
              {uploadProgress === 100 && (
                <p className="text-[11px] text-emerald-400 flex items-center gap-1 mt-1">
                  <CheckCircle2 className="w-3.5 h-3.5 inline" /> Schema validated successfully! Ready for ingestion.
                </p>
              )}
            </div>
          )}
        </div>
      </GlassCard>

      {/* Enterprise Connectors Grid */}
      <div>
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Database className="w-5 h-5 text-purple-400" /> Connected Data Sources & Warehouses
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {DATA_SOURCES.map((source) => (
            <GlassCard key={source.id} glowColor="purple" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-2xl">{source.logo}</span>
                  <Badge variant={source.status === 'Connected' ? 'emerald' : 'neutral'}>
                    {source.status}
                  </Badge>
                </div>
                <h3 className="text-sm font-bold text-white">{source.name}</h3>
                <p className="text-xs text-slate-400 mt-0.5">{source.type}</p>
              </div>

              <div className="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <div>
                  <span className="text-slate-500 font-mono text-[10px]">Sync Status:</span>
                  <p className="font-semibold text-slate-300">{source.sync}</p>
                </div>
                <Button variant="ghost" size="sm" icon={RefreshCw}>
                  Configure
                </Button>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>

      {/* Live Data Schema & Ingestion Preview */}
      <GlassCard glowColor="cyan">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" /> Live Ingestion Staging Preview
            </h2>
            <p className="text-xs text-slate-400">Inspecting 1,250 sample records from Snowflake staging tables</p>
          </div>
          <Button variant="purple" size="sm" icon={ArrowRight}>
            Commit Ingestion Pipeline
          </Button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Column Name</th>
                <th className="py-3 px-4">Inferred Type</th>
                <th className="py-3 px-4">Null Rate</th>
                <th className="py-3 px-4">Distinct Values</th>
                <th className="py-3 px-4">Health Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 text-white font-bold">account_id</td>
                <td className="py-3 px-4 text-blue-400">VARCHAR(64)</td>
                <td className="py-3 px-4 text-emerald-400">0.0%</td>
                <td className="py-3 px-4">1,428</td>
                <td className="py-3 px-4"><Badge variant="emerald">Valid Key</Badge></td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 text-white font-bold">mrr_amount</td>
                <td className="py-3 px-4 text-purple-400">DECIMAL(12,2)</td>
                <td className="py-3 px-4 text-emerald-400">0.0%</td>
                <td className="py-3 px-4">842</td>
                <td className="py-3 px-4"><Badge variant="emerald">Clean Numeric</Badge></td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 text-white font-bold">region_code</td>
                <td className="py-3 px-4 text-blue-400">VARCHAR(8)</td>
                <td className="py-3 px-4 text-emerald-400">0.2%</td>
                <td className="py-3 px-4">4</td>
                <td className="py-3 px-4"><Badge variant="blue">Categorical</Badge></td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 text-white font-bold">contract_start_date</td>
                <td className="py-3 px-4 text-amber-400">TIMESTAMP_TZ</td>
                <td className="py-3 px-4 text-emerald-400">0.0%</td>
                <td className="py-3 px-4">365</td>
                <td className="py-3 px-4"><Badge variant="emerald">Valid Date</Badge></td>
              </tr>
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  );
};
