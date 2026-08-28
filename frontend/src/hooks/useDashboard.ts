import { useQuery } from '@tanstack/react-query';
import { useDashboardStore } from '@/store';
import { dashboardService } from '@/services';
import { QUERY_STALE_TIME } from '@/constants';
import type { DashboardMetrics, DashboardAlert, ChartDataPoint, TimeSeriesDataPoint } from '@/types';
import type { AxiosResponse } from 'axios';

// ============================================================
// Dashboard Hook
// ============================================================

export function useDashboard() {
  const store = useDashboardStore();

  const metricsQuery = useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: () => dashboardService.getMetrics().then((r: AxiosResponse<DashboardMetrics>) => r.data),
    staleTime: QUERY_STALE_TIME.SHORT,
    refetchInterval: 60_000,
  });

  const alertsQuery = useQuery({
    queryKey: ['dashboard', 'alerts'],
    queryFn: () => dashboardService.getAlerts().then((r: AxiosResponse<DashboardAlert[]>) => r.data),
    staleTime: QUERY_STALE_TIME.SHORT,
  });

  const churnChartQuery = useQuery({
    queryKey: ['dashboard', 'churn-risk-chart'],
    queryFn: () => dashboardService.getChurnRiskChart().then((r: AxiosResponse<ChartDataPoint[]>) => r.data),
    staleTime: QUERY_STALE_TIME.MEDIUM,
  });

  const revenueChartQuery = useQuery({
    queryKey: ['dashboard', 'revenue-chart'],
    queryFn: () => dashboardService.getRevenueChart().then((r: AxiosResponse<TimeSeriesDataPoint[]>) => r.data),
    staleTime: QUERY_STALE_TIME.MEDIUM,
  });

  const healthDistributionQuery = useQuery({
    queryKey: ['dashboard', 'health-distribution'],
    queryFn: () => dashboardService.getHealthDistribution().then((r: AxiosResponse<ChartDataPoint[]>) => r.data),
    staleTime: QUERY_STALE_TIME.MEDIUM,
  });

  return {
    metrics: metricsQuery.data ?? store.metrics,
    alerts: alertsQuery.data ?? store.alerts,
    churnRiskChart: churnChartQuery.data ?? store.churnRiskChart,
    revenueChart: revenueChartQuery.data ?? store.revenueChart,
    healthDistribution: healthDistributionQuery.data ?? store.healthDistribution,
    isLoading: metricsQuery.isLoading,
    isError: metricsQuery.isError,
    refetch: metricsQuery.refetch,
    markAlertAsRead: store.markAlertAsRead,
    unreadAlertCount: (alertsQuery.data ?? store.alerts).filter((a: DashboardAlert) => !a.isRead).length,
  };
}
