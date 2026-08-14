import React, { useState } from 'react';
import { GlassCard } from '../components/common/GlassCard';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { SAMPLE_AI_CONVERSATION } from '../data/mockData';
import { Sparkles, Send, Bot, User, ArrowUpRight, Zap, RefreshCw, BarChart2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

export const AIInsights = () => {
  const [messages, setMessages] = useState(SAMPLE_AI_CONVERSATION);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const promptSuggestions = [
    'Summarize Q3 gross margin anomalies',
    'Forecast next quarter churn risk by region',
    'Compare Enterprise vs Mid-Market LTV',
    'Which products have highest expansion speed?',
  ];

  const handleSend = (textToSend) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsThinking(true);

    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        sender: 'ai',
        text: `Based on automated analysis of 1.4 Billion records in Snowflake, key takeaway for "${query}": Gross margins expanded by +2.8% to 81.4% driven by higher compute efficiency in EMEA and standard pricing index adjustments on the Enterprise AI Suite.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        chartData: [
          { category: 'AI Suite', value: 84 },
          { category: 'Connector', value: 79 },
          { category: 'Detector', value: 88 },
          { category: 'Copilot', value: 82 },
        ],
      };
      setMessages((prev) => [...prev, aiResponse]);
      setIsThinking(false);
    }, 1000);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-400" /> Stratify AI Executive Copilot
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Natural language business intelligence assistant backed by LLM + RAG over your data lakehouse.
          </p>
        </div>

        <Badge variant="purple" className="self-start md:self-auto py-1 px-3">
          Model: Stratify-BI-70B v4.2 (Live)
        </Badge>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-slate-400 flex items-center gap-1 font-semibold">
          <Zap className="w-3.5 h-3.5 text-amber-400" /> Quick Prompts:
        </span>
        {promptSuggestions.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-purple-500/50 text-xs text-slate-300 hover:text-white transition-all duration-200"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Main Chat Interface */}
      <GlassCard glowColor="purple" className="min-h-[500px] flex flex-col justify-between p-6">
        {/* Messages Stream */}
        <div className="space-y-6 overflow-y-auto max-h-[550px] pr-2">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-4 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.sender === 'ai' && (
                <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 p-0.5 shrink-0 shadow-lg shadow-purple-500/20">
                  <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                    <Bot className="w-5 h-5 text-purple-400" />
                  </div>
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-4 space-y-3 text-sm ${
                  msg.sender === 'user'
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20 rounded-tr-none'
                    : 'bg-slate-950/80 border border-slate-800 text-slate-200 rounded-tl-none'
                }`}
              >
                <div className="flex items-center justify-between text-[11px] opacity-70 mb-1">
                  <span className="font-semibold">{msg.sender === 'user' ? 'Executive User' : 'Stratify AI Engine'}</span>
                  <span>{msg.timestamp}</span>
                </div>

                <p className="leading-relaxed">{msg.text}</p>

                {/* Inline Chart if returned by AI */}
                {msg.chartData && (
                  <div className="mt-4 p-3 rounded-xl bg-slate-900 border border-slate-800">
                    <div className="flex items-center justify-between mb-2 text-xs">
                      <span className="font-bold text-white flex items-center gap-1.5">
                        <BarChart2 className="w-4 h-4 text-purple-400" /> Margin Breakdown by Product (%)
                      </span>
                    </div>
                    <div className="h-40 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={msg.chartData}>
                          <XAxis dataKey="category" stroke="#64748b" fontSize={10} tickLine={false} />
                          <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                          <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-9 h-9 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                  <User className="w-5 h-5 text-slate-300" />
                </div>
              )}
            </div>
          ))}

          {isThinking && (
            <div className="flex gap-4 items-center text-xs text-purple-400 animate-pulse">
              <Bot className="w-5 h-5 animate-spin" /> Stratify AI is querying Snowflake & synthesizing response...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="mt-6 pt-4 border-t border-slate-800/80">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3 bg-slate-950/80 border border-slate-800 rounded-2xl p-2 focus-within:border-purple-500 transition-colors"
          >
            <input
              type="text"
              placeholder="Ask Stratify AI anything about revenue, margins, churn, or system metrics..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none px-3"
            />
            <Button type="submit" variant="purple" size="sm" icon={Send} disabled={!input.trim()}>
              Ask AI
            </Button>
          </form>
        </div>
      </GlassCard>
    </div>
  );
};
