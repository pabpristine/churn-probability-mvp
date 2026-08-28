import type { Report, ReportStatistics, ReportHistoryItem, ReportConfiguration } from '@/types';
import apiClient from './api/axios.instance';

export const reportService = {
  getReports: async () => {
    const { data } = await apiClient.get<Report[]>('/reports');
    return { data };
  },

  getReport: async (id: string) => {
    const { data } = await apiClient.get<Report>(`/reports/${id}`);
    return { data };
  },

  getReportStatistics: async () => {
    return {
      data: {
        totalReports: 24,
        generatedThisMonth: 12,
        scheduledReports: 3,
        pendingReports: 0,
        failedReports: 1,
      }
    };
  },

  getReportHistory: async () => {
    return {
      data: [
        {
          id: "rh-1",
          reportId: "rep-0",
          action: "generated",
          reportType: "AI Churn Report",
          clientName: "Yardworx Land Management",
          timestamp: "2026-08-21T18:24:25Z",
          actor: "Current User"
        }
      ]
    };
  },

  generateReport: async (config: ReportConfiguration) => {
    const { data } = await apiClient.post<Report>('/reports', config);
    return { data };
  },
  
  deleteReport: async (_id: string) => {
    return { data: { success: true } };
  },
  
  archiveReport: async (_id: string) => {
    return { data: { success: true } };
  },

  getAnalytics: async () => {
    return {
      data: {
        volume: [
          { date: "Aug 15", reports: 4 },
          { date: "Aug 16", reports: 2 },
          { date: "Aug 17", reports: 5 },
          { date: "Aug 18", reports: 3 },
          { date: "Aug 19", reports: 6 },
          { date: "Aug 20", reports: 4 },
          { date: "Aug 21", reports: 7 }
        ],
        typeDistribution: [
          { name: "AI Churn Report", value: 12, color: "hsl(var(--primary))" },
          { name: "Executive Report", value: 6, color: "hsl(var(--purple-accent))" },
          { name: "KPI Report", value: 4, color: "hsl(var(--success))" },
          { name: "Recommendation Report", value: 2, color: "hsl(var(--warning))" }
        ],
        generationTime: [
          { name: "0-2s", value: 15 },
          { name: "2-5s", value: 8 },
          { name: "5s+", value: 1 }
        ]
      }
    };
  }
};


