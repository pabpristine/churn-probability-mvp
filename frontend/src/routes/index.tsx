import { createBrowserRouter } from 'react-router-dom';
import { AppLayout } from '@/layouts/AppLayout';
import { DashboardPage } from '@/pages/Dashboard';
import { ClientsPage } from '@/pages/Clients';
import {
  ClientDetailPage,
  ClientKPIPage,
  ClientAnalysisPage,
  ClientHistoryPage,
  ClientRecommendationsPage,
} from '@/pages/ClientDetails';
import { AnalyticsPage } from '@/pages/Analytics';
import { WorkflowPage } from '@/pages/Workflow';
import { RecommendationsPage } from '@/pages/Recommendations';
import { ReportsPage } from '@/pages/Reports';
import { SettingsPage } from '@/pages/Settings';
import { AIAnalysisPage } from '@/pages/AIAnalysis';
import { HistoricalClientsPage } from '@/pages/HistoricalClients';
import { ROUTES } from '@/constants/routes.constants';

// ============================================================
// Application Router
// ============================================================

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      // Dashboard
      {
        index: true,
        element: <DashboardPage />,
      },

      // AI Analysis Page
      {
        path: 'ai-analysis',
        element: <AIAnalysisPage />,
      },

      // Historical Clients Page
      {
        path: 'historical',
        element: <HistoricalClientsPage />,
      },
      {
        path: 'historical-clients',
        element: <HistoricalClientsPage />,
      },

      // Clients list
      {
        path: 'clients',
        element: <ClientsPage />,
      },

      // Client detail (nested)
      {
        path: 'client/:id',
        element: <ClientDetailPage />,
        children: [
          {
            index: true,
            element: <ClientKPIPage />,
          },
          {
            path: 'kpi',
            element: <ClientKPIPage />,
          },
          {
            path: 'analysis',
            element: <ClientAnalysisPage />,
          },
          {
            path: 'history',
            element: <ClientHistoryPage />,
          },
          {
            path: 'recommendations',
            element: <ClientRecommendationsPage />,
          },
        ],
      },

      // Analytics
      {
        path: 'analytics',
        element: <AnalyticsPage />,
      },

      // Workflow Monitor
      {
        path: 'workflow',
        element: <WorkflowPage />,
      },

      // Recommendations
      {
        path: 'recommendations',
        element: <RecommendationsPage />,
      },

      // Reports
      {
        path: 'reports',
        element: <ReportsPage />,
      },

      // Settings
      {
        path: 'settings',
        element: <SettingsPage />,
      },
    ],
  },
]);

export default router;
