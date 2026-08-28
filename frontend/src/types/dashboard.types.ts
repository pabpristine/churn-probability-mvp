// ============================================================
// Dashboard Types
// ============================================================

export interface MetricTrend {
  value: number;
  percentage: number;
  direction: 'up' | 'down' | 'neutral';
  period: string;
}

export interface DashboardMetric {
  id: string;
  label: string;
  value: number | string;
  formattedValue: string;
  trend?: MetricTrend;
  description?: string;
  icon?: string;
}

export interface ChurnRiskSummary {
  critical: number;
  high: number;
  medium: number;
  low: number;
  healthy: number;
  total: number;
}

export interface RevenueAtRisk {
  amount: number;
  percentage: number;
  clientCount: number;
}

export interface DashboardMetrics {
  totalClients: DashboardMetric;
  activeClients: DashboardMetric;
  atRiskClients: DashboardMetric;
  avgChurnProbability: DashboardMetric;
  avgHealthScore: DashboardMetric;
  totalMRR: DashboardMetric;
  totalARR: DashboardMetric;
  revenueAtRisk: RevenueAtRisk;
  churnRiskSummary: ChurnRiskSummary;
  recentAlerts: DashboardAlert[];
}

export interface DashboardAlert {
  id: string;
  type: 'critical' | 'warning' | 'info';
  clientId: string;
  clientName: string;
  message: string;
  timestamp: string;
  isRead: boolean;
}

export interface ChartDataPoint {
  label: string;
  value: number;
  secondaryValue?: number;
  date?: string;
  [key: string]: string | number | undefined;
}

export interface TimeSeriesDataPoint {
  date: string;
  value: number;
  label?: string;
}
