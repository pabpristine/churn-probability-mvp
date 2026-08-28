import apiClient from './api/axios.instance';
import type { DashboardMetrics, DashboardAlert, ChartDataPoint, TimeSeriesDataPoint } from '@/types';
import { API_ENDPOINTS } from '@/constants';

// ============================================================
// Dashboard Service — wire up during implementation
// ============================================================

export const dashboardService = {
  getMetrics: () =>
    apiClient.get<DashboardMetrics>(API_ENDPOINTS.DASHBOARD.METRICS),

  getAlerts: () =>
    apiClient.get<DashboardAlert[]>(API_ENDPOINTS.DASHBOARD.ALERTS),

  getRecentActivity: () =>
    apiClient.get(API_ENDPOINTS.DASHBOARD.RECENT_ACTIVITY),

  getChurnRiskChart: () =>
    apiClient.get<ChartDataPoint[]>(API_ENDPOINTS.DASHBOARD.CHURN_RISK_CHART),

  getRevenueChart: (period?: string) =>
    apiClient.get<TimeSeriesDataPoint[]>(API_ENDPOINTS.DASHBOARD.REVENUE_CHART, {
      params: { period },
    }),

  getHealthDistribution: () =>
    apiClient.get<ChartDataPoint[]>(API_ENDPOINTS.DASHBOARD.HEALTH_DISTRIBUTION),
};
