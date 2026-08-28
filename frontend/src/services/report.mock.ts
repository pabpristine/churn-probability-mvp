import type { Report, ReportStatistics, ReportHistoryItem } from '@/types';

export const MOCK_REPORT_STATISTICS: ReportStatistics = {
  totalReports: 243,
  generatedThisMonth: 42,
  scheduledReports: 12,
  pendingReports: 3,
  failedReports: 1,
};

export const MOCK_REPORTS: Report[] = [
  {
    id: 'rep-001',
    name: 'Q3 Enterprise Client Intelligence',
    type: 'Client Intelligence',
    clientId: 'c-101',
    clientName: 'ABC Corporation',
    status: 'ready',
    format: 'PDF',
    sizeBytes: 2540000, // ~2.5MB
    generatedBy: 'Sarah Jenkins',
    createdAt: '2025-05-21T10:42:00Z',
    updatedAt: '2025-05-21T10:43:12Z',
    generationDuration: 72.4,
    sections: ['Executive Summary', 'KPI Analysis', 'AI Churn Analysis', 'Recommendations'],
    version: 1,
  },
  {
    id: 'rep-002',
    name: 'Global Tech - High Risk Alert',
    type: 'AI Churn Analysis',
    clientId: 'c-103',
    clientName: 'Global Tech',
    status: 'ready',
    format: 'PDF',
    sizeBytes: 1100000,
    generatedBy: 'Automated System',
    createdAt: '2025-05-20T08:15:00Z',
    updatedAt: '2025-05-20T08:15:45Z',
    generationDuration: 45.1,
    sections: ['Executive Summary', 'AI Churn Analysis', 'Historical Similar Clients', 'Recommendations'],
    version: 1,
  },
  {
    id: 'rep-003',
    name: 'XYZ Solutions Benchmarking',
    type: 'KPI Analytics',
    clientId: 'c-102',
    clientName: 'XYZ Solutions',
    status: 'scheduled',
    format: 'Excel',
    generatedBy: 'Michael Chang',
    createdAt: '2025-05-22T00:00:00Z',
    updatedAt: '2025-05-22T00:00:00Z',
    sections: ['KPI Analysis', 'Trend Interpretation'],
    version: 1,
  },
  {
    id: 'rep-004',
    name: 'Acme Corp Annual Review',
    type: 'Executive Report',
    clientId: 'c-104',
    clientName: 'Acme Corp',
    status: 'failed',
    format: 'PDF',
    generatedBy: 'Sarah Jenkins',
    createdAt: '2025-05-19T14:30:00Z',
    updatedAt: '2025-05-19T14:32:10Z',
    generationDuration: 130.5,
    sections: ['Executive Summary', 'KPI Analysis', 'Trend Interpretation', 'Activity'],
    version: 1,
  },
  {
    id: 'rep-005',
    name: 'Workflow Execution Log - May',
    type: 'Workflow Execution',
    clientId: 'sys-001',
    clientName: 'System Default',
    status: 'generating',
    format: 'CSV',
    generatedBy: 'Admin User',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    sections: ['Workflow Details', 'Activity'],
    version: 1,
  },
  {
    id: 'rep-006',
    name: 'TechFlow Recommendations',
    type: 'Recommendations',
    clientId: 'c-105',
    clientName: 'TechFlow',
    status: 'archived',
    format: 'PDF',
    sizeBytes: 850000,
    generatedBy: 'Michael Chang',
    createdAt: '2025-04-15T09:20:00Z',
    updatedAt: '2025-04-15T09:21:00Z',
    generationDuration: 60.2,
    sections: ['Recommendations'],
    version: 1,
  }
];

export const MOCK_REPORT_HISTORY: ReportHistoryItem[] = [
  { id: 'hist-1', reportId: 'rep-001', action: 'generated', reportType: 'Client Intelligence', clientName: 'ABC Corporation', timestamp: '2025-05-21T10:43:12Z', actor: 'Sarah Jenkins' },
  { id: 'hist-2', reportId: 'rep-001', action: 'downloaded', reportType: 'Client Intelligence', clientName: 'ABC Corporation', timestamp: '2025-05-21T11:05:00Z', actor: 'Sarah Jenkins' },
  { id: 'hist-3', reportId: 'rep-002', action: 'generated', reportType: 'AI Churn Analysis', clientName: 'Global Tech', timestamp: '2025-05-20T08:15:45Z', actor: 'Automated System' },
  { id: 'hist-4', reportId: 'rep-002', action: 'shared', reportType: 'AI Churn Analysis', clientName: 'Global Tech', timestamp: '2025-05-20T09:30:00Z', actor: 'Alex Manager' },
  { id: 'hist-5', reportId: 'rep-004', action: 'failed', reportType: 'Executive Report', clientName: 'Acme Corp', timestamp: '2025-05-19T14:32:10Z', actor: 'System' },
  { id: 'hist-6', reportId: 'rep-006', action: 'archived', reportType: 'Recommendations', clientName: 'TechFlow', timestamp: '2025-05-10T12:00:00Z', actor: 'Michael Chang' }
];

export const MOCK_REPORT_VOLUME_DATA = [
  { date: 'Mon', reports: 12 },
  { date: 'Tue', reports: 19 },
  { date: 'Wed', reports: 15 },
  { date: 'Thu', reports: 22 },
  { date: 'Fri', reports: 28 },
  { date: 'Sat', reports: 4 },
  { date: 'Sun', reports: 7 },
];

export const MOCK_REPORT_TYPE_DATA = [
  { name: 'Executive', value: 45, color: 'hsl(var(--primary))' },
  { name: 'Client Intelligence', value: 30, color: 'hsl(var(--purple-accent))' },
  { name: 'KPI Analytics', value: 25, color: 'hsl(var(--success))' },
  { name: 'AI Churn Analysis', value: 20, color: 'hsl(var(--warning))' },
  { name: 'Recommendations', value: 15, color: 'hsl(var(--orange-accent))' },
];

export const MOCK_REPORT_TIME_DATA = [
  { name: 'Executive', time: 45 },
  { name: 'Client Intel', time: 62 },
  { name: 'KPI Analytics', time: 18 },
  { name: 'AI Churn', time: 85 },
  { name: 'Recommendations', time: 25 },
];
