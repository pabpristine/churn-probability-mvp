import * as React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Clock, AlertTriangle, TrendingUp, Minus } from 'lucide-react';
import { cn } from '@/utils';
import { SEED_TIMELINE, SEED_INSIGHTS, SEED_RISK_FACTORS } from '../client-details.data';
import type { KeyInsight, RiskFactor, ClientTimelineEvent } from '@/types';

// ============================================================
// ExecutiveSummaryCard
// ============================================================

function ExecutiveSummaryCard() {
  return (
    <div className="section-card p-6 bg-gradient-to-br from-primary/5 to-transparent border border-primary/20 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <Sparkles className="w-24 h-24 text-primary" />
      </div>
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-white">
            <Sparkles className="h-3.5 w-3.5" />
          </div>
          <span className="text-[13px] font-semibold text-primary uppercase tracking-wider">AI Executive Summary</span>
          <span className="text-[11px] text-muted-foreground ml-auto flex items-center gap-1">
            <Clock className="h-3 w-3" /> Generated 2 hrs ago
          </span>
        </div>
        <div className="space-y-4">
          <p className="text-[14px] leading-relaxed text-foreground/90 font-medium">
            The client is exhibiting early warning signs of budget-driven churn. While core product utilization remains exceptionally high (92%), we have detected a 15% drop in executive sponsor engagement over the last 30 days.
          </p>
          <p className="text-[14px] leading-relaxed text-muted-foreground">
            Historical vector analysis indicates an 88% similarity pattern to Vanguard Tech, who churned under identical circumstances. Immediate intervention via an Executive Business Review is highly recommended to re-establish ROI visibility before the upcoming renewal window in 90 days.
          </p>
        </div>
        <div className="mt-5 flex items-center gap-3 border-t border-border/50 pt-4">
          <div className="flex items-center gap-1.5">
            <span className="flex h-2 w-2 rounded-full bg-warning animate-pulse" />
            <span className="text-[12px] font-semibold text-warning">Medium Confidence (74%)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// KeyInsights
// ============================================================

function KeyInsights({ insights = SEED_INSIGHTS }: { insights?: KeyInsight[] }) {
  const getIcon = (type: string) => {
    if (type === 'positive') return <TrendingUp className="h-4 w-4 text-success" />;
    if (type === 'negative') return <AlertTriangle className="h-4 w-4 text-destructive" />;
    return <Minus className="h-4 w-4 text-muted-foreground" />;
  };

  return (
    <div className="section-card p-5">
      <h3 className="text-[14px] font-semibold text-foreground mb-4">Key Insights</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {insights.map((insight) => (
          <div key={insight.id} className="p-4 rounded-xl border border-border bg-secondary/30 flex gap-3">
            <div className="mt-0.5">{getIcon(insight.type)}</div>
            <div>
              <p className="text-[13px] font-semibold text-foreground leading-snug">{insight.title}</p>
              <p className="text-[12px] text-muted-foreground mt-1 leading-relaxed">{insight.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// ClientTimeline
// ============================================================

function ClientTimeline({ events = SEED_TIMELINE }: { events?: ClientTimelineEvent[] }) {
  return (
    <div className="section-card p-5">
      <h3 className="text-[14px] font-semibold text-foreground mb-4">Recent Timeline</h3>
      <div className="relative border-l border-border ml-3 space-y-6">
        {events.map((event, i) => (
          <div key={event.id} className="relative pl-6">
            <div className="absolute -left-[5px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-card bg-primary" />
            <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-1">
              <h4 className="text-[13px] font-semibold text-foreground">{event.title}</h4>
              <span className="text-[11px] text-muted-foreground tabular-nums">
                {new Date(event.date).toLocaleString()}
              </span>
            </div>
            <p className="text-[12.5px] text-muted-foreground">{event.description}</p>
            {event.author && (
              <p className="text-[11px] font-medium text-primary mt-1.5">{event.author}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// OverviewTab
// ============================================================

export function OverviewTab() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-4"
    >
      <ExecutiveSummaryCard />
      <KeyInsights />
      <ClientTimeline />
    </motion.div>
  );
}
