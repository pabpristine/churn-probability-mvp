import * as React from 'react';
import { motion } from 'framer-motion';
import { ContentWrapper } from '@/components/common/PageHeader';

// ── Dashboard feature components ──────────────────────────────
import { DashboardHeader }         from './components/DashboardHeader';
import { QuickActionBar }          from './components/QuickActionBar';
import { KPISection }              from './components/KPISection';
import { AISummaryCard }           from './components/AISummaryCard';
import { ClientHealthOverview }    from './components/ClientHealthOverview';
import { RiskDistributionChart, ChurnTrendChart } from './components/DashboardCharts';
import { HighRiskClientsTable }    from './components/HighRiskClientsTable';
import { RecentActivityTimeline }  from './components/RecentActivityTimeline';
import { WorkflowStatusCard }      from './components/WorkflowStatusCard';
import { RecentRecommendations }   from './components/RecentRecommendations';
import { AIAssistantPreview }      from './components/AIAssistantPreview';

// ============================================================
// Dashboard Page — Executive View
// ============================================================

export function DashboardPage() {
  const [refreshKey, setRefreshKey] = React.useState(0);

  return (
    <ContentWrapper className="space-y-5">

      {/* ── 1. Welcome Banner ── */}
      <DashboardHeader
        userName="Alex Johnson"
        userRole="Admin"
        company="Dirt2Dollar AI"
        systemStatus="operational"
      />

      {/* ── 2. Quick Actions ── */}
      <QuickActionBar
        onRefresh={() => setRefreshKey((k) => k + 1)}
      />

      {/* ── 3. KPI Cards ── */}
      <section aria-label="Key Performance Indicators">
        <KPISection />
      </section>

      {/* ── 4. AI Executive Summary ── */}
      <section aria-label="AI Executive Summary">
        <AISummaryCard />
      </section>

      {/* ── 5. Health + Distribution (2-col) ── */}
      <section
        aria-label="Client Health and Risk Distribution"
        className="grid grid-cols-1 lg:grid-cols-3 gap-4"
      >
        <ClientHealthOverview className="lg:col-span-2" />
        <RiskDistributionChart />
      </section>

      {/* ── 6. Churn Trend Chart ── */}
      <section aria-label="Monthly Churn Trend">
        <ChurnTrendChart />
      </section>

      {/* ── 7. High Risk Table ── */}
      <section aria-label="High Risk Clients">
        <HighRiskClientsTable />
      </section>

      {/* ── 8. Activity + Workflow (2-col) ── */}
      <section
        aria-label="Activity and Workflow"
        className="grid grid-cols-1 lg:grid-cols-3 gap-4"
      >
        <RecentActivityTimeline className="lg:col-span-2" />
        <WorkflowStatusCard />
      </section>

      {/* ── 9. Recent Recommendations ── */}
      <section aria-label="Recent Recommendations">
        <RecentRecommendations />
      </section>

      {/* ── 10. AI Assistant Preview ── */}
      <section aria-label="AI Assistant Preview">
        <AIAssistantPreview />
      </section>

      {/* ── 11. Footer ── */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex items-center justify-between py-4 border-t border-border"
      >
        <p className="text-[11.5px] text-muted-foreground">
          © 2025 Dirt2Dollar AI · All rights reserved
        </p>
        <div className="flex items-center gap-4">
          <a href="#" className="text-[11.5px] text-muted-foreground hover:text-foreground transition-colors">Privacy</a>
          <a href="#" className="text-[11.5px] text-muted-foreground hover:text-foreground transition-colors">Terms</a>
          <a href="#" className="text-[11.5px] text-muted-foreground hover:text-foreground transition-colors">Support</a>
        </div>
      </motion.footer>

    </ContentWrapper>
  );
}

export default DashboardPage;
