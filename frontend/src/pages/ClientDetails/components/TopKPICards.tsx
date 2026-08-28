import * as React from 'react';
import { Activity, ShieldAlert, Heart, TrendingUp, Target, Lightbulb } from 'lucide-react';
import { MetricCard } from '@/components/common/MetricCard';
import type { Client } from '@/types';

// ============================================================
// TopKPICards
// ============================================================

export function TopKPICards({ client }: { client: Client }) {
  // We mock some metrics for demonstration since they aren't all on the client type directly yet
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <MetricCard
        title="Health Score"
        value={`${client.healthScore}/100`}
        icon={Heart}
        iconColor={client.healthScore > 70 ? 'success' : client.healthScore > 50 ? 'warning' : 'danger'}
        trend={{ value: 5, percent: 5, period: 'vs last month', direction: 'up' }}
      />
      <MetricCard
        title="Churn Probability"
        value={`${client.churnProbability}%`}
        icon={ShieldAlert}
        iconColor={client.churnProbability > 60 ? 'danger' : client.churnProbability > 30 ? 'warning' : 'success'}
        trend={{ value: -2.4, percent: -2.4, period: 'vs AI benchmark', direction: 'down' }}
      />
      <MetricCard
        title="Revenue (MRR)"
        value={`$${(client.mrr / 1000).toFixed(1)}k`}
        icon={TrendingUp}
        iconColor="primary"
        trend={{ value: 12, percent: 12, period: 'YoY growth', direction: 'up' }}
      />
      <MetricCard
        title="Engagement Score"
        value="88"
        icon={Activity}
        iconColor="info"
        trend={{ value: -15, percent: -15, period: 'vs last quarter', direction: 'down' }}
      />
      <MetricCard
        title="Campaign ROI"
        value="142%"
        icon={Target}
        iconColor="success"
        trend={{ value: 8, percent: 8, period: 'vs expected', direction: 'up' }}
      />
      <MetricCard
        title="Active Recs"
        value="3"
        icon={Lightbulb}
        iconColor="warning"
      />
    </div>
  );
}
