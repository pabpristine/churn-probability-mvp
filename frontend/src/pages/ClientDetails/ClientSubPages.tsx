import * as React from 'react';
import { useParams } from 'react-router-dom';
import { SectionHeader } from '@/components/common/PageHeader';
import { RadarChart } from '@/components/charts/PieChart';
import { BarChart } from '@/components/charts/BarChart';
import { useClientKPIs } from '@/hooks/useClients';
import { PageLoader } from '@/components/ui/Loader';

// ============================================================
// Client KPI Tab
// ============================================================

export function ClientKPIPage() {
  const { id } = useParams<{ id: string }>();
  const { kpis, isLoading } = useClientKPIs(id ?? '');

  if (isLoading) return <PageLoader label="Loading KPIs…" />;

  const radarData = kpis.map((kpi: any) => ({
    subject: kpi.name,
    value: kpi.value,
    fullMark: 100,
  }));

  const barData = kpis.map((kpi: any) => ({
    name: kpi.name,
    value: kpi.value,
  }));

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="rounded-xl border bg-card p-6">
          <SectionHeader title="KPI Radar" description="Across all categories" className="mb-4" />
          <RadarChart data={radarData} height={280} />
        </div>
        <div className="rounded-xl border bg-card p-6">
          <SectionHeader title="KPI Breakdown" description="Score per metric" className="mb-4" />
          <BarChart
            data={barData}
            series={[{ dataKey: 'value', label: 'Score' }]}
            xDataKey="name"
            layout="vertical"
            height={280}
          />
        </div>
      </div>
    </div>
  );
}

// ============================================================
// Client Analysis Tab
// ============================================================

export function ClientAnalysisPage() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="space-y-6">
      <div className="rounded-xl border bg-card p-6">
        <SectionHeader title="AI Risk Analysis" description="Powered by machine learning" className="mb-4" />
        <p className="text-sm text-muted-foreground">Risk analysis module — implementation pending.</p>
      </div>
    </div>
  );
}

// ============================================================
// Client History Tab
// ============================================================

export function ClientHistoryPage() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="space-y-6">
      <div className="rounded-xl border bg-card p-6">
        <SectionHeader title="Historical Data" description="Health score & churn trend over time" className="mb-4" />
        <p className="text-sm text-muted-foreground">Historical data module — implementation pending.</p>
      </div>
    </div>
  );
}

// ============================================================
// Client Recommendations Tab
// ============================================================

export function ClientRecommendationsPage() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="space-y-6">
      <div className="rounded-xl border bg-card p-6">
        <SectionHeader title="AI Recommendations" description="Tailored actions for this client" className="mb-4" />
        <p className="text-sm text-muted-foreground">Recommendations module — implementation pending.</p>
      </div>
    </div>
  );
}
