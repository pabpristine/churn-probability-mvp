// ============================================================
// Dashboard Seed Data — Placeholder shapes for UI dev
// Replaced by real API data when backend connects.
// ============================================================

import type {
  DashboardKPI,
  AISummary,
  ClientHealthBreakdown,
  ChurnTrendPoint,
  RiskDistributionSlice,
  ActivityItem,
  WorkflowStep,
  HighRiskClientRow,
  DashboardRecommendation,
  QuickAction,
} from './dashboard.types';

// ── KPIs ─────────────────────────────────────────────────────

export const PLACEHOLDER_KPIS: DashboardKPI[] = [
  {
    id: 'total_clients',
    label: 'Total Clients',
    value: 248,
    trend: { direction: 'up', percent: 4.2, period: 'vs last month' },
    sparkline: [220, 224, 230, 235, 238, 242, 248],
    iconColor: 'primary',
  },
  {
    id: 'healthy',
    label: 'Healthy Clients',
    value: 162,
    trend: { direction: 'up', percent: 2.8, period: 'vs last month' },
    sparkline: [145, 148, 151, 155, 158, 160, 162],
    iconColor: 'success',
  },
  {
    id: 'medium_risk',
    label: 'Medium Risk',
    value: 54,
    trend: { direction: 'down', percent: 1.4, period: 'vs last month' },
    sparkline: [60, 59, 57, 56, 55, 55, 54],
    iconColor: 'warning',
  },
  {
    id: 'high_risk',
    label: 'High Risk',
    value: 32,
    trend: { direction: 'up', percent: 6.7, period: 'vs last month' },
    sparkline: [25, 26, 27, 29, 30, 31, 32],
    iconColor: 'danger',
  },
  {
    id: 'ai_predictions',
    label: 'AI Predictions Today',
    value: 89,
    trend: { direction: 'up', percent: 12.1, period: 'vs yesterday' },
    sparkline: [40, 55, 60, 72, 78, 85, 89],
    iconColor: 'info',
  },
  {
    id: 'reports',
    label: 'Reports Generated',
    value: 17,
    trend: { direction: 'neutral', percent: 0, period: 'this week' },
    sparkline: [10, 12, 14, 14, 15, 16, 17],
    iconColor: 'primary',
  },
];

// ── AI Summary ────────────────────────────────────────────────

export const PLACEHOLDER_AI_SUMMARY: AISummary = {
  headline: 'Client portfolio health is stable with localized risk clusters.',
  body: 'Overall client health has improved compared to the previous reporting period. 12 enterprise clients require immediate attention due to declining KPIs and negative historical similarity patterns. Revenue at risk has decreased by 3.2%, however the SaaS and FinTech segments continue to show elevated churn signals. AI models processed 89 predictions today with an average confidence of 83%. Automated workflows completed 34 executions with a 97.1% success rate.',
  confidence: 0.83,
  generatedAt: 'Today at 09:14 AM',
  flags: ['12 clients need immediate action', '3 workflows failed overnight', 'SaaS churn signal elevated'],
};

// ── Client Health ─────────────────────────────────────────────

export const PLACEHOLDER_HEALTH: ClientHealthBreakdown = {
  healthy: 162,
  medium: 54,
  high: 20,
  critical: 12,
  total: 248,
};

// ── Churn Trend ───────────────────────────────────────────────

export const PLACEHOLDER_CHURN_TREND: ChurnTrendPoint[] = [
  { month: 'Jan', churnRate: 6.2, predicted: 6.0 },
  { month: 'Feb', churnRate: 5.8, predicted: 5.9 },
  { month: 'Mar', churnRate: 6.5, predicted: 6.1 },
  { month: 'Apr', churnRate: 5.2, predicted: 5.5 },
  { month: 'May', churnRate: 4.8, predicted: 5.0 },
  { month: 'Jun', churnRate: 5.4, predicted: 5.2 },
  { month: 'Jul', churnRate: 6.1, predicted: 5.8 },
  { month: 'Aug', churnRate: 5.9, predicted: 5.6 },
  { month: 'Sep', churnRate: 4.6, predicted: 5.0 },
  { month: 'Oct', churnRate: 4.2, predicted: 4.8 },
  { month: 'Nov', churnRate: 3.8, predicted: 4.2 },
  { month: 'Dec', churnRate: 3.5, predicted: 3.9 },
];

// ── Risk Distribution ─────────────────────────────────────────

export const PLACEHOLDER_RISK_DISTRIBUTION: RiskDistributionSlice[] = [
  { name: 'Healthy',  value: 162, color: '#22C55E' },
  { name: 'Medium',   value: 54,  color: '#F59E0B' },
  { name: 'High',     value: 20,  color: '#EF4444' },
  { name: 'Critical', value: 12,  color: '#991B1B' },
];

// ── Activity ──────────────────────────────────────────────────

export const PLACEHOLDER_ACTIVITY: ActivityItem[] = [
  { id: '1', type: 'ai_analysis',        title: 'AI Analysis Complete',     description: 'Batch analysis for 89 clients finished', timestamp: '9 min ago',  isNew: true },
  { id: '2', type: 'alert_triggered',    title: 'High Risk Alert',          description: 'Acme Corp churn probability exceeded 85%', client: 'Acme Corp', timestamp: '24 min ago', isNew: true },
  { id: '3', type: 'workflow_executed',  title: 'Workflow Completed',       description: 'Client Onboarding workflow ran successfully', timestamp: '1h ago' },
  { id: '4', type: 'report_generated',  title: 'Report Generated',         description: 'Monthly Executive Summary exported', timestamp: '2h ago' },
  { id: '5', type: 'recommendation_sent', title: 'Recommendation Sent',    description: 'Next-best-action delivered to GlobalTech AM', client: 'GlobalTech', timestamp: '3h ago' },
  { id: '6', type: 'client_updated',    title: 'Client Data Refreshed',    description: 'FinServe Inc KPI data synced from CRM', client: 'FinServe Inc', timestamp: '5h ago' },
];

// ── Workflow Steps ─────────────────────────────────────────────

export const PLACEHOLDER_WORKFLOW: WorkflowStep[] = [
  { id: 'slack',       name: 'Slack Trigger',      status: 'completed', duration: '0.1s' },
  { id: 'retrieval',   name: 'Client Retrieval',   status: 'completed', duration: '0.4s' },
  { id: 'summary',     name: 'Data Summary',        status: 'completed', duration: '1.2s' },
  { id: 'embedding',   name: 'Embedding',           status: 'completed', duration: '2.1s' },
  { id: 'similarity',  name: 'Similarity Search',   status: 'completed', duration: '0.8s' },
  { id: 'groq',        name: 'Groq Analysis',       status: 'running',   duration: '—' },
  { id: 'recommend',   name: 'Recommendation',      status: 'pending' },
  { id: 'complete',    name: 'Completed',            status: 'pending' },
];

// ── High Risk Clients ─────────────────────────────────────────

export const PLACEHOLDER_HIGH_RISK: HighRiskClientRow[] = [
  { id: '1', name: 'Acme Corporation',  industry: 'SaaS',      healthScore: 28, churnProbability: 87, trend: 'down', riskLevel: 'critical', mrr: 42000 },
  { id: '2', name: 'GlobalTech Ltd',    industry: 'FinTech',   healthScore: 34, churnProbability: 79, trend: 'down', riskLevel: 'high',     mrr: 28500 },
  { id: '3', name: 'Nexus Systems',     industry: 'E-Commerce',healthScore: 41, churnProbability: 73, trend: 'down', riskLevel: 'high',     mrr: 19800 },
  { id: '4', name: 'Apex Dynamics',     industry: 'Healthcare',healthScore: 45, churnProbability: 68, trend: 'neutral', riskLevel: 'high',  mrr: 15200 },
  { id: '5', name: 'StrataCom Group',   industry: 'Logistics', healthScore: 50, churnProbability: 62, trend: 'up',   riskLevel: 'medium',   mrr: 11600 },
];

// ── Recommendations ────────────────────────────────────────────

export const PLACEHOLDER_RECOMMENDATIONS: DashboardRecommendation[] = [
  { id: '1', title: 'Schedule Executive Business Review', description: 'Acme Corp has had no EBR in 90+ days. Engagement score is critically low.', client: 'Acme Corp',   priority: 'critical', confidence: 0.91, category: 'Engagement' },
  { id: '2', title: 'Offer Feature Training Session',     description: 'GlobalTech is underutilizing 3 core features. Adoption increase correlates with 34% churn reduction.', client: 'GlobalTech', priority: 'high', confidence: 0.84, category: 'Adoption' },
  { id: '3', title: 'Contract Renewal Risk Mitigation',   description: 'Nexus Systems contract ends in 47 days. No renewal discussion initiated.', client: 'Nexus Systems', priority: 'high', confidence: 0.78, category: 'Retention' },
];

// ── Quick Actions ─────────────────────────────────────────────

export const QUICK_ACTIONS: QuickAction[] = [
  { id: 'analyze',   label: 'Analyze Client',    description: 'Run AI analysis on any client',      icon: 'brain',         color: 'primary', href: '/clients' },
  { id: 'report',    label: 'Generate Report',   description: 'Export executive summary',           icon: 'file-text',     color: 'success', href: '/reports' },
  { id: 'ai',        label: 'AI Assistant',      description: 'Ask Dirt2Dollar AI anything',        icon: 'sparkles',      color: 'info'    },
  { id: 'workflow',  label: 'Workflow Monitor',  description: 'View automation pipeline status',    icon: 'git-branch',    color: 'warning', href: '/workflow' },
  { id: 'export',    label: 'Export Dashboard',  description: 'Download dashboard as PDF',          icon: 'download',      color: 'default' },
  { id: 'refresh',   label: 'Refresh Data',      description: 'Pull latest data from backend',      icon: 'refresh-cw',    color: 'default' },
];
