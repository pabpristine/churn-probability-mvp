import * as React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, BarChart2 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { SEED_KPIS, SEED_TREND } from '../client-details.data';
import type { KPI, TrendInterpretation } from '@/types';
import { cn } from '@/utils';

// ============================================================
// Shared Tooltip
// ============================================================

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="section-card px-3 py-2.5 shadow-lg text-[12px]">
      {label && <p className="font-semibold text-foreground mb-1">{label}</p>}
      {payload.map((entry: any) => (
        <div key={entry.name} className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full flex-shrink-0" style={{ backgroundColor: entry.color }} />
          <span className="text-muted-foreground">{entry.name}:</span>
          <span className="font-semibold text-foreground">{entry.value}</span>
        </div>
      ))}
    </div>
  );
}

// ============================================================
// AnalyticsCharts
// ============================================================

function AnalyticsCharts({ kpis = SEED_KPIS }: { kpis?: (KPI & { history: any[] })[] }) {
  // Extract history for a sample area chart (Adoption)
  const adoptionKpi = kpis.find(k => k.name === 'Product Adoption');
  const adoptionData = adoptionKpi?.history || [];

  // Data for Radar
  const radarData = kpis.map(k => ({ subject: k.name, value: k.value, fullMark: 100 }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {/* Area Chart */}
      <div className="section-card p-5">
        <h3 className="text-[14px] font-semibold text-foreground mb-4">Adoption Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={adoptionData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(221,83%,53%)" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="hsl(221,83%,53%)" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
            <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }} />
            <Tooltip content={<ChartTooltip />} />
            <Area type="monotone" dataKey="value" stroke="hsl(221,83%,53%)" strokeWidth={2} fillOpacity={1} fill="url(#colorValue)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Radar Chart */}
      <div className="section-card p-5">
        <h3 className="text-[14px] font-semibold text-foreground mb-4">KPI Performance Matrix</h3>
        <ResponsiveContainer width="100%" height={250}>
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
            <PolarGrid stroke="hsl(var(--border))" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
            <Radar name="Score" dataKey="value" stroke="hsl(221,83%,53%)" fill="hsl(221,83%,53%)" fillOpacity={0.2} />
            <Tooltip content={<ChartTooltip />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// ============================================================
// TrendInterpretationCard
// ============================================================

function TrendInterpretationCard({ trend = SEED_TREND }: { trend?: TrendInterpretation }) {
  return (
    <div className="section-card p-5 bg-card border-border">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="h-4 w-4 text-primary" />
        <h3 className="text-[14px] font-semibold text-foreground">AI Trend Interpretation</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <p className="text-[11.5px] font-semibold uppercase text-muted-foreground mb-1">Detected Pattern</p>
          <p className="text-[15px] font-bold text-foreground mb-4">{trend.detectedTrend}</p>
          
          <p className="text-[11.5px] font-semibold uppercase text-muted-foreground mb-1">Business Context</p>
          <p className="text-[13px] text-muted-foreground leading-relaxed">{trend.businessInterpretation}</p>
        </div>
        
        <div className="space-y-4">
          <div>
            <p className="text-[11.5px] font-semibold uppercase text-muted-foreground mb-1">Possible Causes</p>
            <ul className="list-disc pl-4 space-y-1">
              {trend.possibleCauses.map((cause, i) => (
                <li key={i} className="text-[13px] text-muted-foreground">{cause}</li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-[11.5px] font-semibold uppercase text-muted-foreground mb-1">Historical Comparison</p>
            <p className="text-[13px] font-medium text-warning">{trend.historicalComparison}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// KPIAnalyticsTab
// ============================================================

export function KPIAnalyticsTab() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-4"
    >
      <TrendInterpretationCard />
      <AnalyticsCharts />
    </motion.div>
  );
}
